import bson
from bson import ObjectId
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from datetime import datetime as dt, timezone
from datetime import timedelta

from models import UserRequest
from mongodb import *
from auth.utils.auth_utils import get_password_hash
from routes.route_utils import swagger_bearer_scheme, check_valid_user_inputs
from auth.services.auth_service import create_acces_token

router = APIRouter()

invalid_id_exception = HTTPException(status_code=400, detail="invalid id")
user_doesnt_exist_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user doesn't exist")


# NO AUTH
@router.post("/users")
def create_user(user: UserRequest):
    unique_email = users_collection.find_one({ "email": user.email })
    if unique_email:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="email is not unique")

    check_valid_user_inputs(user)

    if "admin" not in [i['role'] for i in users_collection.find({})]:
        new_user = {
            "username": user.username,
            "email": user.email,
            "password_hash": get_password_hash(user.password),
            "created_at": dt.now(),
            "role": "admin"
        }
        
        access_token_expires = timedelta(minutes=1440)
        access_token = create_acces_token(
            data={'sub': user.email, 'admin': True},
            expires_delta=access_token_expires
        )
    else:
        new_user = {
            "username": user.username,
            "email": user.email,
            "password_hash": get_password_hash(user.password),
            "created_at": dt.now(),
            "role": "user"
        }
        
        access_token_expires = timedelta(minutes=1440)
        access_token = create_acces_token(
            data={'sub': user.email, 'admin': False},
            expires_delta=access_token_expires
        )


    user_id = users_collection.insert_one(new_user).inserted_id
    return {"user-id": str(user_id), "token": access_token}


# AUTHORIZED
@router.get("/users/{user_id}")
def get_user(
    user_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        user_id = ObjectId(user_id)
        user = users_collection.find_one({ "_id": user_id })

        if not user:
            raise user_doesnt_exist_exception

        # avoid returning ObjectId, and dont return password
        user['_id'] = str(user['_id'])
        user.pop("password_hash")

        return user
    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.get("/users/{user_id}/statistics")
def get_user_statistics(
    user_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        user_id = ObjectId(user_id)

        if not users_collection.find_one({ "_id": user_id }):
            raise user_doesnt_exist_exception

        result = results_collection.aggregate([
                {
                    '$match': {
                        'user_id': user_id
                    }
                },
                {
                    '$group': {
                        '_id': None, 
                        'quizzes_taken': {
                            '$sum': 1
                        }, 
                        'average_score': {
                            '$avg': '$score'
                        }, 
                        'best_score': {
                            '$max': '$score'
                        }, 
                        'total_questions_answered': {
                            '$sum': {
                                '$size': '$answers'
                            }
                        }, 
                        'correct_answers': {
                            '$sum': '$score'
                        }
                    }
                },
                {
                    '$project': {
                        '_id': 0, 
                        'quizzes_taken': '$quizzes_taken', 
                        'average_score': '$average_score', 
                        'best_score': '$best_score', 
                        'total_questions_answered': '$total_questions_answered', 
                        'correct_answers': '$correct_answers', 
                        'accuracy': {
                            '$multiply': [
                                { '$divide': [ '$correct_answers', '$total_questions_answered' ] },
                                100
                            ]
                        }
                    }
                }
            ])

        final_result = list(result)

        if not final_result:
            return {"message": "this user has no statistics"}

        return {"result": final_result}

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.get("/users/{user_id}/history/{page}")
def get_user_history(
    user_id: str,
    page: int,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        user_id = ObjectId(user_id)

        user_exists = users_collection.find_one({ "_id": user_id })
        if not user_exists:
            raise user_doesnt_exist_exception

        if page <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page should be greater than 0")

        # page 1 => 0 - 10 docs
        # page 2 => 10 - 20 docs
        # ...
        skipping_value = (page - 1) * 10
        limit = 10

        result = results_collection.aggregate([
            {
                "$match": {
                    "user_id": user_id
                }
            },
            {
                "$lookup": {
                    "from":         "quizzes",
                    "localField":   "quiz_id",
                    "foreignField": "_id",
                    "as":           "quiz"
                }
            },
            {
                "$unwind": {
                    "path": "$quiz"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "quiz_id": "$quiz_id",
                    "title": "$quiz.title",
                    "percentage": "$percentage",
                    "quiz_started_at": "$started_at"
                }
            },
            {
                "$group": {
                    "_id": "$quiz_id",
                    "average_percentage": {
                        "$avg": "$percentage"
                    },
                    "started_at": {
                        "$first": "$quiz_started_at"
                    }
                }
            },
            {
                "$skip": skipping_value
            },
            {
                "$limit": limit
            }
        ])

        final_result = list(result)

        if not final_result:
            return {"message": "this user has no statistics on this page"}

        for i in range(len(final_result)):
            final_result[i]['_id'] = str(final_result[i]['_id'])

        return {"result": final_result}

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.get("/users/{user_id}/recent-attempts")
def get_user_recent_attempts(
    user_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        user_id = ObjectId(user_id)

        user_exists = users_collection.find_one({ "_id": user_id })
        if not user_exists:
            raise user_doesnt_exist_exception

        time_threshold = dt.now(timezone.utc) - timedelta(days=4)
        result = results_collection.aggregate([
            {
                '$match': {
                    'user_id': user_id
                }
            },
            {
                '$match': {
                    'completed_at': {
                        '$gte': time_threshold
                    }
                }
            },
            {
                '$group': {
                    '_id': '$quiz_id', 
                    'user_id': {
                        '$first': '$user_id'
                    }, 
                    'quiz_id': {
                        '$first': '$quiz_id'
                    }, 
                    'answers': {
                        '$first': '$answers'
                    }, 
                    'score': {
                        '$first': '$score'
                    }, 
                    'total_questions': {
                        '$first': '$total_questions'
                    }, 
                    'percentage': {
                        '$first': '$percentage'
                    }, 
                    'started_at': {
                        '$first': '$started_at'
                    }, 
                    'completed_at': {
                        '$first': '$completed_at'
                    }, 
                    'time_taken': {
                        '$first': '$time_taken'
                    }
                }
            },
            {
                '$lookup': {
                    'from':         'quizzes', 
                    'localField':   'quiz_id', 
                    'foreignField': '_id', 
                    'as':           'quiz_details'
                }
            },
            {
                '$unwind': {
                    'path': '$quiz_details'
                }
            }
        ])

        final_result = list(result)

        if not final_result:
            return {"message": "this user has no recent attemtps"}

        quizzes = []
        for doc in final_result:
            doc['quiz_details']['_id'] = str(doc['quiz_details']['_id'])
            for i in range(len(doc['quiz_details']['question_ids'])):
                doc['quiz_details']['question_ids'][i] = str(doc['quiz_details']['question_ids'][i])

            doc['quiz_details']['taken_at'] = doc['started_at']
            doc['quiz_details']['completed_at'] = doc['completed_at']

            quizzes.append(doc['quiz_details'])

        return {"result": quizzes}

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.get("/users/{user_id}/attempts")
def get_user_attempts(
    user_id: str,
    page: int,
    sortingBy: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        user_id = ObjectId(user_id)
    except bson.errors.InvalidId:
        raise invalid_id_exception

    if sortingBy not in ['newestFirst', 'oldestFirst', 'highestAccuracy', 'lowestAccuracy']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid sorting")

    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page should be greater than 0")

    user_exists = users_collection.find_one({ "_id": user_id })
    if not user_exists:
        raise user_doesnt_exist_exception

    skipping_value = (page - 1) * 10
    limit = 10

    sortBy_map = {
        "newestFirst": "started_at",
        "oldestFirst": "started_at"
    }

    if sortingBy in sortBy_map:
        sortBy = sortBy_map[sortingBy]
    else:
        sortBy = "percentage"

    sortOrder = -1 if sortingBy == "newestFirst" or sortingBy == "highestAccuracy" else 1

    cursor = results_collection.aggregate([
        {
            '$match': {
                'user_id': user_id
            }
        },
        {
            '$lookup': {
                'from':         'quizzes', 
                'localField':   'quiz_id', 
                'foreignField': '_id', 
                'as':           'quiz_details'
            }
        },
        {
            '$unwind': {
                'path': '$quiz_details'
            }
        },
        {
            '$project': {
                "user_id": "$user_id",
                "quiz_id": "$quiz_id",
                "score": "$score",
                "total_questions": "$total_questions",
                "percentage": "$percentage",
                "started_at": "$started_at",
                "time_taken": "$time_taken",
                "quiz_title": "$quiz_details.title",
                "quiz_category": "$quiz_details.category",
                "quiz_difficulty": "$quiz_details.difficulty"
            }
        },
        {
            "$sort": {
                sortBy: sortOrder
            }
        },
        {
            "$skip": skipping_value
        },
        {
            "$limit": limit
        } 
    ])

    cursor2 = results_collection.aggregate([
        {
            '$match': {
                'user_id': user_id
            }
        }, {
            '$group': {
                '_id': None, 
                'total_attempts': {
                    '$sum': 1
                }
            }
        }
    ])

    final_result = list(cursor)
    total_attempts = list(cursor2)
    if not final_result:
        return {"message": "this user has no attempts on this page"}

    for i in range(len(final_result)):
        final_result[i]['_id'] = str(final_result[i]['_id'])
        final_result[i]['user_id'] = str(final_result[i]['user_id'])
        final_result[i]['quiz_id'] = str(final_result[i]['quiz_id'])

    return {"result": final_result, 'total_attempts': total_attempts[0]['total_attempts']}


# AUTHORIZED
@router.get("/users/{user_id}/performance-over-time")
def get_user_performance_over_time(
    user_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        user_id = ObjectId(user_id)
    except bson.errors.InvalidId:
        raise invalid_id_exception

    cursor = results_collection.aggregate([
        {
            '$match': {
                'user_id': user_id
            }
        },
        {
            '$setWindowFields': {
                'sortBy': { 'started_at': 1 }, 
                'output': {
                    'previous_percentage': {
                        '$shift': {
                            'output': '$percentage', 
                            'by': -1, 
                            'default': None
                        }
                    }
                }
            }
        },
        {
            '$project': {
                'percentage': '$percentage', 
                'previous_percentage': '$previous_percentage', 
                'percentage_growth': {
                    '$cond': {
                        'if': {
                            '$or': [
                                {
                                    '$eq': [
                                        '$previous_percentage', None
                                    ]
                                }, {
                                    '$eq': [
                                        '$previous_percentage', 0
                                    ]
                                }
                            ]
                        }, 
                        'then': None, 
                        'else': {
                            '$multiply': [
                                {
                                    '$divide': [
                                        { '$subtract': ['$percentage', '$previous_percentage'] },
                                        '$previous_percentage'
                                    ]
                                }, 100
                            ]
                        }
                    }
                }
            }
        }
    ])
    
    final_result = list(cursor)

    for i in range(len(final_result)):
        final_result[i]['_id'] = str(final_result[i]['_id'])

    return final_result
