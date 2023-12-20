import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from dotenv import load_dotenv

load_dotenv()
print("TWILIO_ACCOUNT_SID:", os.environ.get('TWILIO_ACCOUNT_SID'))
print("TWILIO_AUTH_TOKEN:", os.environ.get('TWILIO_AUTH_TOKEN'))
print("TWILIO_VERIFY_SERVICE_SID:", os.environ.get('TWILIO_VERIFY_SERVICE_SID'))

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
# service = client.verify.v2.services.create(friendly_name='My Verify Service')

service = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])
print(service,"verifyyyyy")

# sendin otp to phone using twilio service
def send(phone):
    service.verifications.create(to=phone, channel='sms')
    print(phone)


# verifying code sent and code given by user
def check(phone, code):
    try:
        print(phone,code)
        # formatted_phone = f"+91{phone}"  # Assuming phone is a string without a leading '+'
        # print(f"Checking code: {code} for formatted phone: {formatted_phone}")
        result = service.verification_checks.create(to=phone, code=code)
        print(result,"k")
    except TwilioRestException as e:
        print(f"TwilioRestException: {e}")
        print(f"TwilioRestException Code: {e.code}")
        print(f"TwilioRestException Message: {e.msg}")
        
        return False
    return result.status=='approved'
















# class EmailThread(threading.Thread):

#     def __init__(self, email):
#         self.email = email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()

# class Util:
#     @staticmethod
#     def send_email(data):
#         email = EmailMessage(
#             subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
#         EmailThread(email).start()

# class EmailUtils:
#     @staticmethod
#     def send_password_reset_email(email_subject, email_body, to_email):
#         email = EmailMessage(
#             subject=email_subject,
#             body=email_body,
#             to=[to_email]
#         )
#         EmailThread(email).start()