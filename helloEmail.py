#encoding=utf8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
def sendMail():
    sender='zamjbn@163.com'
    #receiver='zamjbn@163.com'
    receiver = '1369796093@qq.com'
    message = MIMEText('爬虫已经爬去完成，可以下载数据了.', 'plain', 'utf-8')
    message['From'] = Header(sender)
    message['To'] = Header(receiver)
    subject = 'Python 邮件通知'
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP_SSL("smtp.163.com")
    smtpObj.login(sender, 'cyl0516')
    smtpObj.sendmail(sender, receiver, message.as_string())
    smtpObj.quit()
    print "邮件发送成功"

sendMail()