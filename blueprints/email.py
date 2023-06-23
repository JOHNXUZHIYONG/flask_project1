from flask import Blueprint, render_template, request, redirect, url_for, session
from config import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from werkzeug.utils import secure_filename

bp=Blueprint('email',__name__,url_prefix='/email')



@bp.route('/send_email', methods=['GET','POST'])
def send_email():
    if request.method == 'POST':
        # 获取表单数据
        sender = request.form['sender']
        receiver = request.form['receiver']
        subject = request.form['subject']
        message = request.form['message']
        print(message)
        print('hello')

        # SMTP服务器配置
        smtp_host = SMTP_HOST
        smtp_port = SMTP_PORT
        smtp_username = SMTP_USERNAME
        smtp_password = SMTP_PASSWORD

        # 创建一个MIME消息
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject

        # 将邮件内容附加到MIME消息中
        msg.attach(MIMEText(message, 'plain'))

        # 处理上传的附件
        if 'attachment' in request.files:
            attachment_file = request.files['attachment']
            if attachment_file.filename != '':
                filename = secure_filename(attachment_file.filename)
                attachment = MIMEApplication(attachment_file.read())
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attachment)

        # 创建一个SMTP会话
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            # 启动TLS加密（如果需要）
            server.starttls()

            # 使用用户名和密码登录SMTP服务器
            server.login(smtp_username, smtp_password)

            # 发送邮件
            server.send_message(msg)

        return f'Email has been sent to {receiver} successfully！'
    else:
        return render_template('send_email.html')