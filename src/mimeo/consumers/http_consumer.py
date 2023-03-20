from mimeo.consumers import Consumer


class HttpConsumer(Consumer):

    def consume(self, data: str) -> None:
        print(data)
