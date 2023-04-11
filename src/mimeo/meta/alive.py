from mimeo.meta.exc import InstanceNotAlive


class Alive:

    def __init__(self):
        self._alive = False

    def __enter__(self):
        self._alive = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._alive = False
        return None

    def assert_alive(self):
        if not self.is_alive():
            raise InstanceNotAlive("The instance is not alive!")
        return self.is_alive()

    def is_alive(self):
        return self._alive


class OnlyOneAlive(type):

    __INSTANCES = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__INSTANCES:
            cls.__INSTANCES[cls] = []

        alive_instance = next((instance for instance in cls.__INSTANCES[cls] if instance.is_alive()), None)
        if alive_instance is not None:
            return alive_instance
        else:
            instance = super().__call__(*args, **kwargs)
            cls.__INSTANCES[cls].append(instance)
            return instance
