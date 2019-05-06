#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Send_email:

    def Send_email(self):
        fromaddr = "672394162@qq.com"
        toaddr = "heronghr@cn.ibm.com"
        msg = MIMEText('This email is a testing email to check if the python send email can be successfully.', 'plain', 'utf-8')
        msg['From'] = Header("Cindy He", 'utf-8')
        msg['To'] = Header("heronghr", 'utf-8')
        msg['Subject'] = 'Python test'

        #body = "HAHAHA!"

        #msg.attach(MIMEText(body, 'plain'))
        try:
            server = smtplib.SMTP_SSL("smtp.qq.com",465)
            server.login(fromaddr, 'atdrvjurcrsybdgg')
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
        except Exception as e:
            print("Send failed")
            print(e.args)
        finally:
            server.quit()


if __name__ == "__main__":
    sendEmail = Send_email()
    sendEmail.Send_email()
