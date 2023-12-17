from flask import Flask, session, redirect, url_for, request, render_template, flash
import sqlite3
import requests
from datetime import timedelta
import os 

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=30)
app.secret_key = os.urandom(16)  # Set a random secret key

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In real app, use hashed passwords

        try:
            conn = sqlite3.connect('books.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
            conn.close()

            if user:
                session['username'] = username
                session['user_id'] = user[0]
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password')
        except sqlite3.Error as e:
            flash(str(e))

    return render_template('login.html')

@app.route('/add_from_search/<string:book_id>', methods=['GET'])
def add_from_search(book_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        # Fetch book details from Google Books API
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes/{book_id}')
        if response.status_code != 200:
            flash('Failed to fetch book details')
            return redirect(url_for('search_by_title'))

        book_data = response.json()
        book_info = parse_book_data(book_data)

        # Insert book details into the database
        conn = sqlite3.connect('books.db')
        c = conn.cursor()
        c.execute("INSERT INTO books (user_id, isbn_10, isbn_13, title, author, page_count, average_rating, thumbnail) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (session['user_id'], book_info['isbn_10'], book_info['isbn_13'], book_info['title'], book_info['authors'], book_info['page_count'], book_info['average_rating'], book_info['thumbnail']))
        conn.commit()
        conn.close()

        flash('Book added successfully')
    except requests.exceptions.RequestException as e:
        flash(f'An error occurred while fetching book details: {e}')
    except sqlite3.Error as e:
        flash(f'An error occurred while adding book to the database: {e}')

    return redirect(url_for('view_books'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        isbn = request.form['isbn']
        book_details = get_book_details(isbn)
        print('yes')
        if book_details:
            conn = sqlite3.connect('books.db')
            c = conn.cursor()
            c.execute("INSERT INTO books (user_id, isbn_10, isbn_13, title, author, page_count, average_rating, thumbnail) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (session['user_id'], book_details['isbn_10'], book_details['isbn_13'], book_details['title'], book_details['authors'], book_details['page_count'], book_details['average_rating'], book_details['thumbnail']))
            conn.commit()
            conn.close()
        else:
            return 'Failed to add book'

    return render_template('add_book.html')


@app.route('/view_books')
def view_books():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE user_id=?", (session['user_id'],))
    books = c.fetchall()
    conn.close()

    return render_template('view_catalogue.html', books=books)

@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=? AND user_id=?", (book_id, session['user_id']))
    conn.commit()
    conn.close()

    return redirect(url_for('view_books'))

@app.route('/search_by_title', methods=['GET', 'POST'])
def search_by_title():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=intitle:{title}')
        if response.status_code == 200:
            books = response.json().get('items', [])
            return render_template('search_results.html', books=books)
        else:
            flash('Failed to fetch books')

    return render_template('search_by_title.html')

def get_book_details(isbn):
    try:
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        return parse_book_data(data)
    except requests.exceptions.HTTPError as err:
        flash(f"HTTP error: {err}")
    except requests.exceptions.RequestException as err:
        flash(f"Error: {err}")
    except Exception as err:
        flash(f"An error occurred: {err}")
    return None


def parse_book_data(data):
    if 'items' in data and data['items']:
        print('yes')
        book = data['items'][0]['volumeInfo']

        title = book.get('title', 'No Title')
        authors = ', '.join(book.get('authors', ['Unknown']))
        page_count = book.get('pageCount', 0)
        average_rating = book.get('averageRating', 0)
        thumbnail = book.get('imageLinks', {}).get('thumbnail', '')

        # Extracting ISBN
        industry_identifiers = book.get('industryIdentifiers', [])
        isbn_10 = isbn_13 = ''
        for identifier in industry_identifiers:
            if identifier['type'] == 'ISBN_10':
                isbn_10 = identifier['identifier']
            elif identifier['type'] == 'ISBN_13':
                isbn_13 = identifier['identifier']

        return {
            'title': title,
            'authors': authors,
            'page_count': page_count,
            'average_rating': average_rating,
            'thumbnail': thumbnail,
            'isbn_10': isbn_10,
            'isbn_13': isbn_13
        }
    else:
        return None

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
