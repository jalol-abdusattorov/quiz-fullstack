from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    email: str = "user@example.com"
    password: str

class Quiz(BaseModel):
    title: str
    description: str
    category: str
    difficulty: str
    question_ids: list[str]
    time_limit: int

class QuestionRequest(BaseModel):
    question: str
    options: list[str] | list[int]
    correct_answer: int
    category: str = "..."
    difficulty: str = "easy"

class SubmitRequest(BaseModel):
    attempt_id: int 
    answers: list[dict] = [{"question_id": "...", "selected_answer": 0}]