import json




class Response:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
