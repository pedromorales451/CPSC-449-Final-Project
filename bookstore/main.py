from typing import List, Optional
from fastapi import Body, FastAPI, Path, Form, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pymongo import MongoClient
from pymongo.collection import Collection
from bson import BSON, ObjectId
from bson.son import SON
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
    price: float = Field(..., ge=0)  # Non-negative constraint
    stock: int = Field(..., ge=0)   # Non-negative constraint
    numberOfSales: int = Field(..., ge=0)   # Non-negative constraint
    book_id: int = Field(..., ge=0)     # Non-negative constraint
 
class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)  # Non-negative constraint
    stock: Optional[int] = Field(None, ge=0)   # Non-negative constraint
    numberOfSales: Optional[int] = Field(None, ge=0)   # Non-negative constraint

@app.get("/")
async def index():
    return FileResponse(os.path.join(static_folder, "home.html"))

#●	GET /books: Retrieves a list of all books in the store
@app.get("/books")
async def books() -> List[Book]:
    result = await collection.find().to_list(length=100)
    print(result)
        
    return result

#●	GET /books/total: The total number of books in the store
@app.get("/books/total")
async def get_total_books():
    pipeline = [
        SON({"$count": "totalBooks"})
    ]
    result = await collection.aggregate(pipeline).to_list(length=1)
    return result[0] if result else {"totalBooks": 0}

#●	GET /books/bestsellers: Top 5 bestselling books
@app.get("/books/bestsellers")
async def get_bestsellers():
    try:
        pipeline = [
            {"$sort": {"numberOfSales": -1}},
            {"$limit": 5}
        ]
        result = await collection.aggregate(pipeline).to_list(length=5)

        # ObjectId is not iterable so convert it to a string
        for book in result:
            book["_id"] = str(book["_id"])
        return result
    except Exception as e:
        print("Error retrieving bestsellers:", str(e))
        return {"error": "An error occurred while retrieving bestsellers"}

#●	GET /books/top-authors: Top 5 authors with the most books in the store
@app.get("/books/top-authors")
async def get_top_authors():
    pipeline = [
        SON({
            "$group": {
                "_id": "$author",
                "bookCount": {"$sum": 1}
            }
        }),
        SON({"$sort": {"bookCount": -1}}),
        SON({"$limit": 5})
    ]
    result = await collection.aggregate(pipeline).to_list(length=5)
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
        # check if a book with book_id already exists
        duplicate_result = await collection.find_one({"book_id": book.book_id})

        # book already exists, raise error
        if duplicate_result: 
            raise DuplicateKeyError("Duplicate key error!")
        
        result = await collection.insert_one(dict(book))

        # return the inserted object id 
        return {"inserted_id": str(result.inserted_id)}
    except DuplicateKeyError:
        return {"error": "Duplicate key error!"}
    except Exception as e:
        return {"error": "Please fix any negative input!"}

#●	POST /create-book/form: Adds a new book to the store using create.html form
@app.post("/create-book/form")
async def create_book_form(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    numberOfSales: int = Form(...),
    book_id: int = Form(...)
):
    try:
        try:
            book = Book(
                title=title,
                author=author,
                description=description,
                price=price,
                stock=stock,
                numberOfSales=numberOfSales,
                book_id=book_id
            )
        except:
            return {"error": "Please ensure price, stock, and numberOfSales are non-negative!"}

        # check if a book with book_id already exists
        duplicate_result = await collection.find_one({"book_id": book.book_id})

        # book already exists, raise error
        if duplicate_result: 
            raise DuplicateKeyError("Duplicate key error!")
        
        
        # perform insert_one() asynchronously, 
        # convert book to dict before insertion
        result = await collection.insert_one(dict(book))
        
        # return the inserted object id 
        return {"inserted_id": str(result.inserted_id)}
    except DuplicateKeyError:
        return {"error": "Duplicate key error!"}
    
#●	GET /create-book/: Redirects to create.html  
@app.get("/create-book/")
async def create_book():
    return FileResponse(os.path.join(static_folder, "create.html"))

#   PUT /books/{book_id}: Updates an existing book by ID
@app.put("/books/{book_id}")
async def update_book(book_id:int, book: UpdateBook):
    # check if a book with book_id exists
    find_result = await collection.find_one({"book_id": book_id})

    # book does not exist, raise error
    if find_result == None: 
        return {"Error": "Book does not exist!"}
    
    # dict to store modified data
    updated_data = {}

    # if the field value != None, add the field and its value to updated_data
    if book.title != None:
        updated_data['title'] = book.title 

    if book.author != None:
        updated_data['author'] = book.author 

    if book.description != None:
        updated_data['description'] = book.description 
        
    if book.price != None:
        updated_data['price'] = book.price 

    if book.stock != None:
        updated_data['stock'] = book.stock 

    if book.numberOfSales != None:
        updated_data['numberOfSales'] = book.numberOfSales 
    
    # update the book with the new values
    result = await collection.update_one({'book_id': book_id}, {'$set': updated_data})

    # return the number of books modified by update_one()
    return {"Modified": result.modified_count}

#●	DELETE /books/{book_id}: Deletes a book from the store by ID
@app.delete("/books/delete/{book_id}")
async def delete_book(book_id:int):
    result = await collection.delete_one({"book_id": book_id})

    # Book was not found, therefore not deleted 
    if result.deleted_count == 0:
        return {"error" : "Book not found!"}

    return {"Deleted": book_id}

#●	GET /search?title=<title_input>&author=<author_input>&min_price=<min_input>&max_price=<max_input>: Searches for books by title, author, and price range
@app.get("/search")
async def search_books(request: Request):
    title = request.query_params.get("title")
    author = request.query_params.get("author")
    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")

    query = {}

    if title:
        query["title"] = title

    if author:
        query["author"] = author

    if min_price is not None and max_price is not None:
        query["price"] = {"$gte": float(min_price), "$lte": float(max_price)}
    elif min_price is not None:
        query["price"] = {"$gte": float(min_price)}
    elif max_price is not None:
        query["price"] = {"$lte": float(max_price)}

    result = await collection.find(query).to_list(length=100)

    # ObjectId is not iterable so convert it to a string
    for book in result:
        book["_id"] = str(book["_id"])

    return result

# Serve the book_search.html file
@app.get("/book-search")
async def book_search():
    return FileResponse(os.path.join(static_folder, "search.html"))
