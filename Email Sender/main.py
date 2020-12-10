import smtplib
from email.message import EmailMessage
import getpass

mymail = (str(input( 'YOUR EMAIL:')))
mypass = (getpass.getpass('\nThe password will not be visible for privacy\nYOUR PASSWORD:'))
mailsend = (str(input('\nEMAIL OF WHOM TO SEND:')))
subject = (input('\nSUBJECT:'))
message = (input('\nMESSAGE:'))

msg = EmailMessage()
msg.set_content(message)

msg['Subject'] = subject
msg['From'] = mymail
msg['To'] = mailsend

# Send Mail
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(mymail, mypass)
server.send_message(msg)

print("\nThe Mail was sent Successfully")
input("\n Press Enter to exit")

server.quit()