class Responder(object):

    def OK(self, payload, msg=None):
        response = dict()
        response['payload'] = payload
        response['msg'] = msg or 'Success'

        return response
