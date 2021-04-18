import os
import smtplib
import imghdr
from email.message import EmailMessage
from EmailSend import template_reader
from bs4 import BeautifulSoup
import json
import re

class MailClient:
    def sendEmail(self,contacts):
        # testing values
        # print(contacts[0])
        # print(contacts[1])
        # print(contacts[2])
        # print(contacts[3])

        EMAIL_ADDRESS = 'emergingtechchatbot@gmail.com'
        EMAIL_PASSWORD = 'chatbotemergingtech'

        msg = EmailMessage()
        msg['Subject'] = 'Covid-19 Report!'
        msg['From'] = EMAIL_ADDRESS
        # print("---------------",contacts[3])
        msg['To'] = contacts[2]

        value = contacts[3]
        values = value.get("cases")
        # print(values)
        msg.set_content("Hello Mr. {} Here is your Covid 19 Report PFA".format(contacts[0]))
        #print(contacts[2])
        template = template_reader.TemplateReader()
        email_message = template.read_template("simple")
        #print(email_message)
        country_name1 = "India"
        total1 = str(values.get("total"))
        new1 = str(values.get("new"))
        active1 = str(values.get("active"))
        critical1 = str(values.get("critical"))
        recovered1 = str(values.get("recovered"))
        print(new1 + total1)

        msg.add_alternative(email_message.format(country_name=country_name1, total=total1, new=new1, active=active1, critical=critical1,
                                    recovered=recovered1), subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            print("EMAIL_PASSWORD",EMAIL_PASSWORD)
            print("EMAIL_ADDRESS",EMAIL_ADDRESS)
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

    def __init__(self):
        pass