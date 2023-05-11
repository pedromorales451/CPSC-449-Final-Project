from typing import List
from fastapi import Body, FastAPI, Path
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Initialize MongoDB client
mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo_client["bookstore"]
collection = db["books"]


class Book(BaseModel):
    title: str
    author: str
    description: str
    price: float
    stock: int
    numberOfSales: int

@app.get("/")
def index():
    return {'greeting': 'Welcome to Bookstore'}

@app.get("/books")
async def books() -> List[Book]:
    result = await collection.find().to_list(length=100)
        
    return result


@app.post("/create-book/")
async def create_book(book: Book):
    try:
        # perform insert_one() asynchronously, 
        # convert book to dict before insertion
        result = await collection.insert_one(dict(book))

        # return the inserted object id 
        return {"inserted_id": str(result.inserted_id)}
    except DuplicateKeyError:
        return {"error": "Duplicate key error!"}
