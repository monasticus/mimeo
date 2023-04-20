class FirstName:

    def __init__(self, name: str, sex: str):
        self.name = name
        self.sex = sex

    def __str__(self) -> str:
        return str({
            "name": self.name,
            "sex": self.sex
        })

    def __repr__(self) -> str:
        return f"FirstName('{self.name}', '{self.sex}')"
