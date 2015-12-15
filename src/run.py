import sys
import logging
from notifications import Notification
from klein import Klein
from twisted.internet.defer import Deferred

# from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.python import log

from db import Application

app = Klein()


@app.route('/api/notify/', methods=['POST'])
def notify(request):
    try:
        app_key = request.getHeader('Authorization').split(' ')[1]
    except:
        # TODO: handle this
        return

    app = Application(key=app_key).auth()

    message = request.args.get('message')[0]
    sound = request.args.get('sound')[0] or 'default'
    badge = request.args.get('badge') or 0
    token = request.args.get('token')[0]

    request.setHeader('Content-Type', 'application/json')

    content = dict(alert=message, sound=sound, badge=badge)
    if app:
        d = Deferred()
        notification = Notification(token=token, app=app, content=content)
        d.addCallback(notification.send())
        d.callback(None)

    else:
        log.msg('No application found with key %s' % app_key[1], logLevel=logging.WARNING)


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    app.run("0.0.0.0", 8080)
