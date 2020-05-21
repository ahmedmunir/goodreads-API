import os
import csv

from flask import Flask, session
from sqlalchemy import create_engine
from sqlalchemy.sql import text


app = Flask(__name__)

#check for environment variable first

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("Database URL has not been submited")

#connect DATABASE with PostgreSQL database on Heroku
engine = create_engine(os.getenv("DATABASE_URL"))

#create table of users
engine.execute(text('''CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL )'''))

# #create table of books
engine.execute(text('''CREATE TABLE books(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
)'''))

# #create table of reviews
engine.execute(text('''CREATE TABLE reviews(
    id SERIAL PRIMARY KEY,
    rate INTEGER NOT NULL,
    text VARCHAR NOT NULL,
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users
)'''))


print("Successful Created Tables")

# #read csv file

F = open("books.csv") 
 
file_reader = csv.reader(F)

#move to the next row at CSV to avoid titles
next(file_reader)

statement = text("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)")

for isbn, title, author, year in file_reader:
    engine.execute(statement, {"isbn": isbn, "title": title, "author": author, "year": int(year)})

print("Successful Inserted Data")