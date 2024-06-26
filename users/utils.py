from django.core.mail import EmailMessage


class Mail:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data["email_subject"], body=data["email_body"], to=data["to_email"]
        )
        email.send()
