import time
from apns import APNs, Frame, Payload
from db import Application
from gcm import GCM


class Notification(object):

    def __init__(self, token, application, content):
        #self.application = application ... fetched from db
        self.application = Application(code_name=application, cert_file='nbdev_cert.pem', cert_key='nbdev_key.pem', debug=True)
        self.content = content
        self.token = token


class AppleNotification(Notification):

    def send(self):
        apns = APNs(use_sandbox=self.application.debug, cert_file=self.application.cert_file, key_file=self.application.cert_key)

        # Send a notification
        payload = Payload(alert=str(self.content.get('alert')), sound=self.content.get('sound'), badge=self.content.get('badge'))
        apns.gateway_server.send_notification(self.token, payload)


class AndroidNotification(Notification):

    def send(self):
        gcm = GCM('AIzaSyDfRGJLpgBOjIBb_t-Ka78JoWcw4j5Gw_o')
        # Send a notification
        gcm.plaintext_request(registration_id=self.token, data=dict(message=str(self.content.get('alert'))))


if __name__ == '__main__':
    apns = APNs(use_sandbox=True, cert_file='nbdev_cert.pem', key_file='nbdev_key.pem')
    token_hex = '977c04b62db07fc5920aa04c2495adb0b8cdc5cf390ab1e0ef8d6315cfe506a2'
    payload = Payload(alert='cao', sound='chime', badge=1)
    apns.gateway_server.send_notification(token_hex, payload)
