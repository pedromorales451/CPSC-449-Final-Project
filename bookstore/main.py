from typing import List
from fastapi import Body, FastAPI, Path, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure
from motor.motor_asyncio import AsyncIOMotorClient
from random import randint
import os

app = FastAPI()

# Get the absolute path of the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Serve static files (e.g., HTML, CSS, JS)
static_folder = os.path.join(base_dir, "static")
app.mount("/static", StaticFiles(directory=static_folder), name="static")

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
    return FileResponse(os.path.join(static_folder, "home.html"))

#●	GET /books: Retrieves a list of all books in the store
@app.get("/books")
async def books() -> List[Book]:
    result = await collection.find().to_list(length=100)
    print(result)
        
    return result

#●	GET /books/{book_id}: Retrieves a specific book by ID
@app.get("/books/{book_id}")
async def getbook(book_id: int) -> List[Book]:
    if(book_id >=0):
        result = await collection.find({"book_id": book_id}).to_list(length=100)
    else: 
        result={"error": "no book by that id found"}
    return result

#●	POST /create-book: Adds a new book to the store  
@app.post("/create-book/")
async def create_book(book: Book):
    try:
        # perform insert_one() asynchronously, 
        # convert book to dict before insertion
        '''result = await db.collection.insert_one(dict(book))''' #(collection.insert_one may suffice)
        result = await collection.insert_one(dict(book))

        # return the inserted object id 
        return {"inserted_id": str(result.inserted_id)}
    except DuplicateKeyError:
        return {"error": "Duplicate key error!"}

#●	POST /create-book/form: Adds a new book to the store using create.html form
@app.post("/create-book/form")
async def create_book_form(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    numberOfSales: int = Form(...)
):
    try:
        book = Book(
            title=title,
            author=author,
            description=description,
            price=price,
            stock=stock,
            numberOfSales=numberOfSales,
            book_id=randint(1000, 9999)
        )

        # perform insert_one() asynchronously, 
        # convert book to dict before insertion
        '''result = await db.collection.insert_one(dict(book))''' #(collection.insert_one may suffice)
        result = await collection.insert_one(dict(book))
        

        # return the inserted object id 
        return {"inserted_id": str(result.inserted_id)}
    except DuplicateKeyError:
        return {"error": "Duplicate key error!"}
    
#●	GET /create-book/: Redirects to create.html  
@app.get("/create-book/")
async def create_book():
    return FileResponse(os.path.join(static_folder, "create.html"))

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