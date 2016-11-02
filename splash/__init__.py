import boto
from boto.s3.key import Key
from werkzeug.utils import secure_filename
import hashlib
import os
import sendgrid
import re
import cgi
from yurl import URL
from titlecase import titlecase

def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True

def is_length_of_name_valid(name):
    if len(name) > 0 and len(name) < 76:
        return True
    return False

def is_length_of_major_valid(major):
    if len(major) > 0 and len(major) < 101:
        return True
    return False

def is_length_of_school_valid(school):
    if len(school) > 0 and len(school) < 201:
        return True
    return False

def is_length_of_projects_and_awards_valid(projects_and_awards):
    if len(projects_and_awards) >= 0 and len(projects_and_awards) < 5001:
        return True
    return False

def is_url_valid(url):
    try:
        URL(url).validate()
        return True
    except:
        return False

def is_length_of_password_valid(password):
    if len(password) > 5 and len(password) < 51:
        return True
    return False  

def sendConfirmationEmail(a):
    sg = sendgrid.SendGridClient(os.getenv('CS490_SENDGRID_USERNAME'), os.getenv('CS490_SENDGRID_PASSWORD'))
    message = sendgrid.Mail()
    message.add_to('%s %s <%s>' %(cgi.escape(a.firstname), cgi.escape(a.lastname), cgi.escape(a.email)))
    message.set_subject('Email Confirmation')
    message.set_html(buildConfirmationHTMLEmail(cgi.escape(a.firstname), a.confirmation_code))
    message.set_text(buildConfirmationTextEmail(cgi.escape(a.firstname), a.confirmation_code))
    message.set_from('Christopher Wan <christopher.wan@yale.edu>')
    status,msg = sg.send(message)
    print "Confirmation Email To: %s, Status: %s" %(cgi.escape(a.email), status)

def sendPasswordResetEmail(a):
    sg = sendgrid.SendGridClient(os.getenv('CS490_SENDGRID_USERNAME'), os.getenv('CS490_SENDGRID_PASSWORD'))
    message = sendgrid.Mail()
    message.add_to('%s %s <%s>' %(cgi.escape(a.firstname), cgi.escape(a.lastname), cgi.escape(a.email)))
    message.set_subject('CS490 Password Reset')
    message.set_html(buildResetPasswordHTMLEmail(cgi.escape(a.firstname), a.password_reset_token))
    message.set_text(buildResetPasswordTextEmail(cgi.escape(a.firstname), a.password_reset_token))
    message.set_from('Christopher Wan <christopher.wan@yale.edu>')
    status,msg = sg.send(message)
    print "Password Reset Email To: %s, Status: %s" %(cgi.escape(a.email), status)
    return status

def sendEmailChangeEmail(a):
    print "here"
    sg = sendgrid.SendGridClient(os.getenv('CS490_SENDGRID_USERNAME'), os.getenv('CS490_SENDGRID_PASSWORD'))
    message = sendgrid.Mail()
    message.add_to('%s %s <%s>' %(cgi.escape(a.firstname), cgi.escape(a.lastname), cgi.escape(a.email)))
    message.set_subject('YHack 2016 Password Reset')
    message.set_html(buildChangeEmailHTMLEmail(cgi.escape(a.firstname), a.confirmation_code))
    message.set_text(buildChangeEmailTextEmail(cgi.escape(a.firstname), a.confirmation_code))
    message.set_from('YHack <team@yhack.org>')
    status,msg = sg.send(message)
    print "Change Email Address Email To: %s, Status: %s" %(cgi.escape(a.email), status)


def getFileSize(obj):
    if obj.content_length:
        return obj.content_length

    try:
        pos = obj.tell()
        obj.seek(0, 2)  #seek to end
        size = obj.tell()
        obj.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass

    # in-memory file object that doesn't support seeking or tell
    return 0  #assume small enough

def buildConfirmationHTMLEmail(firstName, confirmationCode):
    confirmationURL = os.getenv('CS490_ADMIN_URL') + 'submitted?code=2&confirmationCode=' + confirmationCode
    msg = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>*|MC:SUBJECT|*</title>
            <style type="text/css">
                #outlook a{padding:0;}
                body{width:100% !important; background-color:#ffffff;-webkit-text-size-adjust:none; -ms-text-size-adjust:none;margin:0; padding:0;} 
                .ReadMsgBody{width:100%;} 
                .ExternalClass{width:100%;}
                ol li {margin-bottom:15px;}
                    
                img{height:auto; line-height:100%; outline:none; text-decoration:none;}
                #backgroundTable{height:100% !important; margin:0; padding:0; width:100% !important;}
                    
                p {margin: 1em 0;}
                    
                h1, h2, h3, h4, h5, h6 {color:#222222 !important; font-family:Arial, Helvetica, sans-serif; line-height: 100% !important;}
                    
                table td {border-collapse:collapse;}
                    
                .yshortcuts, .yshortcuts a, .yshortcuts a:link,.yshortcuts a:visited, .yshortcuts a:hover, .yshortcuts a span { color: black; text-decoration: none !important; border-bottom: none !important; background: none !important;}
                    
                .im {color:black;}
                div[id="tablewrap"] {
                        width:100%; 
                        max-width:600px!important;
                    }
                table[class="fulltable"], td[class="fulltd"] {
                        max-width:100% !important;
                        width:100% !important;
                        height:auto !important;
                    }
                            
                @media screen and (max-device-width: 430px), screen and (max-width: 430px) { 
                        td[class=emailcolsplit]{
                            width:100%!important; 
                            float:left!important;
                            padding-left:0!important;
                            max-width:430px !important;
                        }
                    td[class=emailcolsplit] img {
                    margin-bottom:20px !important;
                    }
                }
            </style>
        </head>
        <body style="width:100%; margin:0; padding:0; -webkit-text-size-adjust:none; -ms-text-size-adjust:none; background-image:url('https://s3-us-west-2.amazonaws.com/yhack-static/furley_bg.png');">
        <table cellpadding="0" cellspacing="0" border="0" id="backgroundTable" style="height:auto !important; margin:0; padding:0; width:100% !important; background-image:url('https://s3-us-west-2.amazonaws.com/yhack-static/furley_bg.png'); color:#222222;">
            <tr>
                <td>
                <div id="tablewrap" style="width:90% !important; max-width:600px !important; text-align:center; margin:0 auto; padding-bottom:5px; padding-top:15px">
                      <table id="contenttable" width="600" align="center" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF; margin:0 auto; text-align:center; border:none; width: 100% !important; max-width:600px !important;border-bottom-left-radius:5px;border-bottom-right-radius:5px">
                    <tr>
                        <td width="100%">
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="25" width="100%">
                                <tr>
                                    <td width="100%" bgcolor="#ffffff" style="text-align:left;">
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:25px; padding:0; font-weight:normal;">
                                            Dear """ + firstName + """,                                  
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            Thank you for creating an account. Please confirm your account by clicking the button below!
                                        </p>
                                    </td>
                                </tr>
                           </table>
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="0" width="100%">
                                <tr>
                                  <td width="100%" bgcolor="#ffffff" style="text-align:center;"><a style="font-weight:bold; text-decoration:none;" href='""" + confirmationURL + """'><div style="display:block; max-width:100% !important; width:65% !important; height:auto !important;background-color:rgb(15, 138, 67);padding-top:15px;padding-right:15px;padding-bottom:15px;padding-left:15px;border-radius:5px;color:#ffffff;font-size:24px;font-family:Arial, Helvetica, sans-serif;margin: 0 auto; margin-bottom:10px;">Confirm Your Email Address</div></a></td>
                                </tr>
                           </table>
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" width="100%" style="border-bottom-left-radius:5px;border-bottom-right-radius:5px;">
                                <tr>
                                    <td width="50%" bgcolor="#ffffff" style="text-align:left;border-bottom-left-radius:5px;border-bottom-right-radius:5px;padding-bottom:10px;padding-top:30px;">
                                        <a href="http://sendgrid.com/?utm_source=Dev%20Rel%20Unspecified&utm_campaign=Email%20Sponsorship&utm_medium=email" style="margin-left:62px;">
                                          <img src="https://s3.amazonaws.com/static.sendgrid.com/mkt/poweredbysendgrid.png" alt="Email Powered By SendGrid" width="200" height="40" />
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                </div>
                </td>
            </tr>
        </table> 
        </body>
    </html>
    """
    return msg

def buildConfirmationTextEmail(firstName, confirmationCode):
    confirmationURL = os.getenv('CS490_ADMIN_URL') + 'submitted?code=2&confirmationCode=' + confirmationCode
    return """
    Dear """ + firstName + """,\n

    Thank you for applying to YHack Fall 2016! Your application has been received.
    In order for us to consider your application, however, you must confirm your 
    email address within the next 24 hours.\n

    Please follow """ + confirmationURL + """ to do so.\n

    Applications are batch reviewed on a rolling basis every few weeks,
    so be on the lookout for another email with further instructions.\n

    In the meantime, you can get in touch with us at team@yhack.org with any questions.\n

    Yours Truly,\n

    The YHack Team"""


def buildResetPasswordHTMLEmail(firstName, resetToken):
    confirmationURL = os.getenv('CS490_ADMIN_URL') + 'reset-password?token=' + resetToken
    msg = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>*|MC:SUBJECT|*</title>
            <style type="text/css">
                #outlook a{padding:0;}
                body{width:100% !important; background-color:#ffffff;-webkit-text-size-adjust:none; -ms-text-size-adjust:none;margin:0; padding:0;} 
                .ReadMsgBody{width:100%;} 
                .ExternalClass{width:100%;}
                ol li {margin-bottom:15px;}
                    
                img{height:auto; line-height:100%; outline:none; text-decoration:none;}
                #backgroundTable{height:100% !important; margin:0; padding:0; width:100% !important;}
                    
                p {margin: 1em 0;}
                    
                h1, h2, h3, h4, h5, h6 {color:#222222 !important; font-family:Arial, Helvetica, sans-serif; line-height: 100% !important;}
                    
                table td {border-collapse:collapse;}
                    
                .yshortcuts, .yshortcuts a, .yshortcuts a:link,.yshortcuts a:visited, .yshortcuts a:hover, .yshortcuts a span { color: black; text-decoration: none !important; border-bottom: none !important; background: none !important;}
                    
                .im {color:black;}
                div[id="tablewrap"] {
                        width:100%; 
                        max-width:600px!important;
                    }
                table[class="fulltable"], td[class="fulltd"] {
                        max-width:100% !important;
                        width:100% !important;
                        height:auto !important;
                    }
                            
                @media screen and (max-device-width: 430px), screen and (max-width: 430px) { 
                        td[class=emailcolsplit]{
                            width:100%!important; 
                            float:left!important;
                            padding-left:0!important;
                            max-width:430px !important;
                        }
                    td[class=emailcolsplit] img {
                    margin-bottom:20px !important;
                    }
                }
            </style>
        </head>
        <body style="width:100%; margin:0; padding:0; -webkit-text-size-adjust:none; -ms-text-size-adjust:none; background-image:url('https://s3-us-west-2.amazonaws.com/yhack-static/furley_bg.png');">
        <table cellpadding="0" cellspacing="0" border="0" id="backgroundTable" style="height:auto !important; margin:0; padding:0; width:100% !important; background-image:url('https://s3-us-west-2.amazonaws.com/yhack-static/furley_bg.png'); color:#222222;">
            <tr>
                <td>
                <div id="tablewrap" style="width:90% !important; max-width:600px !important; text-align:center; margin:0 auto; padding-bottom:5px; padding-top:15px">
                      <table id="contenttable" width="600" align="center" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF; margin:0 auto; text-align:center; border:none; width: 100% !important; max-width:600px !important;border-bottom-left-radius:5px;border-bottom-right-radius:5px">
                    <tr>
                        <td width="100%">
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="25" width="100%">
                                <tr>
                                    <td width="100%" bgcolor="#ffffff" style="text-align:left;">
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:25px; padding:0; font-weight:normal;">
                                            Dear """ + firstName + """,                                  
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            You can reset your password <a style="color:#2489B3; font-weight:bold; text-decoration:underline;" href='""" + confirmationURL + """'>here</a>.
                                        </p>

                                         <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            If you did not request a change in password, please let us know.
                                        </p>
                                    </td>
                                </tr>
                           </table>
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" width="100%" style="border-bottom-left-radius:5px;border-bottom-right-radius:5px;">
                                <tr>
                                    <td width="50%" bgcolor="#ffffff" style="text-align:left;border-bottom-left-radius:5px;border-bottom-right-radius:5px;padding-bottom:10px;padding-top:30px;">
                                        <a href="http://sendgrid.com/?utm_source=Dev%20Rel%20Unspecified&utm_campaign=Email%20Sponsorship&utm_medium=email" style="margin-left:62px;">
                                          <img src="https://s3.amazonaws.com/static.sendgrid.com/mkt/poweredbysendgrid.png" alt="Email Powered By SendGrid" width="200" height="40" />
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                </div>
                </td>
            </tr>
        </table> 
        </body>
    </html>
    """
    return msg

def buildResetPasswordTextEmail(firstName, resetToken):
    confirmationURL = os.getenv('CS490_ADMIN_URL') + 'reset-password?token=' + resetToken
    return """
    Dear """ + firstName + """,\n

    Please follow """ + confirmationURL + """ to reset your password.\n
    
    This link will expire in 24 hours.  If you did not request a change
    in password, please let us know.

    You can get in touch with us at team@yhack.org with any questions.\n

    Yours Truly,\n

    The YHack Team"""

def buildChangeEmailHTMLEmail(firstName, resetToken):
    confirmationURL = os.getenv('CS490_ADMIN_URL') + 'submitted?code=2&confirmationCode=' + resetToken
    msg = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>*|MC:SUBJECT|*</title>
            <style type="text/css">
                #outlook a{padding:0;}
                body{width:100% !important; background-color:#ffffff;-webkit-text-size-adjust:none; -ms-text-size-adjust:none;margin:0; padding:0;} 
                .ReadMsgBody{width:100%;} 
                .ExternalClass{width:100%;}
                ol li {margin-bottom:15px;}
                    
                img{height:auto; line-height:100%; outline:none; text-decoration:none;}
                #backgroundTable{height:100% !important; margin:0; padding:0; width:100% !important;}
                    
                p {margin: 1em 0;}
                    
                h1, h2, h3, h4, h5, h6 {color:#222222 !important; font-family:Arial, Helvetica, sans-serif; line-height: 100% !important;}
                    
                table td {border-collapse:collapse;}
                    
                .yshortcuts, .yshortcuts a, .yshortcuts a:link,.yshortcuts a:visited, .yshortcuts a:hover, .yshortcuts a span { color: black; text-decoration: none !important; border-bottom: none !important; background: none !important;}
                    
                .im {color:black;}
                div[id="tablewrap"] {
                        width:100%; 
                        max-width:600px!important;
                    }
                table[class="fulltable"], td[class="fulltd"] {
                        max-width:100% !important;
                        width:100% !important;
                        height:auto !important;
                    }
                            
                @media screen and (max-device-width: 430px), screen and (max-width: 430px) { 
                        td[class=emailcolsplit]{
                            width:100%!important; 
                            float:left!important;
                            padding-left:0!important;
                            max-width:430px !important;
                        }
                    td[class=emailcolsplit] img {
                    margin-bottom:20px !important;
                    }
                }
            </style>
        </head>
        <body style="width:100%; margin:0; padding:0; -webkit-text-size-adjust:none; -ms-text-size-adjust:none; background-image:url('https://s3-us-west-2.amazonaws.com/yhack-static/furley_bg.png');">
        <table cellpadding="0" cellspacing="0" border="0" id="backgroundTable" style="height:auto !important; margin:0; padding:0; width:100% !important; background-image:url('https://s3-us-west-2.amazonaws.com/yhack-static/furley_bg.png'); color:#222222;">
            <tr>
                <td>
                <div id="tablewrap" style="width:90% !important; max-width:600px !important; text-align:center; margin:0 auto; padding-bottom:5px; padding-top:15px">
                      <table id="contenttable" width="600" align="center" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF; margin:0 auto; text-align:center; border:none; width: 100% !important; max-width:600px !important;border-bottom-left-radius:5px;border-bottom-right-radius:5px">
                    <tr>
                        <td width="100%">
                            <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="0" width="100%">
                                <tr>
                                    <td width="100%" bgcolor="#ffffff" style="text-align:center;"><a href="http://yhack.org"><img src="https://s3-us-west-2.amazonaws.com/yhack-static/header.png" alt="Welcome to YHack 2016!" style="display:inline-block; max-width:100% !important; width:100% !important; height:auto !important; border-top-left-radius:5px; border-top-right-radius:5px;" border="0"></a>
                                    </td>
                                </tr>
                           </table>
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="25" width="100%">
                                <tr>
                                    <td width="100%" bgcolor="#ffffff" style="text-align:left;">
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:25px; padding:0; font-weight:normal;">
                                            Dear """ + firstName + """,                                  
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            You can confirm your email change <a style="color:#2489B3; font-weight:bold; text-decoration:underline;" href='""" + confirmationURL + """'>here</a>. Please do so within the next 24 hours.
                                        </p>

                                         <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            As a reminder, your application status has changed to unconfirmed, and will only change back once your confirm the email address change.
                                        </p>

                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:25px; padding:0; font-weight:normal;">
                                            Feel free to get in touch with us at <a style="color:#2489B3; font-weight:bold; text-decoration:underline;" href="mailto:team@yhack.org">team@yhack.org</a> with any questions.
                                        </p>

                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            The YHack Team
                                        </p>
                                    </td>
                                </tr>
                           </table>
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" width="100%" style="border-bottom-left-radius:5px;border-bottom-right-radius:5px;">
                                <tr>
                                    <td width="50%" bgcolor="#ffffff" style="text-align:left;border-bottom-left-radius:5px;border-bottom-right-radius:5px;padding-top:30px;padding-right:25px;padding-bottom:10px;padding-left:25px;">
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:11px; line-height:14px; margin-top:15px; margin-bottom:0px; padding:0; font-weight:normal;">
                                            Questions? Contact us at <a href="mailto:team@yhack.org">team@yhack.org</a>.<br>
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:11px; line-height:14px; margin-top:0px; margin-bottom:0px; padding:0; font-weight:normal;">
                                            Copyright 2016 YHack. All Rights Reserved.<br>
                                        </p>
                                    </td>
                                    <td width="50%" bgcolor="#ffffff" style="text-align:left;border-bottom-left-radius:5px;border-bottom-right-radius:5px;padding-bottom:10px;padding-top:30px;">
                                        <a href="http://sendgrid.com/?utm_source=Dev%20Rel%20Unspecified&utm_campaign=Email%20Sponsorship&utm_medium=email" style="margin-left:62px;">
                                          <img src="https://s3.amazonaws.com/static.sendgrid.com/mkt/poweredbysendgrid.png" alt="Email Powered By SendGrid" width="200" height="40" />
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                </div>
                </td>
            </tr>
        </table> 
        </body>
    </html>
    """
    return msg

def buildChangeEmailTextEmail(firstName, resetToken):
    confirmationURL = os.getenv('CS490_ADMIN_URL') + 'submitted?code=2&confirmationCode=' + resetToken
    return """
    Dear """ + firstName + """,\n

    Please follow """ + confirmationURL + """ to confirm a change in
    your email address.
    
    Your application status will remain as unconfirmed until you confirm
    this change.

    You can get in touch with us at team@yhack.org with any questions.\n

    Yours Truly,\n

    The YHack Team"""

def buildVolunteerEmailHTMLEmail():
    return """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>*|MC:SUBJECT|*</title>
            <style type="text/css">
                #outlook a{padding:0;}
                body{width:100% !important; background-color:#ffffff;-webkit-text-size-adjust:none; -ms-text-size-adjust:none;margin:0; padding:0;} 
                .ReadMsgBody{width:100%;} 
                .ExternalClass{width:100%;}
                ol li {margin-bottom:15px;}
                    
                img{height:auto; line-height:100%; outline:none; text-decoration:none;}
                #backgroundTable{height:100% !important; margin:0; padding:0; width:100% !important;}
                    
                p {margin: 1em 0;}
                    
                h1, h2, h3, h4, h5, h6 {color:#222222 !important; font-family:Arial, Helvetica, sans-serif; line-height: 100% !important;}
                    
                table td {border-collapse:collapse;}
                    
                .yshortcuts, .yshortcuts a, .yshortcuts a:link,.yshortcuts a:visited, .yshortcuts a:hover, .yshortcuts a span { color: black; text-decoration: none !important; border-bottom: none !important; background: none !important;}
                    
                .im {color:black;}
                div[id="tablewrap"] {
                        width:100%; 
                        max-width:600px!important;
                    }
                table[class="fulltable"], td[class="fulltd"] {
                        max-width:100% !important;
                        width:100% !important;
                        height:auto !important;
                    }
                            
                @media screen and (max-device-width: 430px), screen and (max-width: 430px) { 
                        td[class=emailcolsplit]{
                            width:100%!important; 
                            float:left!important;
                            padding-left:0!important;
                            max-width:430px !important;
                        }
                    td[class=emailcolsplit] img {
                    margin-bottom:20px !important;
                    }
                }
            </style>
        </head>
        <body style="width:100%; margin:0; padding:0; -webkit-text-size-adjust:none; -ms-text-size-adjust:none;">
        <table cellpadding="0" cellspacing="0" border="0" id="backgroundTable" style="height:auto !important; margin:0; padding:0; width:100% !important; color:#222222;">
            <tr>
                <td>
                <div id="tablewrap" style="width:90% !important; max-width:600px !important; text-align:center; margin:0 auto; padding-bottom:5px; padding-top:15px">
                      <table id="contenttable" width="600" align="center" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF; margin:0 auto; text-align:center; border:none; width: 100% !important; max-width:600px !important;border-bottom-left-radius:5px;border-bottom-right-radius:5px">
                    <tr>
                        <td width="100%">
                            <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="0" width="100%">
                                <tr>
                                    <td width="100%" bgcolor="#ffffff" style="text-align:center;"><a href="http://yhack.org"><img src="https://s3-us-west-2.amazonaws.com/yhack-static/header2.png" style="display:inline-block; max-width:100% !important; width:100% !important; height:auto !important;" border="0"></a>
                                    </td>
                                </tr>
                           </table>
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="25" width="100%">
                                <tr>
                                    <td width="100%" bgcolor="#ffffff" style="text-align:left;">
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            It's that time of year again! From November 6th to 8th, 1500 students in Computer Science and related fields are arriving on our campus for <a href="http://www.yhack.org">YHack 2016</a>.  In addition to building some of the coolest things you've ever seen, these students will be showered with free food and swag, win over $40,000 in prizes, get to interact with top tech companies, and participate in fun events including a rap battle, a Super Smash Bros. tournament and a Kinect Dance Battle.
                                        </p>

                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            You will be helping us out on the <b>day of the event</b> to help us fight fires and make sure things go smoothly. If you want to join us for the ride, fill out the following form and we'll be in touch :)
                                        </p>

                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            <a href="https://docs.google.com/a/yale.edu/forms/d/1yS-qXDYPGkg_mKa_IU9j8nr-EpKrBZGg6Cjy-38du2M/viewform?usp=send_form">https://docs.google.com/a/yale.edu/forms/d/1yS-qXDYPGkg_mKa_IU9j8nr-EpKrBZGg6Cjy-38du2M/viewform?usp=send_form</a>
                                        </p>

                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            We'll be holding mandatory volunteer training sessions Monday and Tuesday of next week (11/2 and 11/3), at 8PM  in HLH 17 room 007. Please come to one meeting or the other.
                                        </p>

                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            Thanks so much for helping us make this event great! Looking forward to seeing you all there.
                                        </p>

                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            Best,
                                        </p>

                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            The YHack Team <br />
                                            <a href="http://www.yhack.org">http://www.yhack.org</a>
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            PS: if you help us out, you'll get free meals all weekend, t-shirts, and other swag
                                        </p>
                                     
                                    </td>
                                </tr>
                           </table>
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" width="100%" style="border-bottom-left-radius:5px;border-bottom-right-radius:5px;">
                                <tr>
                                    <td width="50%" bgcolor="#ffffff" style="text-align:left;border-bottom-left-radius:5px;border-bottom-right-radius:5px;padding-right:25px;padding-bottom:10px;padding-left:25px;">
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:11px; line-height:14px; margin-top:15px; margin-bottom:0px; padding:0; font-weight:normal;">
                                            Questions? Contact us at <a href="mailto:team@yhack.org">team@yhack.org</a>.<br>
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:11px; line-height:14px; margin-top:0px; margin-bottom:0px; padding:0; font-weight:normal;">
                                            Copyright 2016 YHack. All Rights Reserved.<br>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                </div>
                </td>
            </tr>
        </table> 
        </body>
    </html>
    """

def buildJoinYHackTeamInfoSessionHTMLEmail():
    return """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>*|MC:SUBJECT|*</title>
            <style type="text/css">
                #outlook a{padding:0;}
                body{width:100% !important; background-color:#ffffff;-webkit-text-size-adjust:none; -ms-text-size-adjust:none;margin:0; padding:0;} 
                .ReadMsgBody{width:100%;} 
                .ExternalClass{width:100%;}
                ol li {margin-bottom:15px;}
                    
                img{height:auto; line-height:100%; outline:none; text-decoration:none;}
                #backgroundTable{height:100% !important; margin:0; padding:0; width:100% !important;}
                    
                p {margin: 1em 0;}
                    
                h1, h2, h3, h4, h5, h6 {color:#222222 !important; font-family:Arial, Helvetica, sans-serif; line-height: 100% !important;}
                    
                table td {border-collapse:collapse;}
                    
                .yshortcuts, .yshortcuts a, .yshortcuts a:link,.yshortcuts a:visited, .yshortcuts a:hover, .yshortcuts a span { color: black; text-decoration: none !important; border-bottom: none !important; background: none !important;}
                    
                .im {color:black;}
                div[id="tablewrap"] {
                        width:100%; 
                        max-width:600px!important;
                    }
                table[class="fulltable"], td[class="fulltd"] {
                        max-width:100% !important;
                        width:100% !important;
                        height:auto !important;
                    }
                            
                @media screen and (max-device-width: 430px), screen and (max-width: 430px) { 
                        td[class=emailcolsplit]{
                            width:100%!important; 
                            float:left!important;
                            padding-left:0!important;
                            max-width:430px !important;
                        }
                    td[class=emailcolsplit] img {
                    margin-bottom:20px !important;
                    }
                }
            </style>
        </head>
        <body style="width:100%; margin:0; padding:0; -webkit-text-size-adjust:none; -ms-text-size-adjust:none;">
        <table cellpadding="0" cellspacing="0" border="0" id="backgroundTable" style="height:auto !important; margin:0; padding:0; width:100% !important; color:#222222;">
            <tr>
                <td>
                <div id="tablewrap" style="width:90% !important; max-width:600px !important; text-align:center; margin:0 auto; padding-bottom:5px; padding-top:15px">
                      <table id="contenttable" width="600" align="center" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF; margin:0 auto; text-align:center; border:none; width: 100% !important; max-width:600px !important;border-bottom-left-radius:5px;border-bottom-right-radius:5px">
                    <tr>
                        <td width="100%">
                            <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="0" width="100%">
                                <tr>
                                    <td width="100%" bgcolor="#ffffff" style="text-align:center;"><a href="http://yhack.org"><img src="https://s3-us-west-2.amazonaws.com/yhack-static/header2.png" style="display:inline-block; max-width:100% !important; width:100% !important; height:auto !important;" border="0"></a>
                                    </td>
                                </tr>
                           </table>
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" cellpadding="25" width="100%">
                                <tr>
                                    <td width="100%" bgcolor="#ffffff" style="text-align:left;">
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:25px; padding:0; font-weight:normal;">
                                            Dear Prospective YHack Family Member,                      
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            Thank you for your interest in joining YHack! We are super excited to meet you and make this year's YHack as great, intense, and fun as possible - we have some really exciting things lined up! For those of you still interested in joining our team, please know that there will be two introductory meetings being held this week:
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            <ul style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; font-weight:normal;">
                                                <li>Thursday, September 10 @8PM in the computer cluster at 17 Hillhouse Room 07</li>
                                                <li>Monday, September 14 @8PM in the computer cluster at 17 Hillhouse Room 07</li>
                                            </ul>
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            Please attend either one, and make sure to bring a computer. We will have a small (non-coding!) task for you to complete to give you a sense of what it may be like to be a YHack member! We will also have dessert :)
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            You can RSVP for one of the days here: <a href="https://docs.google.com/a/yale.edu/forms/d/1c34BhWTSX_VEcr9lMPp28j-pATqNN_M1nJ75EOMU_b4/viewform">https://docs.google.com/a/yale.edu/forms/d/1c34BhWTSX_VEcr9lMPp28j-pATqNN_M1nJ75EOMU_b4/viewform</a>.
                                        </p>


                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            If you absolutely cannot attend either, but are still interested in joining the team, please send a message to team@yhack.org and we will schedule another time to get to know you!
                                        </p>


                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            Hope to see you all there!
                                        </p>
                                        
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            Best,
                                        </p>

                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:15px; line-height:19px; margin-top:0; margin-bottom:20px; padding:0; font-weight:normal;">
                                            Jason Brooks and Kevin Tan<br />
                                            Co-Directors, YHack 2016<br />
                                            <a href="http://www.yhack.org">http://www.yhack.org</a>
                                        </p>
                                     
                                    </td>
                                </tr>
                           </table>
                           <table bgcolor="#FFFFFF" border="0" cellspacing="0" width="100%" style="border-bottom-left-radius:5px;border-bottom-right-radius:5px;">
                                <tr>
                                    <td width="50%" bgcolor="#ffffff" style="text-align:left;border-bottom-left-radius:5px;border-bottom-right-radius:5px;padding-right:25px;padding-bottom:10px;padding-left:25px;">
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:11px; line-height:14px; margin-top:15px; margin-bottom:0px; padding:0; font-weight:normal;">
                                            Questions? Contact us at <a href="mailto:team@yhack.org">team@yhack.org</a>.<br>
                                        </p>
                                        <p style="color:#222222; font-family:Arial, Helvetica, sans-serif; font-size:11px; line-height:14px; margin-top:0px; margin-bottom:0px; padding:0; font-weight:normal;">
                                            Copyright 2016 YHack. All Rights Reserved.<br>
                                        </p>
                                    </td>
                                    <td width="50%" bgcolor="#ffffff" style="text-align:left;border-bottom-left-radius:5px;border-bottom-right-radius:5px;padding-bottom:10px;">
                                        <a href="http://sendgrid.com/?utm_source=Dev%20Rel%20Unspecified&utm_campaign=Email%20Sponsorship&utm_medium=email" style="margin-left:62px;">
                                          <img src="https://s3.amazonaws.com/static.sendgrid.com/mkt/poweredbysendgrid.png" alt="Email Powered By SendGrid" width="200" height="40" />
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                </div>
                </td>
            </tr>
        </table> 
        </body>
    </html>
    """
