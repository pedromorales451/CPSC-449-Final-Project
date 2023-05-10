# Authors
* Matthew Butner

* Kim Eaton

* Pedro Morales

# Installation

* Create a Python Virtual Environment in the root directory.

```python -m venv myenv```

or

```python3 -m venv myenv```

* Install dependencies from requirements.txt
```pip install -r requirements.txt```

# MongoDB Prerequisites
* create a new database called "bookstore"
* Then, create a new collection called "books"


# Run
Run using uvicorn 
```uvicorn bookstore.main:app --reload```


