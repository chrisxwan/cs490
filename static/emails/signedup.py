import os
import sendgrid


def sendConfirmationEmail(email):
    sg = sendgrid.SendGridClient(os.getenv('CS490_SENDGRID_USERNAME'), os.getenv('CS490_SENDGRID_PASSWORD'))
    message = sendgrid.Mail()
    message.add_to('%s' %(email))
    message.set_subject('YHack 2016')
    message.set_text(buildConfirmationTextEmail())
    message.set_from('YHack <team@yhack.org>')
    status,msg = sg.send(message)
    print "Email To: %s, Status: %s" %(email, status)

def buildConfirmationTextEmail():
    return """
    Register now @ http://yhack.org
    """

for email in emails:
    sendConfirmationEmail(email)
