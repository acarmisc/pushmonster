from apns import APNs, Payload
from db import Application
from gcm import GCM

from twisted.internet.defer import Deferred

from twisted.python import log


class Notification(object):

    def __init__(self, token, app, content):
        self.token = token
        self.app = app
        self.content = content

    def send(self):
        log.msg('Trying to send to %s... using %s on %s' % (self.token[:8], self.app.name, self.app.platform))

        recipients = self.token.split(',')
        for r in recipients:
            if self.app.platform == 'ANDROID':
                AndroidNotification(r, self.app, self.content).send()

            if self.app.platform == 'APPLE':
                AppleNotification(r, self.app, self.content).send()

        return Deferred


class AppleNotification(Notification):

    def send(self):
        apns = APNs(use_sandbox=self.app.debug,
                    cert_file=self.app.cert_file,
                    key_file=self.app.cert_key)

        payload = Payload(alert=str(self.content.get('alert')),
                          sound=self.content.get('sound'),
                          badge=self.content.get('badge'),
                          custom=self.content.get('extra')
                          )
        
        apns.gateway_server.send_notification(self.token, payload)
        log.msg('Notification sent to %s...' % self.token[:3])


class AndroidNotification(Notification):

    def send(self):
        gcm = GCM(self.app.android_key)
        payload = dict(message=str(self.content.get('alert')), custom=self.content.get('extra'))
        log.msg(payload)

        gcm.plaintext_request(registration_id=self.token, data=payload)
        log.msg('Notification sent to %s...' % self.token[:3])


if __name__ == '__main__':

    app = Application(key='1234', id=1).auth()

    content = dict(alert='ciao mondo!', sound='default', badge=3)

    notification = Notification(token='977c04b62db07fc5920aa04c2495adb0b8cdc5cf390ab1e0ef8d6315cfe506a2',
                                application=app,
                                content=content)
    notification.send()
