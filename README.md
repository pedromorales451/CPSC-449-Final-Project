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
In the terminal, a hyper link with: 
```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) 
```
should appear. Hover over the http link and follow the link to view the application.

In the terminal, a hyper link with "Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)" should appear. Hover over the http link and follow the link to view the application.


