import os
import requests

from flask import Flask, session, render_template, redirect, url_for, request, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#MAIN INDEX PAGE
@app.route("/")
def index():
    return render_template("index.html")

#LOGIN ROUTE
@app.route("/login", methods=["POST", "GET"])
def login():
    
    #at GET request
    if request.method == "GET":

        #in case that user is already logged in
        if session.get("user_id"):
            return redirect(url_for('search'))
        
        #in case that user is not logged in
        return render_template("login.html")
    
    #at POST request
    elif request.method == "POST":

        #get information from form
        name = request.form.get("username")
        password = request.form.get("password")

        try:

            #check the validation of username & password
            user = db.execute('SELECT * FROM users WHERE (username=:username) AND (password=:password)',
            {"username": name, "password": password}).fetchone()

            #add user to session
            session["user_id"] = user.id

        except:

            #redirect to login page in case that username or password is wrong
            flash("Wrong username or Password")
            return redirect(url_for('login'))
        
        db.commit()

        #redirect to search page if username and password are right
        flash("Logged in successfully")
        return redirect(url_for('search'))


#REGISTERATION ROUTE
@app.route("/register", methods=["GET", "POST"])
def register():

    #AT GET request
    if request.method == "GET":

        #in case that user is already logged in
        if session.get("user_id"):
            return redirect(url_for('search'))

        #in case that user is not logged in
        return render_template("register.html")

    #AT POST request 
    elif request.method == "POST":

        name = request.form.get("username")
        password = request.form.get("password")

        #add user information into DATABASE
        try:
            db.execute('INSERT INTO users (username, password) VALUES (:username, :password)', 
            {"username": name, "password": password})
        except:
            
            #create Error page in case that username already used
            flash("this username is already used, change it please")
            return redirect(url_for('register'))

        db.commit()

        #redirect to login page in case that account created
        flash('Account created successfully, you can log in now')
        return redirect(url_for('login'))

#SEARCH ROUTE
@app.route('/search', methods = ["GET", "POST"])
def search():
    
    if request.method == "GET":

        #check if user is already logged in or not
        if session.get("user_id"):
            return render_template("search.html")
        else:

            #redirect to login page if user not logged in
            flash("Please log in first")
            return redirect(url_for('login'))
    
    elif request.method == "POST":
        
        try:
            search = request.form.get("search")

            #first search for specific values (suppose that user will provide perfect details)
            results = db.execute('''SELECT * FROM books WHERE isbn=:isbn OR title=:title OR author=:author''',
            {"isbn": search, "title": search, "author": search}).fetchall()

            if results:
                return render_template("results.html", results=results)
            
            #in case that user will just provide part of isbn, title or author
            else:
                results = db.execute("SELECT * FROM books WHERE isbn LIKE CONCAT('%',:a,'%')" \
                "OR isbn LIKE CONCAT('%', :a)" \
                "OR isbn LIKE CONCAT(:a, '%')" \
                "OR title LIKE CONCAT ('%', :b, '%')" \
                "OR title LIKE CONCAT('%', :b)" \
                "OR title LIKE CONCAT(:b, '%')" \
                "OR author LIKE CONCAT ('%', :b, '%')" \
                "OR author LIKE CONCAT('%', :b)" \
                "OR author LIKE CONCAT(:b, '%')", {"a": search, "b": search.capitalize()}).fetchall()

                #in case we found the results
                if results:
                    return render_template("results.html", results=results)
                
                else:

                    #if there are not results, redirect to search page
                    flash("Can't Find Any Result")
                    return redirect(url_for('search'))
        except:
            return "Can't Get Data now (Internal Server Error)", 404

#SEARCH ROUTE FOR SPECIFIC ISBN
@app.route("/search/<isbn>")
def search_book(isbn):

    # make sure that user is already logged in
    if session.get("user_id"):

        #search for results using provided ISBN
        result = db.execute('SELECT * FROM books WHERE isbn=:isbn', {"isbn": isbn}).fetchall()

        #get book ratings count & average ratings for that book
        #API==> key=GeK53LhIZRCMcwG6LJuIkA
        goodreads_rating = requests.get("https://www.goodreads.com/book/review_counts.json",
        params = {'key': 'GeK53LhIZRCMcwG6LJuIkA',
                'isbns': isbn})
        ratings = goodreads_rating.json()['books'][0]['work_ratings_count']
        average_rate = goodreads_rating.json()['books'][0]['average_rating']

        #get reviews from database for that book
        reviews = db.execute("SELECT rate, text, username FROM reviews"\
        " JOIN books ON books.id = reviews.book_id"\
        " JOIN users ON users.id = reviews.user_id"\
        " WHERE books.isbn = :isbn",
        {"isbn": isbn}).fetchall() or []

        return render_template('book_page.html', 
        result=result[0], 
        ratings= ratings, 
        average_rate= average_rate,
        reviews = reviews)
    else:

        #redirect to login page if user not logged in yer
        flash("Please log in first")
        return redirect(url_for('login'))

#SUBMIT A REVIEW TO BOOK
@app.route("/addreview/<book_id>/<isbn>", methods = ["GET", "POST"])
def add_review(book_id, isbn):

    #check that it is POST request
    if request.method == "POST":

        #check if user is already logged in
        if session.get("user_id"):

            #get the rate & text from form
            rate = int(request.form.get("rate"))
            textarea = request.form.get("review")

            #check that the rate is between 1 & 5 & textarea is provided
            if rate > 5 or rate < 1 or textarea == None:
                return "Rate Must be between 1 & 5"
            
            try:

                #extract all reviews by the id of book
                reviews_of_book = db.execute('SELECT * FROM reviews WHERE book_id=:book_id',
                {"book_id": book_id}).fetchall()

                #check if user posted a comment before or not
                for review in reviews_of_book:
                    if int(session["user_id"]) == review.user_id:

                        #redirect to book page with error message
                        flash("Can't Add multiple reviews from the same account")
                        return redirect(url_for('search_book', isbn=isbn))
                
                #add new review to reviews of book
                db.execute('INSERT INTO reviews (rate, text, book_id, user_id) VALUES (:rate, :text, :book_id, :user_id)',
                {"rate": rate, "text": textarea, "book_id": int(book_id), "user_id": int(session["user_id"])})
            except:
                return "Can't add data to datbase", 404

            db.commit()

            #redirect to book-page with successful message about adding new comment
            flash("Review added successfully")
            return redirect(url_for('search_book', isbn=isbn))
        else:

            #redirect to login page if user not logged in
            flash("Please log in first")
            return redirect(url_for('login'))         

#LOGOUT ROUTE
@app.route("/logout")
def logout():

    #delete the session of current user
    del session["user_id"]
    flash("Logout successfully")
    return redirect(url_for('login'))

#API ROUTE
@app.route("/api/<isbn>")
def api(isbn):
    try:

        #get title, author, year and isbn from local database
        our_db = db.execute('SELECT * FROM books WHERE isbn=:isbn', {"isbn": isbn}).fetchone()
        
        #get review_count & average_score from goodreads API
        remote_api = requests.get("https://www.goodreads.com/book/review_counts.json",
        params= {
            "key": "GeK53LhIZRCMcwG6LJuIkA",
            "isbns": isbn
        })

        #return JSON data
        return jsonify({
            "title": our_db.title,
            "author": our_db.author,
            "year": our_db.year,
            "isbn": our_db.isbn,
            "review_count": remote_api.json()['books'][0]['work_reviews_count'],
            "average_score": remote_api.json()['books'][0]['average_rating']
        })
    except:
        return "Wrong isbn number", 404

if __name__=="__main__":
    app.run()