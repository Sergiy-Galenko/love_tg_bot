from pymongo.mongo_client import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # Підключення до локального сервера MongoDB
db = client["telegram_bot"]  # Назва вашої бази даних
users_collection = db["users"]  # Назва колекції користувачів

def save_user(user_id, name, age, city, username):
    user_data = {
        "user_id": user_id,
        "name": name,
        "age": age,
        "city": city,
        "username": username
    }
    users_collection.update_one({"user_id": user_id}, {"$set": user_data}, upsert=True)

def get_users_by_city_and_age(city, min_age, max_age, exclude_user_id):
    query = {
        "city": city,
        "age": {"$gte": min_age, "$lte": max_age},
        "user_id": {"$ne": exclude_user_id}
    }
    return list(users_collection.find(query))
