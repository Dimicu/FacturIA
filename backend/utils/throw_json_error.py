class throw_json_error:
    def __init__(self, error_message, status_code=int):
        self.error_message = error_message
        self.status_code = status_code

    def to_json(self):
        return {"error": self.error_message, "status_code": self.status_code}
