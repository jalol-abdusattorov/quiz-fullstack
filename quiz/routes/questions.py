import bson
from bson.objectid import ObjectId
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status

from mongodb import *
from models import QuestionRequest
from routes.route_utils import swagger_bearer_scheme, check_valid_question

router = APIRouter()
permission_denied_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="permission denied")
invalid_id_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid id")

# AUTHORIZED AND ADMIN
@router.post("/questions")
def create_question(
    question: QuestionRequest,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if not request.state.admin:
        raise permission_denied_exception

    check_valid_question(question)

    new_question = {
        "question": question.question,
        "options": question.options,
        "correct_answer": question.correct_answer,
        "category": question.category,
        "difficulty": question.difficulty
    }

    question_id = questions_collection.insert_one(new_question).inserted_id
    return {"question_id": str(question_id)}


# AUTHORIZED AND ADMIN
@router.get("/questions/{question_id}")
def get_question(
    question_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if not request.state.admin:
        raise permission_denied_exception

    try:
        question_id = ObjectId(question_id)
        question = questions_collection.find_one(
            {
                "_id": question_id
            },
            {
                "_id": 1,
                "question": 1,
                "options": 1,
                "category": 1,
                "difficulty": 1
            }
        )

        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="question not found")

        question['_id'] = str(question['_id'])

        return question

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED AND ADMIN
@router.get("/questions/{question_id}/statistics")
def get_question_statistics(
    question_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if not request.state.admin:
        raise permission_denied_exception

    try:
        question_id = ObjectId(question_id)

        result = results_collection.aggregate([
            {
                '$unwind': {
                    'path': '$answers'
                }
            },
            {
                '$match': {
                    'answers.question_id': question_id
                }
            },
            {
                '$group': {
                    '_id': '$answers.question_id', 
                    'times_answered': {
                        '$sum': 1
                    }, 
                    'correct': {
                        '$sum': {
                            '$cond': [
                                { '$eq': [ '$answers.is_correct', True ] },
                                1, # if answer is correct
                                0  # if answer is not correct
                            ]
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'question_id': '$_id',
                    'times_answered': '$times_answered',
                    'correct': '$correct',
                    'incorrect': {
                        '$subtract': [ '$times_answered', '$correct' ]
                    },
                    'accuracy': {
                        '$multiply': [
                            { '$divide': [ '$correct', '$times_answered' ] },
                            100
                        ]
                    }
                }
            }
        ])

        final_result = list(result)
        
        if not final_result:
            return {"message": "this user has no statistics or invalid id"}

        # avoid returning ObjectId
        final_result[0]["question_id"] = str(final_result[0]["question_id"])
        final_result[0]['accuracy'] = round(final_result[0]['accuracy'], 2)

        return {"result": final_result[0]}

    except bson.errors.InvalidId:
        raise invalid_id_exception
