import csv
import unittest
import os

from device_registry import DeviceRegistry, ValueParser


class  DeviceRegistryTestCase(unittest.TestCase):
    file_name = 'test.csv'
    node_id = "node"
    registration_id = "registration"

    def test_save_device_registration(self):
        registry = DeviceRegistry(self.file_name)
        registry.save_device_registration(self.node_id, self.registration_id)
        reader = csv.reader(open(self.file_name, 'r'), csv.excel)
        for row in reader:
            self.assertEquals(self.node_id, row[0])
            self.assertEquals(self.registration_id, row[1])

    def test_change_registration_id_for_node(self):
        registry = DeviceRegistry(self.file_name)
        registry.save_device_registration(self.node_id, self.registration_id)
        registry.save_device_registration('node_id_2', 'registration_id_2')
        registry.save_device_registration('node_id_3', 'registration_id_3')
        new_registration_id = 'new_registration_id'
        registry.change_registration_id_for_node(
                self.node_id, new_registration_id)

        reader = csv.reader(open(self.file_name, 'r'), csv.excel)
        for row in reader:
            self.assertEqual(self.node_id, row[0])
            self.assertEqual(new_registration_id, row[1])
            break

    def test_lookup_registration_id_for_mds(self):
        registry = DeviceRegistry(self.file_name)
        registry.save_device_registration("node1", "registration1")
        registry.save_device_registration("node2", "registration2")
        node_to_be_found = "node"
        registry_key_to_return = "registry"
        registry.save_device_registration(node_to_be_found, registry_key_to_return)
        self.assertEqual(
                registry.lookup_registration_id_for_mds(node_to_be_found),
                registry_key_to_return)

    def tearDown(self):
        os.remove(self.file_name)

class  ValueParserTest(unittest.TestCase):
    parser = ValueParser()

    def test_that_value_is_replaced(self):
        value = ('key', 'oldvalue')
        self.assertEquals(
                'newvalue',
                self.parser.replace_value_if_key_matches(
                        value, 'key', 'newvalue')[1])

    def test_that_value_is_not_replaced_when_key_do_not_match(self):
        value = ('key', 'old')
        self.assertEqual(
                'old',
                self.parser.replace_value_if_key_matches(
                        value, 'otherkey', 'somevalue')[1])

if __name__ == '__main__':
    unittest.main()
