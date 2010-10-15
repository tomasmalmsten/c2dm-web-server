import unittest
from mockito import mock, when, verify
from c2dm import *

from device_registry import DeviceNotRegisterdError

class  RegistrationHandlerTestCase(unittest.TestCase):

    node_id = "fcc1bf7e0ff1b0dd"
    registration_id = "mock_registration_id"
    device_registry = mock()
    registration_request = RegistrationRequest(node_id, registration_id)
    
    def test_handle_registration(self):
        handler = RegistrationHandler(self.device_registry)
        handler.handle_registration(self.registration_request)
        verify(self.device_registry).save_device_registration(
                self.node_id, self.registration_id)

    def test_handle_registration_id_change(self):
        handler = RegistrationHandler(self.device_registry)
        handler.handle_registration_id_change_for_node(self.registration_request)
        verify(self.device_registry).change_registration_id_for_node(
                self.node_id, self.registration_id)

class MDSWakeupHandlerTestCase(unittest.TestCase):

    device_registry = mock()
    c2dm_service_facade = mock()
    wakeup_handler = MDSWakeupHandler(c2dm_service_facade, device_registry)
    _mds = 'node_id'
    _registration_id = 'registration_id'

    def test_wakeup_for_registerd_mds(self):
        when(self.device_registry).lookup_registration_id_for_mds(self._mds).thenReturn(self._registration_id)
        self.assertTrue(self.wakeup_handler.wakeup_mds(self._mds))

    def test_wakeup_for_unregisterd_mds(self):
        when(self.device_registry).lookup_registration_id_for_mds(self._mds).thenRaise(DeviceNotRegisterdError('Device not found'))
        try:
            self.wakeup_handler.wakeup_mds(self._mds)
            self.fail('Expected DeviceNotRegisterdError')
        except DeviceNotRegisterdError:
            None

    def test_wakeup_when_c2dm_service_is_down(self):
        when(self.device_registry).lookup_registration_id_for_mds(self._mds).thenReturn(self._registration_id)
        when(self.c2dm_service_facade).request_wakeup_of_mds(self._registration_id).thenRaise(C2DMServiceTemporarilyUnavailableError("C2DM Returned a 503"))
        try:
            self.wakeup_handler.wakeup_mds(self._mds)
            self.fail('Expceted C2DMServiceTemporarilyUnavailableError')
        except C2DMServiceTemporarilyUnavailableError:
            None

if __name__ == '__main__':
    unittest.main()

