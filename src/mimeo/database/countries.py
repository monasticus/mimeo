class Country:

    def __init__(self, iso_3: str, iso_2: str, name: str):
        self.iso_3 = iso_3
        self.iso_2 = iso_2
        self.name = name

    def __str__(self) -> str:
        return str({
            "iso_3": self.iso_3,
            "iso_2": self.iso_2,
            "name": self.name
        })

    def __repr__(self) -> str:
        return f"Country('{self.iso_3}', '{self.iso_2}', '{self.name}')"
