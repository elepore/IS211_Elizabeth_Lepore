from flask import Flask, session, redirect, url_for, request, render_template, flash
import sqlite3
import requests
from datetime import timedelta
import os 
print(os.getcwd())
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=30)
app.secret_key = os.urandom(16)  # Set a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

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

    # Code to fetch book details using book_id and add it to the user's catalogue

    return 'Book added successfully'

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        isbn = request.form['isbn']
        book_details = get_book_details(isbn)

        if book_details:
            conn = sqlite3.connect('books.db')
            c = conn.cursor()
            c.execute("INSERT INTO books (user_id, isbn, title, author, page_count, average_rating, thumbnail) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (session['user_id'], isbn, book_details['title'], book_details['authors'], book_details['page_count'], book_details['average_rating'], book_details['thumbnail']))
            conn.commit()
            conn.close()
            return 'Book added successfully'
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

    book_list = '<ul>'
    for book in books:
       book_list += '<li>' + books["title"] + ' by ' + books["authors"] + ' - <a href="/add_from_search/' + str(book['id']) + '">Add to Catalogue</a></li>'
    book_list += '</ul>'

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
            book_list = '<ul>'
            for book in books:
                book_info = parse_book_data(book)  # Assuming parse_book_data function is already defined
                book_list += '<li>' + book_info["title"] + ' by ' + book_info["authors"] + ' - <a href="/add_from_search/' + str(book['id']) + '">Add to Catalogue</a></li>'
            book_list += '</ul>'
            return book_list
        else:
            return 'Failed to fetch books'
    
    return '''
        <form method="post">
            Title: <input type="text" name="title"><br>
            <input type="submit" value="Search">
        </form>
    '''

def get_book_details(isbn):
    try:
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        return parse_book_data(data)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

def parse_book_data(data):
    if 'items' in data:
        book = data['items'][0]  # Assuming the first item is the desired one
        title = book['volumeInfo']['title']
        authors = ', '.join(book['volumeInfo'].get('authors', 'Unknown'))
        page_count = book['volumeInfo'].get('pageCount', 0)
        average_rating = book['volumeInfo'].get('averageRating', 0)
        thumbnail = book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else None

        return {
            'title': title,
            'authors': authors,
            'page_count': page_count,
            'average_rating': average_rating,
            'thumbnail': thumbnail
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
