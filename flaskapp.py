from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash

import pymysql
import creds 

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def hello():
    return '<h1>Hello from Flask!</h1>'

def get_conn():
    conn = pymysql.connect(
        host= creds.host,
        user= creds.user, 
        password = creds.rds_password,
        db=creds.db,
        )
    return conn

def execute_query(query, args=()):
    cur = get_conn().cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

# Asked ChatGPT to make a cool display for my table
def display_html(rows):
    html = """
    <html>
    <head>
        <style>
            body {
                font-family: 'Segoe UI', 'Roboto', 'Courier New', monospace;
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
                <tr><th>City</th><th>Country Code</th><th>District</th></tr>
    """

    for r in rows:
        html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"

    html += """
        </table>
    </body>
    </html>
    """
    return html

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT city.name as Name, city.countrycode as Code, city.district as District
                FROM city
                Order by city.Name asc
                Limit 10""")
    return display_html(rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)