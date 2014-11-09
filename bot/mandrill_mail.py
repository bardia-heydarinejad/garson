# -*- coding: utf-8 -*-

# python import
import mandrill


class MandrillContact(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email


class MandrillEmail(object):
    def __init__(self):
        self.api_key = 'Q5effNYEhFq41PpZ2rUUqg'
        self.domains = ['rishe.co']
        self.mail = 'noreply@rishe.co'
        self.name = 'Garson'

    def send(self, subject, to_contacts, message, async=True):
        try:
            mandrill_client = mandrill.Mandrill(self.api_key)
            message = {
                'inline_css': True,
                'html': message,
                'from_email': self.mail,
                'from_name': self.name,
                'subject': subject,
                'to': [{'email': to.email,
                        'name': to.name,
                        'type': 'to'} for to in to_contacts],
                'google_analytics_domains': self.domains,
            }

            return mandrill_client.messages.send(message=message, async=async)

        except mandrill.Error as e:
            # Mandrill errors are thrown as exceptions
            print('A mandrill error occurred: %s - %s' % (e.__class__, e))
            raise


if __name__ == '__main__':
    tos=[]
    tos.append(MandrillContact('bardia', 'az.bardia13@gmail.com'))
    tos.append(MandrillContact('bardia', 'bardia.heydarinejad@gmail.com'))
    mandrillCli = MandrillEmail()
    print(mandrillCli.send('no fucking subject', tos, "Fuck you"))
