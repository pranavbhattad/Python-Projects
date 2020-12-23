import smtplib
from email.message import EmailMessage
import getpass

mymail = (str(input( 'YOUR EMAIL:')))
mypass = (getpass.getpass('\nThe password will not be visible for privacy\nYOUR PASSWORD:'))
mailsend = (str(input('\nEMAIL OF WHOM TO SEND:')))
subject = (input('\nSUBJECT:'))
message = (input('\nMESSAGE:'))
times = (int(input('\nHow many times should I send the mail:')))

msg = EmailMessage()
msg.set_content(message)

msg['Subject'] = subject
msg['From'] = mymail
msg['To'] = mailsend

# Send Mail
def sendmail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mymail, mypass)
    server.send_message(msg)

    print("\nThe Mail was sent Successfully")

    server.quit()

for i in range(times):
    sendmail()
    print("Your all mails were sent successfully")
    input("\n Press Enter to exit")
