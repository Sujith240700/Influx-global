from flask import Flask,render_template
from flask import request,session

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os



UPLOAD_FOLDER = '/path/to/the/uploads'
app=Flask(__name__)
app_root = os.path.dirname(os.path.abspath(__file__))
app.secret_key="sj@#$240700"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["FILE_UPLOADS"] = "/mnt/c/wsl/projects/pythonise/tutorials/flask_series/app/app/static/img/uploads"

def send_email(name,mailid,number,docname,docname1,message):
    try:
        mail_content = '''<html><head> </head><body><div class="card" style="border:2px solid black;box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);max-width: 300px;margin: auto;text-align: center;font-family: arial;"><h5 style="padding-left: 25px;text-align: left;">Name : {}</h5><h5 style="
                    padding-left: 25px;
                    text-align: left;
                    ">Mail id : {}</h5><h5 style="padding-left: 25px;text-align: left;">Phone number : {}</h5><h5 style="padding-left: 25px;text-align: left;">Message : {}</h5><h5 style="padding-left: 25px;text-align: left;">Resume {}, attached below</h5>
                    <div><a href="mailto:{}" style="
                    text-decoration: none;
                    font-size: 22px;
                    color: black;
                "><button style="    cursor: pointer;text-align: center;border: none;outline: 0;display: inline-block;padding: 8px;color: white;background-color: #000;text-align: center;cursor: pointer;width: 100%;font-size: 18px;display: flex;align-items: center;justify-content: center;"><svg width="33" height="22" viewBox="0 0 63 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M56.0656 0.350098H6.22951C2.80328 0.350098 0.0311475 3.22682 0.0311475 6.74283L0 45.0992C0 48.6152 2.80328 51.4919 6.22951 51.4919H56.0656C59.4918 51.4919 62.2951 48.6152 62.2951 45.0992V6.74283C62.2951 3.22682 59.4918 0.350098 56.0656 0.350098ZM56.0656 45.0992H6.22951V13.1356L31.1475 29.1174L56.0656 13.1356V45.0992ZM31.1475 22.7246L6.22951 6.74283H56.0656L31.1475 22.7246Z" fill="#FD5E53"></path>
                                        </svg><p style="text-align:center">Send mail</p></button></a>
                                        <a href="tel:{}" style="
                    text-decoration: none;
                    font-size: 22px;
                    color: black;
                "><button style="    cursor: pointer;    border: none;    outline: 0;    display: inline-block;    padding: 8px;    color: white;   background-color: #000;    text-align: center;    cursor: pointer;    width: 100%;    font-size: 18px;    display: flex;    align-items: center;    justify-content: center;"><svg width="30" height="32" viewBox="0 0 60 62" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M5.57769 16.0366L5.57787 16.0371C8.73971 25.2596 13.8839 33.6322 20.628 40.5342L20.6288 40.535C27.3536 47.4567 35.5096 52.735 44.4917 55.979C46.5085 56.707 48.8354 56.105 50.4953 54.4014L54.2543 50.5434L5.57769 16.0366ZM5.57769 16.0366C4.86036 13.9537 5.4568 11.5553 7.11766 9.85067L10.8769 5.99233C11.0844 5.77967 11.3329 5.61534 11.6056 5.50955C11.8782 5.40378 12.1693 5.35879 12.4596 5.37727C12.75 5.39576 13.0336 5.47736 13.2918 5.61712C13.55 5.75684 13.7771 5.95167 13.9577 6.18934L5.57769 16.0366ZM54.0591 47.3517L54.0591 47.3517L45.6799 40.661C45.4329 40.4639 45.1462 40.3276 44.8417 40.2615C44.5372 40.1954 44.2221 40.2012 43.9201 40.2784L35.9676 42.3189C34.8366 42.6096 33.6514 42.5946 32.5278 42.2755C31.4042 41.9564 30.3815 41.3444 29.5587 40.5002L29.5586 40.5001L20.6367 31.3391C20.6367 31.3391 20.6367 31.3391 20.6367 31.3391C19.8143 30.4947 19.2199 29.4471 18.9103 28.2987C18.6007 27.1503 18.5862 25.9395 18.8681 24.7837C18.8681 24.7837 18.8681 24.7836 18.8681 24.7836L20.8562 16.6215L54.0591 47.3517ZM54.0591 47.3517C54.2902 47.5362 54.4812 47.7695 54.6189 48.0367C54.7565 48.304 54.8376 48.5987 54.8562 48.9013C54.8748 49.204 54.8305 49.5071 54.7265 49.7903C54.6226 50.0734 54.4616 50.3298 54.2547 50.5429L54.0591 47.3517ZM8.25048 2.01071C8.76605 1.60864 9.33698 1.28367 9.94638 1.0473C10.8413 0.70017 11.7983 0.552207 12.7537 0.613494C13.7091 0.674781 14.6405 0.943871 15.4859 1.40245C16.3313 1.86101 17.0713 2.49839 17.6571 3.27169L24.1717 11.8713C24.1718 11.8714 24.172 11.8716 24.1721 11.8717C25.4432 13.5439 25.8902 15.7242 25.3892 17.777C25.3892 17.7771 25.3891 17.7772 25.3891 17.7773L23.4009 25.9436L23.4009 25.9438C23.3134 26.3021 23.3179 26.6778 23.4138 27.0337C23.5097 27.3896 23.6934 27.7128 23.9459 27.9723L8.25048 2.01071ZM8.25048 2.01071V1.91763L7.56413 2.62135L3.80468 6.47591L3.80434 6.47626C1.02463 9.33335 -0.209215 13.6133 1.1624 17.6171L1.16246 17.6173C4.55693 27.5125 10.0786 36.4972 17.3188 43.9048C24.5367 51.3348 33.2925 57.0024 42.9371 60.4866L42.9372 60.4866C46.8517 61.8993 51.0318 60.6259 53.8123 57.7721L57.5715 53.9138L8.25048 2.01071ZM32.8755 37.1294L23.9462 27.9726L57.5717 53.9135C60.4336 50.9803 60.1389 46.1347 56.9418 43.5839C56.9418 43.5839 56.9417 43.5839 56.9417 43.5839L48.5626 36.8972C47.756 36.2531 46.8165 35.8052 45.815 35.588C44.8134 35.3709 43.7768 35.3903 42.7838 35.6449L42.7837 35.6449L34.8307 37.6855L34.8305 37.6856C34.4863 37.7741 34.1257 37.7696 33.7836 37.6725C33.4414 37.5754 33.1284 37.3887 32.8755 37.1294ZM13.9579 6.18963L20.4804 14.7933C20.4804 14.7934 20.4805 14.7934 20.4805 14.7935C20.6732 15.048 20.8077 15.3449 20.8729 15.6619C20.9382 15.9788 20.9325 16.3069 20.8563 16.6211L13.9579 6.18963Z" fill="#FD5E53" stroke="#FD5E53" stroke-width="0.8"></path>
                                        </svg><p style="text-align:center">Make a phone call</p>
                                    </button></a></div>
                    </div></body></html>'''.format(name,mailid,number,message,docname,mailid,number)


        #The mail addresses and password
        sender_address = 'server.mailbridge@gmail.com'
        sender_pass = 'fwsujrovkmlxmfqm'
        receiver_address = 'influxglobalsolutions@gmail.com'
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Message from InfluxGlobalSolutions.tk'
        #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))

        attach_file = open(docname1, 'rb') # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) #encode the attachment
        #add payload header with filename
        payload.add_header('Content-Disposition','attachment; filename="%s"' % docname)
        message.attach(payload)
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
        os.remove(docname)

    except Exception as e:
        print(e)

def send_email_user(name,mailid):
    try:
        mail_content = '''<html><head> </head><body><div class="card" style="border:2px solid black;box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);max-width: 300px;margin: auto;text-align: center;font-family: arial;"><img src="https://sujithsportfolio.pythonanywhere.com/static/img/logo.jpg" style="
    margin: 10px;
">
                    <div>
                        <h5 style="padding-left: 25px;text-align: left;">Thanks {},Your response has been submitted successfully</h5><button style="    cursor: pointer;text-align: center;border: none;outline: 0;display: inline-block;padding: 8px;color: white;background-color: #000;text-align: center;cursor: pointer;width: 100%;font-size: 18px;display: flex;align-items: center;justify-content: center;"><svg width="33" height="22" viewBox="0 0 63 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M56.0656 0.350098H6.22951C2.80328 0.350098 0.0311475 3.22682 0.0311475 6.74283L0 45.0992C0 48.6152 2.80328 51.4919 6.22951 51.4919H56.0656C59.4918 51.4919 62.2951 48.6152 62.2951 45.0992V6.74283C62.2951 3.22682 59.4918 0.350098 56.0656 0.350098ZM56.0656 45.0992H6.22951V13.1356L31.1475 29.1174L56.0656 13.1356V45.0992ZM31.1475 22.7246L6.22951 6.74283H56.0656L31.1475 22.7246Z" fill="#FD5E53"></path>
                                        </svg><p style="text-align:center">Send mail</p></button></a>
                                        <a href="mailto:influxglobalsolutions@gmail.com" style="
                    text-decoration: none;
                    font-size: 22px;
                    color: black;
                "></div>
                    </div></body></html>'''.format(name)


        #The mail addresses and password
        sender_address = 'server.mailbridge@gmail.com'
        sender_pass = ''
        receiver_address = mailid
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Message from InfluxGlobalSolutions.tk'
        #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))


        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as e:
        print(e)


@app.route("/",methods=['GET','POST'] )
def home():
    """return "This site may be temporarily down, so please contact the administrator."""
    target = os.path.join(app_root, 'static/')
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['ph'] = request.form['ph']
        session['message'] = request.form['message']
        file = request.files['resume']
        file.save(file.filename)
        send_email(session['name'],session['email'],session['ph'],file.filename,file.filename,session['message'])
        send_email_user(session['name'],session['email'])
        return render_template("index.html")

@app.route("/RecruitmentServices")
def RecruitmentServices():
    """return "This site may be temporarily down, so please contact the administrator."""
    return render_template("2.html")

@app.route("/BusinessSolutions")
def BusinessSolutions():
    """return "This site may be temporarily down, so please contact the administrator."""
    return render_template("1.html")

@app.route("/SoftskilltrainingandcareerGuidance")
def SoftskilltrainingandcareerGuidance():
    """return "This site may be temporarily down, so please contact the administrator."""
    return render_template("4.html")


@app.route("/HRAdvisoryConsulting")
def HRAdvisoryConsulting():
    """return "This site may be temporarily down, so please contact the administrator."""
    return render_template("3.html")




if __name__ == "__main__":
    app.run()


