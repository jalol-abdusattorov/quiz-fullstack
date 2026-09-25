import bson
from bson import ObjectId
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status

from mongodb import *
from routes.route_utils import swagger_bearer_scheme


router = APIRouter()
invalid_id_exception = HTTPException(status_code=400, detail="invalid id")


# AUTHORIZED
@router.get("/results/{result_id}")
def get_result(
    result_id: str,
    request: Request,
    _: Annotated[str, Depends(swagger_bearer_scheme)]
):
    try:
        result_id = ObjectId(result_id)
    except bson.errors.InvalidId:
        raise invalid_id_exception

    final_result = results_collection.find_one({ "_id": result_id })

    if not final_result:
        return

    final_result['_id'] = str(final_result['_id'])
    final_result['user_id'] = str(final_result['user_id'])
    final_result['quiz_id'] = str(final_result['quiz_id'])
    for i in range(len(final_result['answers'])):
        final_result['answers'][i]['question_id'] = str(final_result['answers'][i]['question_id'])

    return final_result
