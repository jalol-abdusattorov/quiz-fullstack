import re

import bson
from bson import ObjectId
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from datetime import datetime as dt, timedelta, timezone

from mongodb import *
from models import *
from routes.route_utils import swagger_bearer_scheme, check_valid_quiz, update_quiz_json_file_after_starting, find_errors_and_get_score_after_submitting
from utils import random_id

router = APIRouter()

page_exception = HTTPException(status_code=400, detail="page should be greater than 0")
invalid_id_exception = HTTPException(status_code=400, detail="invalid id")
quiz_not_found_exception = HTTPException(status_code=404, detail="quiz not found")
permission_denied_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="permission denied")

# AUTHORIZED AND ADMIN
@router.post("/quizzes")
def create_quiz(
    quiz: Quiz,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if not request.state.admin:
        raise permission_denied_exception

    check_valid_quiz(quiz)

    new_quiz = {
        "title": quiz.title,
        "description": quiz.description,
        "category": quiz.category,
        "difficulty": quiz.difficulty,
        "question_ids": quiz.question_ids,
        "time_limit": quiz.time_limit,
        "created_at": dt.now()
    }

    quiz_id = quizzes_collection.insert_one(new_quiz).inserted_id
    return {"quiz_id": str(quiz_id)}


# AUTHORIZED
@router.get("/quizzes/get-all-quizzes/{page}")
def get_quizzes(
    page: int,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if page <= 0: raise page_exception

    skipping_pages = (page - 1) * 10
    limit = 10

    page_quizzes = quizzes_collection.find({}).skip(skipping_pages).limit(limit)

    # avoid return the ObjectId at all cost
    quizzes = []
    for quiz in page_quizzes:
        quiz["_id"] = str(quiz["_id"])
        quiz['question_ids'] = [str(question_id) for question_id in quiz['question_ids']]

        quizzes.append(quiz)

    if not quizzes:
        return {"message": "this page is empty"}

    return {"quizzes": quizzes}


# AUTHORIZED
@router.get("/quizzes/{quiz_id}")
def get_quiz(
    quiz_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        quiz_id = ObjectId(quiz_id)
        quiz = quizzes_collection.find_one({ "_id": quiz_id })
        
        if not quiz:
            raise quiz_not_found_exception

        # avoid returning the ObjectId here too
        quiz['_id'] = str(quiz['_id'])
        quiz["question_ids"] = [str(question_id) for question_id in quiz['question_ids']]

        return quiz

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED AND ADMIN
@router.delete("/quizzes/{quiz_id}")
def delete_quiz(
    quiz_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if not request.state.admin:
        raise permission_denied_exception

    try:
        quiz_id = ObjectId(quiz_id)
        result = quizzes_collection.delete_one({ "_id": quiz_id })

        if result.deleted_count == 0:
            raise quiz_not_found_exception

        return {
            "message": "deleted succesfuly",
            "quiz_id": str(quiz_id)
        }

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.post("/quizzes/{quiz_id}/start")
def start_quiz(
    quiz_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        quiz_id = ObjectId(quiz_id)

        if not quizzes_collection.find_one({ "_id": quiz_id }):
            raise quiz_not_found_exception

        _id = random_id()

        update_quiz_json_file_after_starting(_id, str(quiz_id))

        return {
                "attempt_id": _id,
                "quiz_id": str(quiz_id),
                "started_at": dt.now()
        }

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.post("/quizzes/{quiz_id}/submit")
def submit_quiz(
    quiz_id: str, 
    request: SubmitRequest,
    _request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        quiz_id = ObjectId(quiz_id)

        quiz = quizzes_collection.find_one({ "_id": quiz_id })
        user = users_collection.find_one({ "email": _request.state.user['sub'] })

        if not quiz: raise quiz_not_found_exception
        if not user: raise HTTPException(status_code=404, detail="user not found")

        answers, score, quiz_json_started_at = find_errors_and_get_score_after_submitting(request, quiz)

        started_at = dt.strptime(quiz_json_started_at, "%Y-%m-%d %H:%M:%S")
        completed_at = dt.now()
        time_taken = completed_at - started_at
        time_taken = int(time_taken.total_seconds())

        total = len(quiz['question_ids'])
        new_result = {
            "user_id": user['_id'],
            "quiz_id": quiz_id,

            "answers": answers,

            "score": score,
            "total_questions": total,
            "percentage": score / total * 100,

            "started_at": started_at,
            "completed_at": completed_at,
            "time_taken": time_taken
        }

        results_collection.insert_one(new_result)
        # avoid returning ObjectId, and dont return answers as it can get large
        for popping_value in ["_id", "user_id", "quiz_id", "answers"]:
            new_result.pop(popping_value)

        return new_result
    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED  
@router.get("/quizzes/{quiz_id}/leaderboard/{page}")
def get_quiz_leaderboard(
    quiz_id: str,
    page: int,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        quiz_id = ObjectId(quiz_id)
        
        if not quizzes_collection.find_one({ "_id": quiz_id }):
            raise quiz_not_found_exception

        if page <= 0:
            raise page_exception

        skipping_value = (page - 1) * 10
        limit = 10

        result = results_collection.aggregate([
            {
                "$match": {
                    "quiz_id": quiz_id
                }
            },
            {
                "$sort": {
                    "score": 1
                }
            },
            {
                "$lookup": {
                    "from":         "users",
                    "localField":   "user_id",
                    "foreignField": "_id",
                    "as":           "user_details"
                }
            },
            {
                "$unwind": {
                    "path": "$user_details"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "username": "$user_details.username",
                    "score": "$score",
                    "percentage": "$percentage"
                }
            },
            {
                "$group": {
                    "_id": "$username",
                    "score": {
                        "$max": "$score"
                    },
                    "percentage": {
                        "$first": "$percentage"
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
        
        if not final_result and page == 1:
            return {'message': "this quiz haven't been tried yet"}
        elif not final_result and page != 1:
            return {'message': 'this quiz has no statistics on this page'}

        return {'results': final_result}

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED AND ADMIN
@router.get('/quizzes/{quiz_id}/statistics')
def get_quiz_statistics(
    quiz_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if not request.state.admin:
        raise permission_denied_exception

    try:
        quiz_id = ObjectId(quiz_id)
        
        if not quizzes_collection.find_one({ "_id": quiz_id }):
            raise quiz_not_found_exception

        result = results_collection.aggregate([
            {
                "$match": {
                    "quiz_id": quiz_id
                }
            },
            {
                "$group": {
                    "_id": None,
                    "attempts": {
                        "$sum": 1
                    },
                    "average_score": {
                        "$avg": "$score"
                    },
                    "average_percentage": {
                        "$avg": "$percentage"
                    },
                    "highest_score": {
                        "$max": "$score"
                    },
                    "lowest_score": {
                        "$min": "$score"
                    }
                }
            }
        ])

        final_result = list(result)

        if not final_result:
            return {'message': "this quiz haven't been tried yet or invalid id"}

        final_result[0].pop("_id")

        return {"results": final_result[0]}

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.get("/quizzes/{quiz_id}/attempts-by-score")
def get_number_of_attempts_by_score(
    quiz_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        quiz_id = ObjectId(quiz_id)

        if not quizzes_collection.find_one({ "_id": quiz_id }):
            raise quiz_not_found_exception

        result = results_collection.aggregate([
            {
                "$match": {
                    "quiz_id": quiz_id
                }
            },
            {
                "$group": {
                    "_id": "$percentage",
                    "attempts": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "_id": -1
                }
            }
        ])
        
        final_result = list(result)

        if not final_result:
            return {'message': "this quiz haven't been tried yet"}

        
        return {"results": final_result}

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.get("/quizzes/{quiz_id}/leaderboard-rankings/{page}")
def get_quiz_leaderboard_rankings(
    quiz_id: str,
    page: int,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        quiz_id = ObjectId(quiz_id)

        if not quizzes_collection.find_one({ "_id": quiz_id }):
            raise quiz_not_found_exception

        if page <= 0:
            raise page_exception

        skipping_value = (page - 1) * 10
        limit = 10

        result = results_collection.aggregate([
            {
                "$match": {
                    "quiz_id": quiz_id
                }
            },
            {
                "$lookup": {
                    "from":         "users",
                    "localField":   "user_id",
                    "foreignField": "_id",
                    "as":           "user_details"
                }
            },
            {
                "$unwind": {
                    "path": "$user_details"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "username": "$user_details.username",
                    "percentage": "$percentage"
                }
            },
            {
                "$group": {
                    "_id": "$username",
                    "percentage": {
                        "$first": "$percentage"
                    }
                }
            },
            {
                "$setWindowFields": {
                    "sortBy": { "percentage": -1 },
                    "output": {
                        "leaderboard_rank": {
                            "$denseRank": {}
                        }
                    }
                }
            },
            {
                "$sort": {
                    "leaderboard_rank": 1
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

        if not final_result and page == 1:
            return {'message': "this quiz haven't been tried yet"}
        elif not final_result and page != 1:
            return {'message': 'this quiz has no statistics on this page'}
        
        return {"results": final_result}

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.get("/quizzes/{quiz_id}/dashboard")
def get_quiz_dashboard(
    quiz_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        quiz_id = ObjectId(quiz_id)

        quiz = quizzes_collection.find_one({ "_id": quiz_id })
        if not quiz:
            raise quiz_not_found_exception

        result = results_collection.aggregate([
            {
                '$match': {
                    'quiz_id': quiz_id
                }
            },
            {
                '$facet': {
                    'statistics': [
                        {
                            '$lookup': {
                                'from': 'quizzes', 
                                'localField': 'quiz_id', 
                                'foreignField': '_id', 
                                'as': 'quiz'
                            }
                        },
                        {
                            '$unwind': { 'path': '$quiz' }
                        },
                        {
                            '$group': {
                                '_id': None, 
                                'title': {
                                    '$first': '$quiz.title'
                                }, 
                                'attempts': {
                                    '$sum': 1
                                }, 
                                'average_score': {
                                    '$avg': '$score'
                                }, 
                                'average_percentage': {
                                    '$avg': '$percentage'
                                }, 
                                'highest_score': {
                                    '$max': '$score'
                                }
                            }
                        }
                    ],
                    'score_distribution': [
                        {
                            '$bucket': {
                                'groupBy': '$percentage',
                                'boundaries': [ 0, 21, 41, 61, 81, 101 ], 
                                'default': 'Other', 
                                'output': {
                                    'count': {
                                        '$sum': 1
                                    }
                                }
                            }
                        }
                    ], 
                    'leaderboard': [
                        {
                            '$group': {
                                '_id': '$user_id', 
                                'percentage': {
                                    '$max': '$percentage'
                                }
                            }
                        },
                        {
                            '$setWindowFields': {
                                'sortBy': { 'percentage': -1 }, 
                                'output': {
                                    'percentage_rank': {
                                        '$denseRank': {}
                                    }
                                }
                            }
                        },
                        {
                            '$limit': 10
                        },
                        {
                            '$project': {
                                '_id': { '$toString': '$_id' }, 
                                'percentage': '$percentage', 
                                'percentage_rank': '$percentage_rank'
                            }
                        }
                    ],
                    'questions': [
                        {
                            '$lookup': {
                                'from': 'questions', 
                                'localField': 'answers.question_id', 
                                'foreignField': '_id', 
                                'as': 'questions'
                            }
                        },
                        {
                            '$group': {
                                '_id': '$questions.difficulty', 
                                'question_ids': {
                                    '$first': '$answers.question_id'
                                }
                            }
                        }
                    ]
                }
            },
            {
                '$unwind': {
                    'path': '$questions'
                }
            },
            {
                '$project': {
                    'statistics': {
                        '$arrayElemAt': [
                            '$statistics', 0
                        ]
                    },
                    'score_distribution': {
                        '$arrayToObject': {
                            '$map': {
                                'input': '$score_distribution', 
                                'as': 'item', 
                                'in': {
                                    'k': {
                                        '$switch': {
                                            'branches': [
                                                {
                                                    'case': { '$eq': [ '$$item._id', 0 ] }, 
                                                    'then': '0-20'
                                                },
                                                {
                                                    'case': { '$eq': [ '$$item._id', 21 ] }, 
                                                    'then': '21-40'
                                                },
                                                {
                                                    'case': { '$eq': [ '$$item._id', 41 ] }, 
                                                    'then': '41-60'
                                                },
                                                {
                                                    'case': { '$eq': [ '$$item._id', 61 ] }, 
                                                    'then': '61-80'
                                                },
                                                {
                                                    'case': { '$eq': [ '$$item._id', 81 ] }, 
                                                    'then': '81-100'
                                                }
                                            ], 
                                            'default': 'Other'
                                        }
                                    },
                                    'v': '$$item.count'
                                }
                            }
                        }
                    }, 
                    'top_users': '$leaderboard', 
                    'questions': '$questions'
                }
            },
            {
                '$addFields': {
                    'questions': {
                        '$map': {
                            'input': {
                                '$range': [
                                    0, {
                                        '$size': '$questions.question_ids'
                                    }
                                ]
                            }, 
                            'as': 'idx', 
                            'in': {
                                'question_id': {
                                    '$toString': {
                                        '$arrayElemAt': [ '$questions.question_ids', '$$idx' ]
                                    }
                                }, 
                                'difficulty': {
                                    '$arrayElemAt': [ '$questions._id', '$$idx' ]
                                }
                            }
                        }
                    }
                }
            }
        ])

        final_result = list(result)

        if not final_result:
            return {'message': "this quiz haven't been tried yet or invalid id"}

        final_result.insert(0, { "quiz": { "title": quiz["title"] } })

        return {"results": final_result}


    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.get("/questions/{quiz_id}/hardest-questions/{page}")
def get_quiz_hardest_questions(
    quiz_id: str,
    page: int,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        quiz_id = ObjectId(quiz_id)

        if not quizzes_collection.find_one({ "_id": quiz_id }):
            raise quiz_not_found_exception

        if page <= 0:
            raise page_exception

        skipping_value = (page - 1) * 10
        limit = 10

        result = results_collection.aggregate([
            {
                '$match': {
                    'quiz_id': quiz_id
                }
            },
            {
                '$unwind': {
                    'path': '$answers'
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
                                1,
                                0
                            ]
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 0, 
                    'question_id': { "$toString": '$_id' }, 
                    'accuracy': {
                        "$round": [
                            {
                                '$multiply': [
                                    { '$divide': [ '$correct', '$times_answered' ] },
                                    100
                                ] 
                            },
                            2
                        ]
                    }
                }
            },
            {
                '$sort': {
                    'accuracy': 1
                }
            },
            {
                "$skip": skipping_value
            },
            {
                '$limit': limit
            }
        ])

        final_result = list(result)

        if not final_result and page == 1:
            return {'message': "this quiz haven't been tried yet"}
        elif not final_result and page != 1:
            return {'message': 'this quiz has no statistics on this page'}

        return {"result": final_result}

    except bson.errors.InvalidId:
        raise invalid_id_exception


# AUTHORIZED
@router.get("/quizzes/popular/{page}")
def get_popular_quizzes(
    page: int,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if page <= 0:
        raise page_exception

    skipping_value = (page - 1) * 10
    limit = 10

    time_threshold = dt.now(timezone.utc) - timedelta(days=7)
    result = results_collection.aggregate([
        {
            "$match": {
                "completed_at": {
                    "$gte": time_threshold
                }
            }
        },
        {
            '$group': {
                '_id': '$quiz_id', 
                'play_count': {
                    '$sum': 1
                }
            }
        },
        {
            '$sort': { 'play_count': -1 }
        },
        {
            "$skip": skipping_value
        },
        {
            "$limit": limit
        },
        {
            '$lookup': {
                'from':         'quizzes', 
                'localField':   '_id', 
                'foreignField': '_id', 
                'as':           'quiz_details'
            }
        },
        {
            '$unwind': { 'path': '$quiz_details' }
        }
    ])

    final_result = list(result)

    for doc in final_result:
        doc['_id'] = str(doc['_id'])
        doc['quiz_details']['_id'] = str(doc['quiz_details']['_id'])

        for i in range(len(doc['quiz_details']['question_ids'])):
            doc['quiz_details']['question_ids'][i] = str(doc['quiz_details']['question_ids'][i])

    return {"result": final_result}


# AUTHORIZED
@router.get("/quizzes/category/{category}/{page}")
def get_quizzes_by_category(
    category: str,
    page: int,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if page < 1:
        return page_exception

    skipping_value = (page - 1) * 10
    limit = 10

    cursor = quizzes_collection.aggregate([
        {
            '$match': {
                'category': category
            }
        },
        {
            '$skip': skipping_value
        },
        {
            '$limit': limit
        }
    ])

    result = list(cursor)

    for doc in result:
        doc['_id'] = str(doc['_id'])
        for i in range(len(doc['question_ids'])):
            doc['question_ids'][i] = str(doc['question_ids'][i])

    return {"result": result}


# AUTHORIZED
@router.get("/quizzes")
def get_quizzes(
    req: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)],
    category: str,
    difficulty: str,
    sorting_by: str,
    sorting_order: str,
    page: int,
):
    if page < 1:
        raise page_exception

    if difficulty not in ['all', 'easy', 'medium', 'hard']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="difficulty should be all, easy, medium or hard")

    sorting_order = 1 if sorting_order == "ascending" else -1

    categoryFilter = {} if category == "all" else { "category": category }
    difficultyFilter = {} if difficulty == "all" else { "difficulty": difficulty }
    sort = { sorting_by: sorting_order }

    skipping_val = (page - 1) * 10
    limit = 10

    cursor = quizzes_collection.aggregate([
        {
            "$match": categoryFilter
        },
        {
            "$match": difficultyFilter
        },
        {
            "$sort": sort
        },
        {
            "$skip": skipping_val
        },
        {
            "$limit": limit
        }
    ])

    final_result = list(cursor)
    
    for i in range(len(final_result)):
        final_result[i]['_id'] = str(final_result[i]['_id'])

        for j in range(len(final_result[i]['question_ids'])):
            final_result[i]['question_ids'][j] = str(final_result[i]['question_ids'][j])

    return {"result": final_result}


# AUTHORIZED
@router.get("/quizzes/search/{page}")
def search_quizzes_by(
    search_by: str,
    search: str,
    page: int,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if search_by not in ['title', 'description', 'category', 'difficulty']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid search")

    safe_target = re.escape(search)

    skipping_val = (page - 1) * 10
    limit = 10

    search = search.strip()
    if len(search) == 0:
        cursor = quizzes_collection.find({}).skip(skipping_val).limit(limit)
    else:
        cursor = quizzes_collection.aggregate([
            {
                "$match": {
                    f"{search_by}": {
                        "$regex": safe_target,
                        "$options": "i"
                    }
                }
            },
            {
                "$skip": skipping_val
            },
            {
                "$limit": limit
            }
        ])

    final_result = list(cursor)
    if not final_result:
        return {'message': f'doesnt match any {search_by}'}

    for i in range(len(final_result)):
        final_result[i]['_id'] = str(final_result[i]['_id'])

        for j in range(len(final_result[i]["question_ids"])):
            final_result[i]['question_ids'][j] = str(final_result[i]['question_ids'][j])

    return final_result


# AUTHORIZED
@router.get("/quizzes/{quiz_id}/questions")
def get_quiz_questions(
    quiz_id: str,
    req: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        quiz_id = ObjectId(quiz_id)

        cursor = quizzes_collection.aggregate([
            {
                '$match': {
                    '_id': quiz_id
                }
            },
            {
                '$lookup': {
                    'from':         'questions', 
                    'localField':   'question_ids', 
                    'foreignField': '_id', 
                    'as':           'questions'
                }
            },
            {
                '$unwind': { 'path': '$questions' }
            },
            {
                '$group': {
                    '_id': '$questions._id', 
                    'question': {
                        '$first': '$questions.question'
                    }, 
                    'options': {
                        '$first': '$questions.options'
                    }, 
                    'category': {
                        '$first': '$questions.category'
                    }, 
                    'difficulty': {
                        '$first': '$questions.difficulty'
                    }
                }
            }
        ])
        
        final_result = list(cursor)
        for i in range(len(final_result)):
            final_result[i]['_id'] = str(final_result[i]['_id'])

        return final_result
    except:
        return invalid_id_exception
