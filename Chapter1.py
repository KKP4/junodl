from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import timezone, datetime
import sys


localTime = datetime.now(timezone.utc).date().isoformat()
sender = "yout@email.com"
receiver = "target@email.com"
fileName = 'file_in_folder.txt'
baseUrl = 'https://www.junodownload.com'
path = urlopen('https://www.junodownload.com/deep-dubstep/this-week/releases/')
bs = BeautifulSoup(path.read(), 'html.parser')
urls = []
constructedUrls = []
port = 465
password = sys.argv[1]
subject = "Komadi"
body = "Novi (zadnji teden) komadi iz Junodownload Deep Dubstep sekcije " + str(localTime)
message = MIMEMultipart()
message["From"] = sender
message["To"] = receiver
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))


for a in bs.find_all('a', href=True):
    urls.append(a['href'])
matching = [s for s in urls if "/products/" in s]

for a in matching:
    constructedUrls.append(baseUrl+a)

with open(fileName, 'w', encoding='UTF-8') as file:
    for item in set(constructedUrls):
        file.write("%s\n" % item)

with open(fileName, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {fileName}",
)
message.attach(part)
text = message.as_string()
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("you@email.com", password)
        server.sendmail(sender, receiver, text)

