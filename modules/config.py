import json

class Config:
    def __init__(self, file_name):
        self.file_name = file_name
        self.config_dict = self.load_file()

    def load_file(self):
        try:
            with open(self.file_name, 'r') as json_file:
                return json.load(json_file)
        except:
            print('*** could not load configuration file %s' % self.file_name)
            return []

    def get_value(self, key):
        if key in self.config_dict:
            return self.config_dict[key]
        else:
            return None
