import bson
from bson import ObjectId
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status

from mongodb import *
from routes.route_utils import swagger_bearer_scheme

router = APIRouter()
invalid_id_exception = HTTPException(status_code=400, detail="invalid id")


# AUTHORIZED AND ADMIN
@router.get("/admin/get-dashboard")
def get_result(
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    if not request.state.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="permission denied")

    total_users = len(list(users_collection.find({})))
    total_quizzes = len(list(quizzes_collection.find({})))
    total_questions = len(list(questions_collection.find({})))
    total_attempts = len(list(results_collection.find({})))

    return { "total_users": total_users, "total_quizzes": total_quizzes, "total_questions": total_questions, "total_attempts": total_attempts }