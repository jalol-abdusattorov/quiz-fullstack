import os
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)
db = client.quiz_backend

# importing from here, dont want to make a new collection in every files
users_collection = db.users
quizzes_collection = db.quizzes
questions_collection = db.questions
results_collection = db.results
attempts_collection = db.attempts