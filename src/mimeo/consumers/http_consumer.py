from requests import Response, Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from mimeo.config.mimeo_config import MimeoOutputDetails
from mimeo.consumers import Consumer


class HttpConsumer(Consumer):

    def __init__(self, output_details: MimeoOutputDetails):
        self.method = output_details.method
        self.url = HttpConsumer.__build_url(output_details)
        if output_details.auth == "basic":
            self.__auth = HTTPBasicAuth(output_details.username, output_details.password)
        else:
            self.__auth = HTTPDigestAuth(output_details.username, output_details.password)

    def consume(self, data: str) -> Response:
        with Session() as sess:
            if self.method == "POST":
                return sess.post(self.url, auth=self.__auth, data=data)
            elif self.method == "PUT":
                return sess.put(self.url, auth=self.__auth, data=data)

    @staticmethod
    def __build_url(output_details: MimeoOutputDetails):
        if output_details.port is None:
            return f"{output_details.protocol}://{output_details.host}{output_details.endpoint}"
        else:
            return f"{output_details.protocol}://{output_details.host}:{output_details.port}{output_details.endpoint}"
