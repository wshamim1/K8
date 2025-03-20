
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'host': 'localhost',  # Change to your MySQL host
    'user': 'root',       # Change to your MySQL username
    'password': 'password',  # Change to your MySQL password
    'database': 'flaskapp'
}

# Route for the home page that shows the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        # Get form data
        user_id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        # Insert record into MySQL
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            sql = "INSERT INTO users (id, firstname, lastname) VALUES (%s, %s, %s)"
            values = (user_id, firstname, lastname)
            cursor.execute(sql, values)
            conn.commit()

            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            return f"Error: {err}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

if __name__ == '__main__':
    app.run(debug=True)

