class Nightbook(object):

    def __init__(self, url):
        self.base_url = url

    def status(self):
        return "%s/%s" % (self.base_url, '/api/commons/status/')