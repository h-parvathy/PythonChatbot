class TemplateReader:
    def __init__(self):
        pass

    def read_template(self, mail_type):
        try:
            if (mail_type== 'report'):
                email_file = open("EmailSend/graphs.html", "r")
                email_message = email_file.read()

            elif (mail_type == 'country'):
                email_file = open("EmailSend/DLM_Template.html", "r")
                email_message = email_file.read()
            elif (mail_type == 'simple'):
                email_file = open("EmailSend/simple.html", "r")
                email_message = email_file.read()
            return email_message
        except Exception as e:
            print('The exception is '+str(e))
