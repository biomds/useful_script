#!/usr/bin/python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
import glob
import sys
from argparse import ArgumentParser
parser = ArgumentParser(description="This script is used to send email")
parser.add_argument('-in','--info',help='Your email information')
parser.add_argument('-p','--password',help='Your email password')
args = parser.parse_args()

msg = MIMEMultipart()
lst = args.info
passwd = args.password
info={}
rec = open(lst,'r')
for line in rec:
	lst = line.strip().split("=")
	info[lst[0]]=lst[1]
sender = info['sender']
reciever = info['reciver']
copy = info['copy']
msg['From'] = sender
msg['To'] = reciever
msg['Cc'] = ''.join(copy)
print (type(copy))
print(msg['From'],msg['To'],msg['Cc'])
print(reciever,type(reciever))
msg['Subject'] = Header("小豆子",'utf-8').encode()
#msg['Subject'] = Header("This greetings is from a little bean",'utf-8').encode()
message = """
<html>
 <body>
  <h3>This email have some attachments!</h3>
  <p3>Hi<br/>
   Please look over the attachments by yourself.
  <p4>
   <img src="cid:image1">
  </p4>
    </p3>
 </body>
</html>
"""
lanes = glob.glob("*")
lanes = sorted(lanes)
n=0
for lane in lanes:
	f = open(lane,'rb')
	mime=MIMEBase('plain','txt',filename=lane)
	mime.add_header('Content-Disposition','attachment',filename =lane)
	mime.add_header('Content-ID','<%s>'%n)
	mime.add_header('X-Attachment-Id','%s'%n)
	mime.set_payload(f.read())
	encoders.encode_base64(mime)
	n+=1
	msg.attach(mime)
	f.close()
pic = open("LD.png",'rb')
img=MIMEBase('plain','img',filename='LD.png')
img.add_header('Content-Disposition','attachment',filename = 'LD.png')
img.add_header('Content-ID','<image1>')
img.add_header('X-Attachment-Id','image1')
img.set_payload(pic.read())
encoders.encode_base64(img)
pic.close()
msg.attach(img)
msg.attach(MIMEText(message,'html','utf-8'))
server = smtplib.SMTP("smtp.163.com")
server.starttls()
server.login(msg['From'],passwd)
server.sendmail(msg['From'],[reciever]+[copy],msg.as_string())
server.quit()
