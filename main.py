from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# إنشاء قاعدة بيانات لتخزين الأسماء والتوقيعات
def init_db():
    conn = sqlite3.connect("signatures.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signatures (
            id INTEGER PRIMARY KEY,
            name TEXT,
            signature BLOB
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        signature = request.form["signature"]
        
        # حفظ البيانات في قاعدة البيانات
        conn = sqlite3.connect("signatures.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO signatures (name, signature) VALUES (?, ?)", (name, signature))
        conn.commit()
        conn.close()
        
        return redirect(url_for("thank_you"))

    return render_template("index.html")

@app.route("/thank-you")
def thank_you():
    return "شكراً لتوقيعك! تم تسجيل اسمك بنجاح."

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
