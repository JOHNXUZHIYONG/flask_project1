from flask import Flask, render_template
import config
from exts import db

from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from blueprints.shopping import bp as shopping_bp
from blueprints.email import bp as email_bp
from flask_migrate import Migrate



app =  Flask(__name__)
app.config.from_object(config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(shopping_bp)
app.register_blueprint(email_bp)



@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/base')
def base():
    return render_template('base.html')

if __name__=='__main__':
    app.run(host='10.5.56.113', port=5000, debug=True)