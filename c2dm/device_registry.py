import csv


class DeviceRegistry():
    
    csv_dialect = csv.excel

    def __init__(self, registry_file_name = 'registry.csv'):
        self.registry_file_name = registry_file_name

    def save_device_registration(self, node_id, registration_id):
        file = open(self.registry_file_name, 'a')
        writer = csv.writer(file, self.csv_dialect)
        row = [node_id, registration_id]
        writer.writerow(row)
        file.close()

    def change_registration_id_for_node(self, node_id, registration_id):
        file = open(self.registry_file_name, 'r')
        reader = csv.reader(file, self.csv_dialect)
        parser = ValueParser()
        rows = []
        for row in reader:
            rows.append(
                    parser.replace_value_if_key_matches(
                            row, node_id, registration_id))
        file.close()
        file = open(self.registry_file_name, 'w')
        writer = csv.writer(file, self.csv_dialect)
        writer.writerows(rows)
        file.close()

    def lookup_registration_id_for_mds(self, mds):
        file = open(self.registry_file_name, 'r')
        reader = csv.reader(file, self.csv_dialect)
        for row in reader:
            if(mds == row[0]):
                file.close()
                return row[1]
        file.close()


class ValueParser():
    
    def replace_value_if_key_matches(self, values_pair, key, new_value):
        if(values_pair[0] == key):
            return (key, new_value)
        return values_pair

class DeviceNotRegisterdError(Exception):
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
