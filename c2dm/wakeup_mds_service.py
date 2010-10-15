import tornado.web
from c2dm import RegistrationHandler, RegistrationRequest, MDSWakeupHandler, C2DMServiceTemporarilyUnavailableError
from device_registry import DeviceNotRegisterdError

class WakeupMDSApplcations(tornado.web.Application):

    def __init__(self, registration_handler = RegistrationHandler(), wakeup_handler = MDSWakeupHandler()):
        handlers = [
            (r'/register_device', RegisterNewDeviceHandler),
            (r'/update_device', UpdateDeviceRegistrationHandler),
            (r'/wakeup_mds', WakeupMDSHandler),
        ]

        tornado.web.Application.__init__(self, handlers)
        
        self.registration_handler = registration_handler
        self.wakeup_handler = wakeup_handler

class BaseHandler(tornado.web.RequestHandler):
    def get_registration_request(self):
        return RegistrationRequest(
                self.get_argument('nodeid'), self.get_argument('registrationid'))

    @property
    def registration_handler(self):
        return self.application.registration_handler

class RegisterNewDeviceHandler(BaseHandler):
        
    def get(self):
        registration_request = self.get_registration_request()
        print("Will now register device with node id: " + registration_request.node_id() +
              " and registration id: " + registration_request.registration_id())
        self.registration_handler.handle_registration(registration_request)

class UpdateDeviceRegistrationHandler(BaseHandler):

    def get(self):
        self.registration_handler.handle_registration_id_change_for_node(self.get_registration_request())

class WakeupMDSHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            self.application.wakeup_handler.wakeup_mds(self.get_argument('nodeid'))
            print('Attempt to wake device with node id: ' + self.get_argument('nodeid') + ' was successfull.')
        except DeviceNotRegisterdError:
            raise tornado.web.HTTPError(401, self.get_argument('nodeid') + ' is not a rebisterd device.')
        except C2DMServiceTemporarilyUnavailableError:
            raise tornado.web.HTTPError(503, "C2DM is temporarly unavailable.")

