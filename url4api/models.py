class ApiUrl(object):
    def __init__(self, version, url, protocol, port, domain):
        self.version = version
        self.url = url
        self.protocol = protocol
        self.domain = domain
        self.port = port

    def as_dict(self):
        return {
            'version': self.version,
            'url': self.url,
            'protocol': self.protocol,
            'domain': self.domain,
            'port': self.port,
        }
