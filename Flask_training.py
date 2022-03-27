from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vlog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	intro = db.Column(db.String(300), nullable=False)
	main = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, default=datetime.now)

	def __repr__(self):
		return '<Article %r>' % self.id


@app.route('/home')
@app.route('/')
def main_page():
	return render_template('home.html')


@app.route('/second')
def second_page():
	return render_template('second.html')


@app.route('/posts')
def set_posts():
	articls = Article.query.all()
	return render_template('set_posts.html', articls=articls)


@app.route('/posts/<int:id>')
def get_post(id):
	articl = Article.query.get(id)
	return render_template('get_post.html', articl=articl)


@app.route('/posts/<int:id>/del')
def del_post(id):
	articl = Article.query.get(id)
	try:
		db.session.delete(articl)
		db.session.commit()
		return redirect('/posts')
	except:
		return f"при удалении из БД возникла ошибка"


@app.route('//posts/<int:id>/update', methods=['POST', 'GET'])
def update_article(id):
	articl = Article.query.get(id)
	if request.method == 'POST':
		articl.title = request.form['title']
		articl.intro = request.form['intro']
		articl.main = request.form['main']

		try:
			db.session.commit()
			return redirect('/posts')
		except:
			return f"при обновлении в БД возникла ошибка"
	else:
		return render_template('update_article.html', articl=articl)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
	if request.method == 'POST':
		title = request.form['title']
		intro = request.form['intro']
		main = request.form['main']
		article = Article(title=title, intro=intro, main=main)
		try:
			db.session.add(article)
			db.session.commit()
			return redirect('/posts')
		except:
			return f"при добавление в БД возникла ошибка"
	else:
		return render_template('create_article.html')


if __name__ == '__main__':
	app.run(debug=True)
