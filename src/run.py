import json
import logging
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

logger = logging.getLogger(__name__)


@app.route('/api/status/', methods=['GET'])
@inlineCallbacks
def status(request):
    request.setHeader('Content-Type', 'application/json')
    r = yield treq.get(nb.status())
    content = yield r.json()

    returnValue(Responder().OK(json.dump(content)))


@app.route('/api/notify/', methods=['POST'])
def notify(request):

    # TODO: check token to auth and resolve application data

    app_key = request.getHeader('authorization').split(' ')

    if app_key[1] == '25bbdcd06c32d477f7fa1c3e4a91b032': app = 'it.infoporto.nightbook-apple'
    if app_key[1] == 'fcd04e26e900e94b9ed6dd604fed2b64': app = 'it.infoporto.nightbook-android'

    message = request.args.get('message')
    sound = request.args.get('sound')[0] or 'default'
    badge = request.args.get('badge') or None
    token = request.args.get('token')[0]

    logger.debug('data: %s, %s, %s' % (token, message, sound))

    request.setHeader('Content-Type', 'application/json')
    if app == 'it.infoporto.nightbook-apple':
        notify = AppleNotification(application=app, token=token, content=dict(alert=message[0], sound=sound, badge=badge))

    if app == 'it.infoporto.nightbook-android':
        notify = AndroidNotification(application=app, token=token, content=dict(alert=message[0], sound=sound, badge=badge))

    notify.send()


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    app.run("localhost", 8080)
