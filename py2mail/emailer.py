
# -*- coding: utf-8 -*-
"""
#### py2mail v0.01 Beta #####
Created on Thursday, October  29  10:02:04 2015
@author: Lee Carlin
lee@adtheorent.com

The "py2mail" module is a simple "smtplib" wrapper for sending emails.

Required config dictionary

"""

# Necessary libraries: #######################################
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
# Import the connection to config file:

def emailer(mail_conf,subject,email_body_html_file, files = None):
    """
    This function is a wrapper to smtplib.
    :param mail_configs: A dictionary with the following:
                mail_conf = {
                            'client':'your client',
                            'my_mail' : 'youremail@yourmail',
                            'my_pass' : 'your password',
                            'mail_list' : 'first@mail,second@mail',
                            }
    :param subject: your email subject
    :param email_body_html_file: an html file you'ld like to send
    :param files: any attachements yould like to add
    :return: None. an email should be sent.
    """
    ## Initializing the configs: ##################################
    # declaring variables from input_var dictionary for ease of calling:
    my_mail  = mail_conf['my_mail']
    my_pass  = mail_conf['my_pass']
    mail_list = mail_conf['mail_list']
    client = mail_conf['client']
    # Open a plain text file for reading.  For this , assume that
    # the text file contains only ASCII characters.
    textfile = email_body_html_file
    # opening a connection to the file and saving the data to the msg instance
    fp = open(textfile, 'rb')
    msg = MIMEMultipart()
    msg.attach(MIMEText(fp.read(), 'html'))
    fp.close()

    # Attaching files
    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f),
                Name=basename(f)
            ))


    #populating the required fields to send the email:
    msg['Subject'] = subject
    msg['From'] = my_mail
    msg['To'] = mail_list
    # Send the message via your  own SMTP server
    server = smtplib.SMTP(client)
    server.ehlo()
    server.starttls()
    server.login(my_mail, my_pass)
    server.sendmail(msg['From'], mail_list.split(','), msg.as_string())
    server.quit()
