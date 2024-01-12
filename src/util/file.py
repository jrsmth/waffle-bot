import json


# File wrapper functionality
class File:

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path) as file:
            return json.load(file)

    def write(self, content):
        with open(self.file_path, 'w') as outfile:
            json.dump(content, outfile)
