import json

import sys

import treq
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


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    app.run("localhost", 8080)