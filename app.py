import tempfile

from flask import Flask, render_template, abort, redirect, url_for, flash, request
import flask_monitoringdashboard as dashboard
from markdown import markdown
from werkzeug.exceptions import HTTPException
from db_psycorg import db_handler
#import firebase
import os

# import logging
# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
dashboard.bind(app)
app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:unlimitedpower@localhost/chan'


# TODO Separate this shit to Blueprints
@app.route('/')
@app.route('/index')
# Index page with boards
def index():
    return render_template('index.html', boards_list=db_handler.get_boards(),
                           boards_name=db_handler.get_boardname(), zip=zip)


@app.route('/<string:board>', methods=['GET', 'POST'])
# Threads on board
def board(board):
    if request.method == 'GET':  # Get all threads on the board page
        if board in db_handler.get_boards():
            return render_template('board.html', board=board, threads=db_handler.get_threads(board))
        else:
            abort(404)
    elif request.method == 'POST':  # Create thread
        thread_subject = markdown(request.form['subject'])  # TODO push this to DB
        thread_message = markdown(request.form['message'])
        #attachments = request.form['file']

        new_thread = db_handler.create_thread(board=board, message=thread_message,
                                              subject=thread_subject)  # TODO ПРОВЕРКА!!
        return redirect(url_for('thread', board=board, thread=new_thread))
    else:
        abort(405)


@app.route('/<string:board>/<int:thread>', methods=['GET', 'POST'])
# Messages in the thread on the board
def thread(board, thread):
    if request.method == 'GET':  # Get all messages in a thread
        if board in db_handler.get_boards():
            return render_template('thread.html', board=board, thread=thread,
                                   root=db_handler.get_root(board, thread), posts=db_handler.get_posts(board, thread))
        else:
            abort(404)
    elif request.method == 'POST':  # Leave a message in the thread
        thread_message = markdown(request.form['message'])
        db_handler.create_post(board, thread, thread_message)
        return redirect(url_for('thread', board=board, thread=thread))
    else:
        abort(405)


@app.route('/news', methods=['GET'])
def news():
    return render_template('news.html', news=db_handler.get_news())


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template('error_base.html', error=str(code)), code


if __name__ == '__main__':
    app.run(threaded=True)

# TODO https://flask-russian-docs.readthedocs.io/ru/latest/patterns/flashing.html
