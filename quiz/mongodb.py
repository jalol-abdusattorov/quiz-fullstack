from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
db = client.quiz_backend

# importing from here, dont want to make a new collection in every files
users_collection = db.users
quizzes_collection = db.quizzes
questions_collection = db.questions
results_collection = db.results
attempts_collection = db.attempts