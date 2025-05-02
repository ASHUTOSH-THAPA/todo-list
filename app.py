# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for
import sqlite3  # For database operations

# Initialize the Flask application
app = Flask(__name__)

# Function to create the database table if it doesn't exist
def init_db():
    conn = sqlite3.connect('database.db')  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Create a table named 'todos' if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    
    conn.commit()  # Save changes
    conn.close()  # Close the connection

# Route for the home page (shows and adds todos)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # If form is submitted
        task = request.form.get('task')  # Get the task from the form
        
        if task:  # If task is not empty
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Insert the new task into the database
            cursor.execute('INSERT INTO todos (task) VALUES (?)', (task,))
            
            conn.commit()
            conn.close()
        
        return redirect(url_for('index'))  # Redirect to refresh the page
    
    # For GET requests or after POST redirect
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Get all todos from the database
    cursor.execute('SELECT * FROM todos')
    todos = cursor.fetchall()  # Fetch all rows
    
    conn.close()
    
    # Render the template with the todos data
    return render_template('index.html', todos=todos)

# Route to delete a todo
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Delete the todo with the given id
    cursor.execute('DELETE FROM todos WHERE id = ?', (id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))  # Redirect back to the home page

# Route to update a todo status
@app.route('/update/<int:id>/<status>')
def update(id, status):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Update the status of the todo with the given id
    cursor.execute('UPDATE todos SET status = ? WHERE id = ?', (status, id))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))  # Redirect back to the home page

# Initialize the database when the app starts
init_db()

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True,port=5001)  # debug=True enables auto-reload on code changes