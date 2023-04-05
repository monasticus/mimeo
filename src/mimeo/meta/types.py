class Singleton(type):

    __INSTANCE = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__INSTANCE:
            instance = super().__call__(*args, **kwargs)
            cls.__INSTANCE[cls] = instance
        return cls.__INSTANCE[cls]
