"""
    Create a client connection to Book Info frontend
"""
import http
import uuid


class RestClient:
    def __init__(self, host, port):
        self.client = None
        self.host = host
        self.port = port
        self.address = "{0}:{1}".format(host, port)
        self.uuid = uuid.uuid4()

    def init(self):
        self.conn = http.client.HTTPConnection(self.host, int(self.port))
        self.conn.connect()

    def run(self):
        """
            request(method, url, body=None, headers={}, ...)
        """
        header = {
            'FI_TRACE': 'true'
        }
        self.conn.request("GET", "/productpage")
        response = self.conn.getresponse()
        data = response.read()
        headers = response.getheaders()
        print("Status: {}".format(response.status))
        self.conn.close()


if __name__ == "__main__":
    client = RestClient("localhost", 80)
    client.init()
    client.run()
