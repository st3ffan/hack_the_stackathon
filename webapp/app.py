from flask import Flask, render_template
from database import db

app = Flask(__name__)


@app.route("/")
def index():
    corporations = db.get_corporations()
    return render_template("index.html", corporations=corporations)


if __name__ == "__main__":
    if db.connect():
        try:
            app.run(host="0.0.0.0", port=8080, debug=True)
        finally:
            db.close()
    else:
        print("Failed to connect to database. Exiting.")
