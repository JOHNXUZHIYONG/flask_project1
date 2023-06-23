from flask import Blueprint, render_template, request, redirect, url_for, session
from models import UserModel
from exts import db

bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            print('no register')
            return redirect(url_for('auth.register'))
        else:
            if password == user.password:
                print('you log in now')
                session['user_id'] = user.id
                return redirect(url_for('shopping.order'))
            else:
                print('wrong password')
                return redirect(url_for('auth.login'))





@bp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        user=UserModel(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
