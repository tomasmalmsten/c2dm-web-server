from device_registry import DeviceRegistry
from c2dm_service_facade import C2DMServiceFacade

class RegistrationHandler:
    
    def __init__(self, device_registry = DeviceRegistry()):
        self.device_registry = device_registry

    def handle_registration(self, registration_request):
        self.device_registry.save_device_registration(
            registration_request.node_id(),
            registration_request.registration_id())

    def handle_registration_id_change_for_node(self, registration_request):
        self.device_registry.change_registration_id_for_node(
            registration_request.node_id(),
            registration_request.registration_id())

class RegistrationRequest:
        
    def __init__(self, node_id, registration_id):
        self._node_id = node_id
        self._registration_id = registration_id

    def node_id(self):
        return self._node_id

    def registration_id(self):
        return self._registration_id


class MDSWakeupHandler:

    def __init__(self, c2dm_service_facade = C2DMServiceFacade(), device_registry = DeviceRegistry()):
        self._device_registry = device_registry
        self._c2dm_service_facade = c2dm_service_facade

    def wakeup_mds(self, mds):
        registration_id = self._device_registry.lookup_registration_id_for_mds(mds)
        self._c2dm_service_facade.request_wakeup_of_mds(registration_id)
        return True

class C2DMServiceTemporarilyUnavailableError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
