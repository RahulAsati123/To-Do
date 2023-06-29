from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
db_name = "todo.db"

def create_todo_table():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS todo")
    c.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, completed INTEGER)")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM todo")
    items = c.fetchall()
    conn.close()
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO todo (task, completed) VALUES (?, ?)", (task, 0))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("DELETE FROM todo WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    if request.method == "POST":
        task = request.form["task"]
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("UPDATE todo SET task=? WHERE id=?", (task, todo_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    else:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM todo WHERE id=?", (todo_id,))
        item = c.fetchone()
        conn.close()
        return render_template("edit.html", item=item)

@app.route("/complete/<int:todo_id>", methods=["POST"])
def complete(todo_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("UPDATE todo SET completed=? WHERE id=?", (1, todo_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    create_todo_table()
    app.run(debug=True)
