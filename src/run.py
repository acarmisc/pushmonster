import sys
import logging
from notifications import Notification
from klein import Klein

from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.python import log
import json
from db import Application

app = Klein()


@app.route('/api/notify/', methods=['POST'])
@inlineCallbacks
def notify(request):
    try:
        app_key = request.getHeader('Authorization').split(' ')[1]
    except:
        # TODO: handle this
        returnValue('KO')
    
    log.msg(request.args)
    response = yield send_now(app_key, request)

    returnValue('OK')


@inlineCallbacks
def send_now(app_key, request):
    app = Application(key=app_key).auth()

    message = request.args.get('message')[0]
    sound = request.args.get('sound')[0] or 'default'
    badge = request.args.get('badge') or 0
    token = request.args.get('token')[0]
    extra = request.args.get('extra')[0]

    request.setHeader('Content-Type', 'application/json')

    content = dict(alert=message, sound=sound, badge=badge, extra=json.loads(extra))
    if app:
        log.msg('application found: %s' % app.name)
        notification = Notification(token=token, app=app, content=content)
        notification.send()

    else:
        log.msg('No application found with key %s' % app_key[1], logLevel=logging.WARNING)

    yield 'OK'


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    app.run("0.0.0.0", 8080)
