import json
import bson
from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime as dt

from mongodb import questions_collection, attempts_collection
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


def consume_attempt(attempt_id, quiz_id, user_email):
    attempt = attempts_collection.find_one_and_delete({
        "attempt_id": attempt_id,
        "quiz_id": quiz_id,
        "user_email": user_email,
    })

    if attempt is None:
        raise HTTPException(
            status_code=403, detail="quiz didn't start yet or invalid attempt_id"
        )
    return attempt["started_at"]
 
 
def validate_user_inputs_and_calculate_result(request, quiz, user_email) -> tuple:
    quiz_question_ids = set(quiz["question_ids"])
    available_answers = [0, 1, 2, 3]

    selected = {}
    for answer in request.answers:
        try:
            question_id = ObjectId(answer["question_id"])
        except bson.errors.InvalidId:
            raise HTTPException(
                status_code=400, detail=f"invalid id '{answer['question_id']}'"
            )
 
        if answer["selected_answer"] not in available_answers:
            raise HTTPException(
                status_code=403, detail="only available answers 0, 1, 2 and 3"
            )
        if question_id in selected:
            raise HTTPException(
                status_code=403, detail="cannot accept duplicate question_ids"
            )
        if question_id not in quiz_question_ids:
            raise HTTPException(
                status_code=404, detail=f"question not found '{question_id}'"
            )
 
        selected[question_id] = answer["selected_answer"]
 
    correct_answers = {
        q["_id"]: q["correct_answer"]
        for q in questions_collection.find(
            {"_id": {"$in": list(selected)}}, {"correct_answer": 1}
        )
    }
 
    score = 0
    answers = []
    for question_id, selected_answer in selected.items():
        if question_id not in correct_answers:
            raise HTTPException(
                status_code=404, detail=f"question not found '{question_id}'"
            )
 
        is_correct = selected_answer == correct_answers[question_id]
        if is_correct:
            score += 1
 
        answers.append({
            "question_id": question_id,
            "selected_answer": selected_answer,
            "is_correct": is_correct,
        })
 
    started_at = consume_attempt(request.attempt_id, quiz["_id"], user_email)
 
    return answers, score, started_at