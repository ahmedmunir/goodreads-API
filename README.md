# Books API Project:
This is [CS50's Web programming with Python and Javascript](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript) project1 - 2018 version.  

This is a book website which help user to add review about books they read, and read the reviews added by other readers.  
It also provides **API** to help other developers get data about specific book and use it inside their application.  

# Demo:
![Alt Text](https://media.giphy.com/media/dVj2YbtzU61Tx4FFAY/giphy.gif)

# Technologies:
1. python 3.6
2. Flask 1.1.1
3. PostgreSQL
4. Bootstrap 4
5. HTML & CSS

# Overview of project:
- This project has main page where you can **register** or **login**.
- Click on register and create new account but the username must be unique.
- Then will be redirected to **Login** page to enter username and password.
- after that will be redirected to **search** page where you can search for book using (ISBN, title or author).
- Results will be displayed and you can choose any book to read reviews about it and add more review.
- According to Project requirements by CS50, each user can add just **one review** to a single book.
- There is a Logout button at the top right corner in case user wants to Logout.

# Installation:
The app depends on 2 sources to get information about books:  
- **books.csv** which has information about 5000 book, so you need to install data from that books.csv into database to be able to search for books.
- [**goodreads API**](https://www.goodreads.com/api) which used to get some additional information about book that found at **books.csv**.  

Get the URL of your database then run:
```bash
export DATABASE_URL="URL of your database"
pip install -r requirements.txt
python import.py #to create tables at Database and insert book.csv data into it
python application.py #to run application locally at: http://localhost:8000
```
