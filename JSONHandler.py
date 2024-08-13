import json

class JSONHandler:
    def __init__(self, filename):
        self.filename = filename

    def write_data(self, data_list):
        with open(self.filename, 'w') as file:
            json.dump(data_list, file, indent=4)

    def read_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return []

    def update_data(self, index, key, value):
        data_list = self.read_data()
        if 0 <= index < len(data_list):
            data_list[index][key] = value
            self.write_data(data_list)

    def add_entry(self, new_entry):
        data_list = self.read_data()
        data_list.append(new_entry)
        self.write_data(data_list)

    def remove_entry(self, index):
        data_list = self.read_data()
        if 0 <= index < len(data_list):
            removed_entry = data_list.pop(index)
            self.write_data(data_list)