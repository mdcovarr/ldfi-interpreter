"""
    Create a client connection to Book Info frontend
    in order to support 3MileBeach Integration. And
    the ability to orchestrate fault injection and tracing
"""
import http
import uuid
import time
import simplejson as json
import os

"""
    Constants
"""
SEND = 1
RECV = 2
CWD = os.path.dirname(os.path.realpath(__file__))


class Client:
    """
        HTTP Client used to orchestrate 3MileBeach
    """
    def __init__(self, host, port):
        """
            Default Constructor
        """
        self.conn = None
        self.requests = None
        self.host = host
        self.port = port
        self.address = "{0}:{1}".format(host, port)
        self.uuid = "client-{}".format(uuid.uuid4().hex)
        self.trace_dir = os.path.join(CWD, "..", "traces")

    def init(self):
        self.conn = http.client.HTTPConnection(self.host, int(self.port))
        self.conn.connect()

    def generate_record(self, **kwargs):
        """
            Used to generate a record. Request or Response
            for the client Rest HTTP connection
        """
        return {
            "message_name": kwargs["message_name"],
            "service": kwargs["service"],
            "timestamp": int(time.time()),
            "type": kwargs["type"],
            "uuid": kwargs["uuid"]
        }

    def run(self):
        """
            request(method, url, body=None, headers={}, ...)
        """
        # Iterate throught each request/trace
        i = 0
        for request in self.requests["requests"]:
            fi_trace = {
                "id": uuid.uuid4().hex,
                "records": [],
                "tfis": []
            }

            trace_outfile = os.path.join(CWD, "..", "traces/trace-{}.json".format(i))

            # 1. Create connection
            cookie_url = request["cookie_url"]
            self.conn = http.client.HTTPConnection(cookie_url)
            self.conn.connect()

            # Each top level request/trace can be composed of
            # other requests
            for inner_request in request["requests"]:
                # Get request paramerters
                method = inner_request["method"]
                url = inner_request["URL"]
                message_name = inner_request["message_name"]

                # Add record of Request
                request_message_name = "{} {}".format(message_name, "Request")
                fi_trace["records"].append(self.generate_record(uuid=fi_trace["id"], type=SEND, message_name=request_message_name, service=self.uuid))

                # Send Request
                headers = {
                    "fi-trace": json.dumps(fi_trace)
                }
                self.conn.request(method, url, headers=headers)

                # Get Response
                response = self.conn.getresponse()
                data = response.read()
                data = response.headers["fi-trace"]
                fi_trace = json.loads(data)

                # Add record of Response
                response_message_name = "{} {}".format(message_name, "Response")
                fi_trace["records"].append(self.generate_record(uuid=fi_trace["id"], type=RECV, message_name=response_message_name, service=self.uuid))

            # Output trace information
            outfile = open(trace_outfile, "w+")
            outfile.write(json.dumps(fi_trace, indent=4, sort_keys=True))
            outfile.close()

            # Create DAG and output
            self.conn.close()


    def clear_trace_data(self):
        """
            Clearning out old stale trace information
            in traces directory
        """
        for path in os.listdir(self.trace_dir):
            full_path = os.path.join(self.trace_dir, path)

            if os.path.isfile(full_path):
                os.remove(full_path)


    def import_requests(self, filename):
        """
            Helper function used to import
            3MileBeach requests
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.requests = data
        except Exception as e:
            print(e)


def main():
    client = Client("127.0.0.1", 8090)
    client.import_requests(os.path.join(CWD, "..", "requests/request-0.json"))
    client.clear_trace_data()
    client.run()


if __name__ == "__main__":
    main()
