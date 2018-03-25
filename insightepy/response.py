class Response(object):
    def __init__(self, params):
        self.message = params['message']
        self.data = params['data'] if 'data' in params else {}
        self.status = params['status']

    def __repr__(self):
        return 'Response[message="{}", data={}]'.format(self.message, self.data)
