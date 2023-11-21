from flask import Flask, render_template, request, redirect, url_for
import pickle
import re 

app = Flask(__name__)

todo_list = []

@app.route('/')
def view_todo_list():
    return render_template('todo_list.html', todo_list=todo_list)

@app.route('/submit', methods=['POST'])
def submit_todo_item():
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email) or priority not in ['Low', 'Medium', 'High']:
        return redirect(url_for('view_todo_list'))
    todo_list.append({'task': task, 'email': email, 'priority': priority})
    return redirect(url_for('view_todo_list'))


@app.route('/clear', methods=['POST'])
def clear_todo_list():
    todo_list.clear()
    return redirect(url_for('view_todo_list'))

def save_todo_list():
    with open('todo_list.pkl', 'wb') as file:
        pickle.dump(todo_list, file)

def load_todo_list():
    try:
        with open('todo_list.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

todo_list = load_todo_list()

@app.route('/save', methods=['POST'])
def save_list():
    save_todo_list()
    return redirect(url_for('view_todo_list'))

@app.route('/delete/<int:item_index>', methods=['POST'])
def delete_todo_item(item_index):
    if 0 <= item_index < len(todo_list):
        del todo_list[item_index]
    return redirect(url_for('view_todo_list'))

def run_app():
    app.run(debug=True)

if __name__ == '__main__':
    run_app()
