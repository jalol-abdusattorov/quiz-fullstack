import json
import bson
from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime as dt

from mongodb import questions_collection
from models import QuestionRequest, Quiz, UserRequest


swagger_bearer_scheme = HTTPBearer(auto_error=False)

def check_valid_question(question: QuestionRequest):
    if not question.question.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="question must not be empty")
    
    if len(question.options) != 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only 4 options")
    
    if question.correct_answer < 0 or question.correct_answer > 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="correct answer must be 0, 1, 2 or 3")

    if question.difficulty not in ['easy', 'medium', 'hard']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="difficulty must be easy, medium or hard")

    seen = []

    for i in question.options:
        if i not in seen:
            seen.append(i)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cannot accept duplicate options")


def check_valid_user_inputs(user: UserRequest):
    if not user.username.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username shouldn't be empty")
    if not user.email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email shouldn't be empty")
    if not user.password.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password shouldn't be empty")


def check_valid_quiz(quiz: Quiz):
    if not quiz.title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title shouldn't be empty")

    if not all(q_id.strip() for q_id in quiz.question_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="there should be no empty question_ids")

    if quiz.difficulty not in ['easy', 'medium', 'hard']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="difficulty must be easy, medium or hard")

    if quiz.time_limit <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="time_limit should be greater than 0")

    if len(quiz.question_ids) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="atleast one question id")

    for i in range(len(quiz.question_ids)):
        try:
            quiz.question_ids[i] = ObjectId(quiz.question_ids[i])

            is_valid_question_id = questions_collection.find_one({ "_id": quiz.question_ids[i] })

            if not is_valid_question_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"question id '{quiz.question_ids[i]}' not found")

        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"invalid qustion id '{quiz.question_ids[i]}' ")


def update_quiz_json_file_after_starting(_id, quiz_id):
    with open("quiz.json", 'r') as f:
        quizzes = json.load(f)
        quizzes.append({
            "attempt_id": _id,
            "quiz_id": quiz_id,
            "started_at": dt.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        with open('quiz.json', 'w') as f2:
            json.dump(quizzes, f2, indent = 4)


def find_errors_and_get_score_after_submitting(request, quiz) -> tuple:
    try:
        seen_question_ids = []
        available_answers = [0, 1, 2, 3]

        answered_count = 0
        score = 0
        answers = []
        for answer in request.answers:
            answer['question_id'] = ObjectId(answer['question_id'])

            if answer['selected_answer'] not in available_answers:
                raise HTTPException(status_code=403, detail="only available answers 0, 1, 2 and 3")

            if str(answer['question_id']) in seen_question_ids:
                raise HTTPException(status_code=403, detail="cannot accept duplicate question_ids")

            if answer['question_id'] not in quiz['question_ids']:
                raise HTTPException(status_code=404, detail=f"question not found '{answer['question_id']}'")

            seen_question_ids.append(str(answer['question_id']))
            question = questions_collection.find_one({ "_id": answer['question_id'] })

            if answer['selected_answer'] == question['correct_answer']:
                score += 1

                answers.append({
                                "question_id": answer['question_id'],
                                "selected_answer": answer['selected_answer'],
                                "is_correct": True
                })

            else:
                answers.append({
                    "question_id": answer['question_id'],
                    "selected_answer": answer['selected_answer'],
                    "is_correct": False
                })
            answered_count += 1

        if answered_count != len(quiz['question_ids']):
            raise HTTPException(status_code=400, detail=f"please answer all of the questions (answered {answered_count}/{len(quiz['question_ids'])})")

        started_at = update_quiz_json_file_after_submitting(request)

        return (answers, score, started_at)

    except bson.errors.InvalidId:
        raise HTTPException(status_code=400, detail=f"invalid id '{answer['question_id']}'")


def update_quiz_json_file_after_submitting(request):
    with open("quiz.json", "r") as f:
        quizzes = json.load(f)

        for i in quizzes:
            if request.attempt_id == i['attempt_id']:
                quiz_json_started_at = i['started_at']

                with open("quiz.json", 'w') as f2:
                    quizzes.remove(i)
                    json.dump(quizzes, f2, indent = 4)

                break
        else:
            raise HTTPException(status_code=403, detail="quiz didn't started yet or invalid attempt_id")

    return quiz_json_started_at