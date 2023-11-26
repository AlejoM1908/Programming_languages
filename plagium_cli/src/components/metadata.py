import json

class Metadata:
    def __init__(self, filename):
        self.filename = filename
        
        try:
            with open(filename, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {
                "new_user": True
            }

    def __enter__(self):
        return self.data
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            with open(self.data['path'], "w") as file:
                json.dump(self.data, file)
        except FileNotFoundError:
            pass
        except KeyError:
            pass