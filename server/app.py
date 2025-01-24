#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page views to 0 if not already set
    session['page_views'] = session.get('page_views', 0)

    # Check if the article exists
    article = Article.query.get(id)
    if not article:
        return {'message': 'Article not found.'}, 404

    # Increment the page view count
    session['page_views'] += 1

    # Check if the user has reached the limit
    if session['page_views'] > 3:
        return {'message': 'Maximum pageview limit reached'}, 401

    # Serialize the article and return it as JSON
    article_data = {
        'id': article.id,
        'author': article.author,
        'title': article.title,
        'content': article.content,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date,
    }
    return jsonify(article_data), 200


if __name__ == '__main__':
    app.run(port=5555)
