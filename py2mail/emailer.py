
# -*- coding: utf-8 -*-
"""
#### EMAILER v0.01 Beta #####
Created on Thursday, October  29  10:02:04 2015
@author: Lee Carlin
lee@adtheorent.com

The "emailer" module is a simple "smtplib" wrapper for sending emails.

Required config files (\etc):
* conf_file.ini (configurations)

"""

# Necessary libraries: #######################################
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Import the connection to config file:
import ConfigParser


def emailer(mail_conf_path,mail_list,subject,email_body_html):

    ## Initializing the configs: ##################################
    configs = ConfigParser.ConfigParser()
    configs.read(mail_conf_path)
    # Saving input var from the config file as a dictionary:
    mail_conf = dict(configs.items('mail_conf'))
    # declaring variables from input_var dictionary for ease of calling:
    my_mail  = mail_conf['my_mail']
    my_pass  = mail_conf['my_pass']


    # Open a plain text file for reading.  For this , assume that
    # the text file contains only ASCII characters.
    textfile = email_body_html
    # opening a connection to the file and saving the data to the msg instance
    fp = open(textfile, 'rb')
    msg = MIMEMultipart()
    msg.attach(MIMEText(fp.read(), 'html'))
    fp.close()

    #populating the required fields to send the email:
    msg['Subject'] = subject
    msg['From'] = my_mail
    msg['To'] = mail_list
    # Send the message via your  own SMTP server
    server = smtplib.SMTP('smtp.gmail.com')
    server.ehlo()
    server.starttls()
    server.login(my_mail, my_pass)
    server.sendmail(msg['From'], mail_conf['mail_list'].split(','), msg.as_string())
    server.quit()