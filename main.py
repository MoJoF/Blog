from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article:
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Article %r>" % self.id

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/news')
def news():
    return render_template("news.html")


if __name__ == '__main__':
    app.run(debug=True)
