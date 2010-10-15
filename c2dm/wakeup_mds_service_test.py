import unittest
from mockito import mock, verify, any, when
from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase
from wakeup_mds_service import WakeupMDSApplcations
from c2dm import RegistrationRequest, C2DMServiceTemporarilyUnavailableError
from device_registry import DeviceNotRegisterdError


class WakeupMDSServiceTest(AsyncHTTPTestCase, LogTrapTestCase):
    _nodeid = 'nodeid1'
    _registrationid = 'registrationid1'
    _http_success_code = 200
    _http_not_authorised = 401
    _http_temporarly_unavaliblie_code = 503
    _successfull_new_registration = '/register_device?nodeid=' + _nodeid + '&registrationid=' + _registrationid
    _successfull_update_registration = '/update_device?nodeid=' + _nodeid + '&registrationid=' + _registrationid
    _successfull_wakeup_url = '/wakeup_mds?nodeid=' + _nodeid

    def setUp(self):
        self._registration_handler = mock()
        self._wakeup_handler = mock()
        self._wakeup_handler._tornado_facade = mock()
        AsyncHTTPTestCase.setUp(self)

    def get_app(self):
        return WakeupMDSApplcations(self._registration_handler, self._wakeup_handler)

    def test_register_new_device(self):
        self.http_client.fetch(self.get_url(self._successfull_new_registration), self.stop)
        response = self.wait()
        self.assertEqual(self._http_success_code, response.code)
        verify(self._registration_handler).handle_registration(any(RegistrationRequest))

    def test_update_registration_for_registered_device(self):
        self.http_client.fetch(self.get_url(self._successfull_update_registration), self.stop)
        response = self.wait()
        self.assertEquals(self._http_success_code, response.code)
        verify(self._registration_handler).handle_registration_id_change_for_node(any(RegistrationRequest))

    def test_wakeup_mds(self):
        self.http_client.fetch(self.get_url(self._successfull_wakeup_url), self.stop)
        response = self.wait()
        self.assertEqual(self._http_success_code, response.code)
        verify(self._wakeup_handler).wakeup_mds(self._nodeid)

    def test_wakeup_with_non_registerd_mds(self):
        when(self._wakeup_handler).wakeup_mds(self._nodeid).thenRaise(DeviceNotRegisterdError("Device not registered"))
        self.http_client.fetch(self.get_url(self._successfull_wakeup_url), self.stop)
        response = self.wait()
        self.assertEqual(self._http_not_authorised, response.code)
        verify(self._wakeup_handler).wakeup_mds(self._nodeid)

    def test_wakeup_when_c2dm_service_responds_with_500(self):
        when(self._wakeup_handler).wakeup_mds(self._nodeid).thenRaise(C2DMServiceTemporarilyUnavailableError("C2DM 500"))
        self.http_client.fetch(self.get_url(self._successfull_wakeup_url), self.stop)
        repsponse = self.wait()
        self.assertEqual(self._http_temporarly_unavaliblie_code, repsponse.code)
        

if __name__ == '__main__':
    unittest.main()

