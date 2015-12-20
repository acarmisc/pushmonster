from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
import treq

@inlineCallbacks
def get_url(url):
    print "Getting URL %s" % url

    try:
        resp = yield treq.get(url)
        print "Got response code %d from %s" % (resp.code, url)    
    except Exception as e:
        print "Something failed: %s" % str(e)


def main(reactor, *args):    
    url = 'http://localhost:8080/api/testme'
    d = get_url(url)    
    return d

def requestFactory():
    for i in range (0, 15):
        import random
        deferred = treq.get('http://localhost:8080/?k=%s' % i)
        deferred.addCallback(lambda x:x)        
        print('Generated %s' % i)
        reactor.iterate(1)


startTimeStamp = reactor.seconds()
reactor.callWhenRunning(requestFactory)
reactor.run()