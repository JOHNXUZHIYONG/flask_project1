from flask import Blueprint, render_template, request, redirect, url_for
from models import QuestionModel
from exts import db


bp=Blueprint('qa',__name__,url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/qa/publish', methods=['GET','POST'])
def qa_publish():
    if request.method == 'GET':
        return render_template('qa_publish.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = QuestionModel(title=title, content=content)
        db.session.add(question)
        db.session.commit()
        return redirect('/')