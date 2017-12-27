class ApiUrl(object):
    def __init__(self, protocol, port, domain, url, **kwargs):
        self.protocol = protocol
        self.port = port
        self.domain = domain
        self.url = url
        self.kwargs = kwargs

    def __getattr__(self, key):
        return self.kwargs[key]

    def as_dict(self):
        return_val = {
            'protocol': self.protocol,
            'domain': self.domain,
            'port': self.port,
            'url': self.url,
        }

        for key, value in self.kwargs.items():
            return_val[key] = value

        return return_val
