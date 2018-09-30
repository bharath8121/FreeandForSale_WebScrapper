import bs4, requests, time, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class FreeForSale:
    def __init__(self, link):
        self.link = link
        self._list = []

    def refresh(self):
        item_names = []
        request = requests.get(self.link)
        parser = bs4.BeautifulSoup(request.text)
        itemlist = parser.select('div[class="body"] > div[class="clear"] > div[class="item"] > a[class="item-inner"] > h4 > span[class="desc"]')
        for i in itemlist:
            item_names.append(i.getText())
        recently_added = set(item_names) - set(self._list)
        if len(recently_added) > 0:
            print("yo you have some new items to buy!!")
            added = '\n'.join(recently_added)
            sendMail = MailBox()
            sendMail.sendTo({'mailbody' : added, 'toSend' : 'bharathchandra.chandra96@gmail.com', 'subject':'The new items.' })
        else:
            print("You got nothing new!!!")
        for i in recently_added:
            print(i)
        self._list = item_names
        

class MailBox:
    def __init__(self):
        self.username = "username"
        self.password = "password"

    def sendTo(self, mail_parameters):
        toSend = mail_parameters['toSend']
        message = MIMEMultipart()
        text = MIMEText(mail_parameters['mailbody'])
        message.attach(text)
        message['subject'] = mail_parameters['subject']

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.username, self.password)
        print('Logged In')
        server.sendmail(self.username, toSend, message.as_string())
        server.quit()
        print("Message Sent")

if __name__ == "__main__":
    freeforsale=FreeForSale('https://uscfreeandforsale.appspot.com/')
    while True:
        freeforsale.refresh()
        time.sleep(300)
    print("exiting the program..!!")
    
