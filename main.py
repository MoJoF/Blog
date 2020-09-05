from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Article %r>" % self.id


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/news', methods=['GET'])
def news():
    articles = Article.query.order_by(Article.id.desc()).all()

    return render_template("news.html", articles=articles)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        article = Article(title=title, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/success')

        except:
            return "Error"

    else:
        return render_template("create.html")


@app.route('/success')
def success_add():
    return render_template("success.html")


@app.route('/article<int:id>', methods=['POST', 'GET'])
def article(id):
    article = Article.query.get(id)

    return render_template("article.html", article=article)


@app.route('/article<int:id>/del')
def del_article(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect('/news')


@app.route('/article<int:id>/edit', methods=['GET', 'POST'])
def edit_article(id):
    article = Article.query.get(id)

    if request.method == 'POST':
        article.title = request.form['title']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/news')

        except:
            return "При редактировании статьи произошла ошибка"

    else:
        return render_template("edit.html", article=article)


if __name__ == '__main__':
    app.run()
