# CS50 Web programming using Python and Javascript Course (Project 1).

# Books Project 1

This is a book website which help user to add review about books they read, and read the views added by other readers.
It's also provide API to help other developers get data about specific book and use it inside their application.

# Demo:
![Alt Text](https://media.giphy.com/media/dVj2YbtzU61Tx4FFAY/giphy.gif)

# Technologies:
1. python 3.6
2. Flask 1.1.1
3. SQL.
4. werkzeug 0.16.0
5. Bootstrap 4
6. HTML & CSS

# Description of project in details:
- This project has main page where you can **register** or **login**.
- Click on register and create new account but the username must be unique.
- Then will be redirected to **Login** page to enter username and password.
- after that will be redirected to **search** page where you can search for book using (ISBN, title or author).
- Results will be displayed and you can choose any book to read reviews about it and add more review.
- According to Project requirements, each user can add just **one review** to a single book.
- There is a Logout button at the top right corner in case user wants to Logout.

# Contents of project files:
- **import.py**: A python code to connect to DB, create tables, schemas and extract data from **books.csv** and insert them inside **books** table.
- **application.py**: The main .py file which has code that handle all back-end code for our project.
- **templates**: has all HTML files (index, login, register, search, results, book_page).
- **static**: has all CSS files to style our project.

# important Note:
I didn't provide my database URL at the project file, i count on that you will add it using:
```
set DATABASE_URL= <url>
```
But **goodreads** API is provided.