import tornado.httpserver
import tornado.ioloop
import tornado.options as options
from c2dm.wakeup_mds_service import WakeupMDSApplcations
from c2dm.c2dm import RegistrationHandler, MDSWakeupHandler
from c2dm.device_registry import DeviceRegistry
from c2dm.c2dm_service_facade import C2DMServiceFacade

def main():
    device_registry = DeviceRegistry("registry.csv")
    registrion_handler = RegistrationHandler(device_registry)
    c2dm_facade = C2DMServiceFacade()
    wekup_handler = MDSWakeupHandler(c2dm_facade, device_registry)
    print("Will now start the c2dm application server")

    map(lambda x: options.define(*x), [
        ("interface", "", str, "interface to listen on"),
        ("port", 8888, int, "port to listen on"),
        ("debug", False, bool, "run in debug mode"),])
    options.parse_command_line()

    o = options.options
    application = WakeupMDSApplcations(registrion_handler, wekup_handler)
    httpserver = tornado.httpserver.HTTPServer(application)
    httpserver.listen(o.port, o.interface)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
    

if __name__ == "__main__":
    main()


