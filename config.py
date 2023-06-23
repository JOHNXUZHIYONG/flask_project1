SECRET_KEY = 'AKHSDKHSA'

HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWARD = 'ROOT'
DATABASE = 'project1'

DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWARD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URI

# SMTP服务器配置
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'zhiyongxu86@gmail.com'
SMTP_PASSWORD = 'cynatakvbgbnfpci'

# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWARD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)