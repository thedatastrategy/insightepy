class Response(object):
    def __init__(self, data):
        self.message = data['message']
        self.data = data['data']
        self.status = data['status']

    def __repr__(self):
        return 'Response[message="{}", data={}]'.format(self.message, self.data)
