import treq
from klein import Klein
from twisted.internet import reactor, defer
from twisted.internet.defer import inlineCallbacks, returnValue

app = Klein()


@inlineCallbacks
def async(arg):
    print "1:%s" % arg
    yield 'ciao'


@app.route('/', branch=True)
@inlineCallbacks
def tester(request):
    a = yield async(request.args.get('k'))
    print a
    
    returnValue('ciao')
    

app.run("localhost", 8080)