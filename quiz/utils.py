import json
from random import randint

from fastapi.security import HTTPBearer

def random_id() -> int:
    with open("quiz.json", 'r') as f:
        active_quizzes = json.load(f)

    if len(active_quizzes) >= 900000:
        raise OverflowError("there are no id's to generate")

    while True:
        number = randint(100000, 999999)
        if number not in [active_q['attempt_id'] for active_q in active_quizzes]:
            return number
