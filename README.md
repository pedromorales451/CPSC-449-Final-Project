# Authors
* Matthew Butner

* Kim Eaton

* Pedro Morales

# Installation

* Create a Python Virtual Environment in the root directory.

```python -m venv myenv```

or

```python3 -m venv myenv```

* Activate the virtual environment
```
source myenv/bin/activate
```

* Install dependencies from requirements.txt
```
pip install -r requirements.txt
```

# MongoDB Prerequisites
* create a new database called "bookstore"
* Then, create a new collection called "books"


<p align = "center">
<img width="688" alt="Pasted Graphic" src="https://github.com/pedromorales451/CPSC-449-Final-Project/assets/70175052/8e17a692-7910-41a9-901b-8fa76ff7b199">
</p>
<p align = "center">
Database "bookstore" and collection "books" created with MongoDB Compass
</p>

# Run
Run using uvicorn 
```
uvicorn bookstore.main:app --reload
```
In the terminal, a hyperlink should appear. Hover over the http link and follow the link to view the application.
```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
<img width="688" alt="Pasted Graphic" src="https://github.com/pedromorales451/CPSC-449-Final-Project/blob/main/viewappterminal.png">


## PUT /books/{book_id}
### Postman
1. Create a new HTTP request and set the method to PUT.
2. Set the URL to ```http://127.0.0.1:8000/books/{book_id}``` where {book_id} is the ID of the book to update. 
3. To send a request body, click the "Body" tab, then select the "raw" option, then click on the dropdown menu and select "JSON"
4. Create a JSON object containing the fields you want to update for {book_id}. 
5. Click the "Send" button.

<img width="947" alt="image" src="https://github.com/pedromorales451/CPSC-449-Final-Project/assets/70175052/13810f70-30bd-4950-acaf-3dccc3e64654">

### Response Body
* An error message indicating that the requested book does not exist.
```
{
    "Error": "Book does not exist!"
}
```

* The number of book updates. A value of 1 indicates that the requested book has been updated, while a value of 0 means that no books were updated.
```
{
    "Modified": 1
}
```
