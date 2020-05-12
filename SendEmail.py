import json
import getpass
from datetime import datetime
from email.mime.text import MIMEText
import pytz
import requests
import smtplib
import time

sender_email = None
password = None
receiver_email = None


def get_total_infected_by_country(state):
    url_summary = 'https://api.covid19api.com/summary'
    total_confirmed = None
    response = requests.get(url_summary).json()
    for country in response['Countries']:
        if country['Country'] == state:
            total_confirmed = country['TotalConfirmed']
    return total_confirmed


def get_info():
    global sender_email, password, receiver_email
    sender_email = input("Please enter your email address: ")
    password = getpass.getpass(prompt='Please enter password of ' + sender_email + ' email address: ')
    receiver_email = input("Please insert receiver email address: ")


subject_field = 'Subject'
from_field = 'From'
to_field = 'To'
contacts_file_name = 'Contacts.txt'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
my_country = 'Israel'
number_of_seconds_in_minute = 60
number_of_minutes = 10
invalid_string = 'Invalid data...'
get_info()
while True:
    try:
        infected_people = get_total_infected_by_country(my_country)
        html = """\
                <html>
                  <body>
                    <p>The number of infected people with <b>COVID-19</b> is: """ + str(infected_people) + """ </p>
                  </body>
                </html>
                """
        msg = MIMEText(html, 'html')
        msg[subject_field] = "COVID-19 in Israel"
        msg[from_field] = sender_email
        msg[to_field] = receiver_email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(
            'The message sent successfully at: ' + datetime.now().astimezone(pytz.timezone('Asia/Jerusalem')).strftime(
                "%d-%m-%Y %H:%M:%S") + " to " + msg[to_field])
        time.sleep(number_of_minutes * number_of_seconds_in_minute)
    except smtplib.SMTPException:
        print(invalid_string)
        get_info()
    except json.decoder.JSONDecodeError:
        print("Invalid response from corona API, trying to send GET request again...")
    except (TypeError, AttributeError):
        print(invalid_string)
        get_info()
