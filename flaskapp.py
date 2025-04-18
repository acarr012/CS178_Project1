from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from dynamo_functions import add_travel_log, get_all_travel_logs
import creds

# Flask App Config
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL/RDS Connection
def get_conn():
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.rds_password,
        db=creds.db,
    )

def execute_query(query, args=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# 🏠 HOME — Full CRUD for DynamoDB
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Create log
        username = request.form['username']
        log_id = request.form['log_id']
        country = request.form['country']
        rating = int(request.form['rating'])

        success, message = add_travel_log(username, log_id, country, rating)
        flash(message)

        return redirect(url_for('home'))

    # Read logs
    logs = get_all_travel_logs()

    html = """
        <h1>Travel Log</h1>

        <h2>Log a New Trip</h2>
        <form method="post">
            Username: <input type="text" name="username"><br>
            Log ID: <input type="text" name="log_id"><br>
            Country: <input type="text" name="country"><br>
            Rating: <input type="number" name="rating"><br>
            <input type="submit" value="Submit">
        </form>

        <h2>Travel Log</h2>
        <ul>
    """
    for item in logs:
        html += f"""
            <li>
                <b>{item['username']}</b> - {item['country']} (Rating: {item['rating']})<br>
            </li>
        """
    html += "</ul>"

    # Link to view the cities
    html += """
        <h2>View Cities to Visit</h2>
        <a href="/viewdb">Click here to view all cities</a>
    """
    return html

# View all the cities from the database
@app.route("/viewdb")
def viewdb():
    rows = execute_query("""
        SELECT city.Name AS City, city.District, country.Name AS Country
        FROM city
        JOIN country ON city.CountryCode = country.Code
        ORDER BY city.Name ASC
    """)
    return display_html(rows)

# Asked ChatGPT to make a cool display for me
def display_html(rows):
    html = """
    <html>
    <head>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                margin: 0;
                padding: 40px 20px;
                background-color: #1e1e2f;
                color: #f1f1f1;
            }
            .container {
                max-width: 960px;
                margin: auto;
            }
            h2 {
                text-align: center;
                color: #00bcd4;
                font-size: 32px;
                margin-bottom: 30px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                background-color: #2a2a3d;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
            }
            th, td {
                padding: 16px;
                text-align: left;
                font-size: 16px;
            }
            th {
                background-color: #00bcd4;
                color: #fff;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            tr:nth-child(even) {
                background-color: #383854;
            }
            tr:hover {
                background-color: #44446a;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Cities (Alphabetical)</h2>
            <table>
                <tr><th>City</th><th>District</th><th>Country</th></tr>
    """
    for r in rows:
        html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    html += """
            </table>
        </div>
    </body>
    </html>
    """
    return html

# Run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)





