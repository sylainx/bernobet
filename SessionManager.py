class SessionManager:
    # Dictionnaire qui stockera les données de la session
    data = {}

    @classmethod
    def setItem(self, key, value):
        self.data[key] = value

    @classmethod
    def getItem(self, key):
        return self.data.get(key)

    @classmethod
    def removeItem(self, key):
        if key in self.data:
            del self.data[key]

    @classmethod
    def clear(self):
        self.data = {}
