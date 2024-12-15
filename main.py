from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# إنشاء قاعدة بيانات لتخزين الأسماء والتوقيعات
def init_db():
    with sqlite3.connect("signatures.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signatures (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                signature BLOB NOT NULL
            )
        """)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        signature_file = request.files.get("signature")

        # تحقق من إدخال الحقول
        if not name or not signature_file:
            return "الرجاء إدخال الاسم ورفع التوقيع.", 400

        # قراءة ملف التوقيع كـ BLOB
        signature = signature_file.read()

        # حفظ البيانات في قاعدة البيانات
        with sqlite3.connect("signatures.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO signatures (name, signature) VALUES (?, ?)", (name, signature))
            conn.commit()

        return redirect(url_for("thank_you"))

    return render_template("index.html")

@app.route("/thank-you")
def thank_you():
    return "شكراً لتوقيعك! تم تسجيل اسمك بنجاح."

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
