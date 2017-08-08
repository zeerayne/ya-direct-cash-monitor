import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def make_message(clients_array, config):
    from datetime import datetime
    now = datetime.now()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Yandex.Direct report " + now.strftime('%d.%m.%Y')
    msg['From'] = config['email']['from']
    msg['To'] = config['email']['to']

    html = """<html><head></head><body><table>"""
    for c in clients_array:
        html += "<tr><td>" + c['login'] + "</td><td>" + c['amount'] + "</td><td>" + c['currency'] + "</td></tr>"
    html += """</table></body></html>"""
    part = MIMEText(html, 'html')
    msg.attach(part)
    return msg


def send_notification(clients_array, config):
    server = smtplib.SMTP(
        config['email']['smtp_host'],
        int(config['email']['smtp_port'])
    )
    server.login(
        config['email']['login'],
        config['email']['password']
    )
    msg = make_message(clients_array, config)
    server.sendmail(
        config['email']['from'],
        config['email']['to'].replace(' ', '').split(","),
        msg.as_string()
    )
    server.quit()
