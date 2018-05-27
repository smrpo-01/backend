#!/usr/bin/python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    fromaddr = 'emineo.fri@gmail.com'
    username = 'emineo.fri@gmail.com'
    password = 'emineomailtest'

    def __init__(self, toaddrs, subject, message):
        self.toaddrs = ','.join(toaddrs)
        self.toaddrs_list = toaddrs
        self.subject = subject
        self.message = message

        # spremeni html body v txt da pravilno prikaze mail z htmljm
        msgtxt = self.message.replace("<p>", "")
        msgtxt = msgtxt.replace("</p>", "")

        # oblikuje text v celo html bliko
        msghtml_tmp = self.message.replace("\n", "<br>")
        msghtml = "<html><head></head><body>" + msghtml_tmp + "</body></html>"

        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = subject
        self.msg['From'] = self.fromaddr
        self.msg['To'] = self.toaddrs

        part1 = MIMEText(msgtxt, 'plain', 'utf-8')
        part2 = MIMEText(msghtml, 'html', 'utf-8')

        self.msg.attach(part1)
        self.msg.attach(part2)

    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.fromaddr, self.toaddrs_list, self.msg.as_string())
        server.quit()
