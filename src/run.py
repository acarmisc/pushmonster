import json
import sys
import logging
from notifications import Notification
from klein import Klein
from shared import Responder
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.python import log

from db import Application

app = Klein()


@app.route('/api/notify/', methods=['POST'])
def notify(request):

    # TODO: check token to auth and resolve application data

    app_key = request.getHeader('Authorization').split(' ')

    app = Application(key=app_key[1]).auth()

    message = request.args.get('message')[0]
    sound = request.args.get('sound')[0] or 'default'
    badge = request.args.get('badge') or 0
    token = request.args.get('token')[0]

    log.msg('data: %s, %s, %s' % (token, message, sound), logLevel=logging.DEBUG)

    request.setHeader('Content-Type', 'application/json')

    content = dict(alert=message, sound=sound, badge=badge)
    if app:
        notification = Notification(token=token, app=app, content=content)
        notification.send()
    else:
        log.msg('No application found with key %s' % app_key[1], logLevel=logging.WARNING)


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    app.run("localhost", 8080)
