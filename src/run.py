import json

import sys

import treq
from apple import AppleNotification
from klein import Klein
from nightbook import Nightbook
from shared import Responder
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.python import log

app = Klein()
nb = Nightbook(url='http://dev.nightbook.me/')


@app.route('/api/status/', methods=['GET'])
@inlineCallbacks
def status(request):
    request.setHeader('Content-Type', 'application/json')
    r = yield treq.get(nb.status())
    content = yield r.json()

    returnValue(Responder().OK(json.dump(content)))


@app.route('/api/notify/', methods=['POST'])
def notify(request):
    application = request.args.get('application')
    message = request.args.get('message')
    sound = request.args.get('sound') or 'default'
    badge = request.args.get('badge') or 1
    platform = request.args.get('platform') or None
    token = request.data.get('token')

    request.setHeader('Content-Type', 'application/json')
    if platform[0] == 'APPLE':
        notify = AppleNotification(application=application, token=token, content=dict(alert=message[0], sound=sound, badge=badge))
        notify.send()


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    app.run("localhost", 8080)