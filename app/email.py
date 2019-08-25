from threading import Thread
import os
from flask import current_app, render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, To, Subject, PlainTextContent, HtmlContent, Mail

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    from_email = app.config['MAIL_SENDER']
    html_body = render_template(template + ".html", **kwargs)
    plain_body = render_template(template + ".txt", **kwargs)
    mail = Mail(
            from_email=app.config['MAIL_SENDER'],
            to_emails=[To(to)],
            subject=Subject(subject),
            html_content=HtmlContent(html_body),
            plain_text_content=PlainTextContent(plain_body)
            )
    return sg.client.mail.send.post(request_body=mail.get())

