from bs4 import BeautifulSoup as BS
import urllib.request
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime


class Hermes():
    def hermes(self):

        url = 'http://www.poetryoutloud.org/poems-and-performance/random-poem'

        settings = urllib.request.Request(url,
                                          headers={'User-Agent': 'Mozilla'})

        source = urllib.request.urlopen(settings).read().decode()
        signs = re.compile("(\n\s*?\n|<br>|\xa0|\n\s{2})")
        while signs.search(source):
            source = signs.sub('\n', source)

        soup = BS(source, 'lxml')

        poem = soup.find_all('p')[0].text

        title = soup.find_all('div', class_="gap gap_x1dot5")[0].text
        dog = {'poem': poem, 'title': title}
        for i in dog.keys():
            while signs.search(dog.get(i)):
                dog[i] = signs.sub('\n', dog.get(i))
        start_line = re.compile('(^\n|^\s)')
        dog['title'] = start_line.sub('', dog['title'])
        return dog['poem'], dog['title']

    def settings(self):

        # We are creating settings file
        # that will check if we have today
        # received a fresh poetry

        today = datetime.datetime.now().day
        try:
            with open('settings.txt', 'r') as f:
                date = f.read()
            if str(today) == str(date):
                print(date, today)
                date = None
            else:
                date = today
        except NameError:
            date = today

        if date != None:
            with open('settings.txt', 'w') as f:
                f.write(str(date))

        return date

    def send(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # give your credentials 
        server.login('MAIL', 'PASS')
        poem, title = self.hermes()
        msg = MIMEMultipart()
        # put recipients
        recipients = []

        title = title.replace("\n", " ")
        SEP = title.find(" By ")

        msg['Subject'] = "Hermes - Twój dostawca świeżych wierszy: \"" \
                         + title[:SEP] \
                         + "\"" \
                         + title[SEP:]
        # put from
        msg['FROM'] = ""
        msg['TO'] = ", ".join(recipients)
        print(poem, title, sep="\n")
        msg.attach(MIMEText(poem, 'plain'))
        server.sendmail('codzienny dostawca', recipients, msg.as_string())

