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
    book_id: int


@app.get("/")
async def index():
    return {'greeting': 'Welcome to Bookstore'}

#●	GET /books: Retrieves a list of all books in the store
@app.get("/books")
async def books() -> List[Book]:
    result = await collection.find().to_list(length=100)
        
    return result

#●	GET /books/{book_id}: Retrieves a specific book by ID
@app.get("/books/{book_id}")
async def getbook(book_id: int) -> List[Book]:
    if(book_id >=0 and book_id <=1):
        result = await collection.find({"book_id": book_id}).to_list(length=100)
    else: 
        result={"error": "no book by that id found"}
    return result

#●	POST /books: Adds a new book to the store  
@app.post("/create-book/")
async def create_book(book: Book):
    try:
        # perform insert_one() asynchronously, 
        # convert book to dict before insertion
        result = await db.collection.insert_one(dict(book))

        # return the inserted object id 
        return {"inserted_id": str(result.inserted_id)}
    except DuplicateKeyError:
        return {"error": "Duplicate key error!"}




#●	PUT /books/{book_id}: Updates an existing book by ID
@app.put("/books/{book_id}")
async def update_book(book_id:int)->List[Book]:
    collection.update_one({"book_id": book_id}, {"$set":{"stock":4}})
    result = await collection.find({"book_id": book_id}).to_list(length=100)
    return result

#●	DELETE /books/{book_id}: Deletes a book from the store by ID
#●	GET /search?title={}&author={}&min_price={}&max_price={}: Searches for books by title, author, and price range

@app.get("/search?title={}&author={}&min_price={}&max_price={}: Searches for books by title, author, and price range")
async def search():
    return []