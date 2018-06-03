'''
Created on April 05, 2013

@author: AxelVoitier
@license: GNU LGPL v3

Python module to access Avahi through DBus.
'''

import os
import time
import warnings

try:
    import dbus
    import gobject
    from dbus.mainloop.glib import DBusGMainLoop
except ImportError:
    warnings.warn('DBus/Avahi is unavailable (Windows?).', RuntimeWarning) 

# Use the following sources:
# http://avahi.org/wiki/PythonBrowseExample
# http://avahi.org/download/doxygen/index.html
# http://avahi.org/download/ServiceResolver.introspect.xml
# http://avahi.org/wiki/ProgrammingDocs
#
# http://www.freedesktop.org/wiki/IntroductionToDBus
# http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html
# http://cgit.freedesktop.org/dbus/dbus-python/tree/examples
# http://www.no-ack.org/2010/07/writing-simple-dbus-client-in-python.html

def find_all_naos(ip_v6=False):
    '''
    Returns IP, port and other information about NaoQis (real robot or NaoQi
    running on a desktop computer) available on the local network in a list.
    
    Each entry of the list is a dictionary with the following keys:
    - 'robot_name': The name of the robot (string).
    - 'host_name': The hostname of the robot (string).
    - 'ip_address': The IP address corresponding to the hostname (string).
    - 'naoqi_port': The port used by NaoQi (int).
    - 'local': If NaoQi run on the same machine that us or not (boolean).
    - 'favorite': If the environment variable FAVORITE_NAO correspond to this
    robot (boolean)
    
    The ip_v6 argument is for the future.
    '''
    try:
        nao_finder = _AvahiNAOFinder(ip_v6)
        nao_finder.run()
        return nao_finder.services_found
    except NameError:
        # On Windows, return a very default nao.local.
        entry = {
            'robot_name': 'nao',
            'host_name': 'nao.local',
            'ip_address': 'nao.local',
            'naoqi_port': 9559,
            'local': False
        }
        entry['favorite'] = os.environ.get('FAVORITE_NAO') in entry.values()
        return [entry]
    
class _AvahiNAOFinder(object):
    '''
    Class used to query Avahi about NAO on the network.
    '''
    
    # Constant definitions coming from the python-avahi module.
    # The python-avahi module is not installed by default on Nao or usual OSs.
    # But it is mainly made of constant definitions.
    # So I replicate here the important ones.
    AVAHI_DBUS_NAME = 'org.freedesktop.Avahi'
    AVAHI_DBUS_INTERFACE_SERVER = AVAHI_DBUS_NAME + '.Server'
    AVAHI_DBUS_INTERFACE_SERVICE_BROWSER = AVAHI_DBUS_NAME + '.ServiceBrowser'
    AVAHI_IF_UNSPEC = -1
    AVAHI_PROTO_UNSPEC, AVAHI_PROTO_INET, AVAHI_PROTO_INET6  = -1, 0, 1
    AVAHI_LOOKUP_RESULT_LOCAL = 8
    
    TIMEOUT = 30

    def __init__(self, ip_v6=False):
        self.nb_services_found = 0
        self.services_found = []
    
        bus = dbus.SystemBus(mainloop=DBusGMainLoop())

        self.server = dbus.Interface(bus.get_object(self.AVAHI_DBUS_NAME, '/'),
                                     self.AVAHI_DBUS_INTERFACE_SERVER)
                
        proto_inet = self.AVAHI_PROTO_INET6 if ip_v6 else self.AVAHI_PROTO_INET

        sbrowser = dbus.Interface(
                       bus.get_object(
                           self.AVAHI_DBUS_NAME,
                           self.server.ServiceBrowserNew(
                               self.AVAHI_IF_UNSPEC, proto_inet,
                               '_naoqi._tcp', 'local', dbus.UInt32(0)
                            )
                        ), self.AVAHI_DBUS_INTERFACE_SERVICE_BROWSER
                    )
                    
        def item_new_cb_wrapper(interface, protocol, name,
                                stype, domain, flags):
            '''Callback called by Avahi. Wrapping around our object method.'''
            self.item_new_cb(interface, protocol, name, stype, domain, flags)

        sbrowser.connect_to_signal("ItemNew", item_new_cb_wrapper)
        
        self.gloop = gobject.MainLoop()
        
        self.timeout_time = time.time() + self.TIMEOUT
        def timeout(*args):
            '''Callback called by Avahi every second. Quit when timeout.'''
            if time.time() >= self.timeout_time:
                self.quit()
                return False
            return True
            
        gobject.timeout_add(1000, timeout)
        
    def run(self):
        '''
        Start the main loop.
        '''
        self.timeout_time = time.time() + self.TIMEOUT
        self.gloop.run()
        
    def quit(self):
        '''
        Quit the main loop.
        '''
        self.gloop.quit()
    
    def item_new_cb(self, interface, protocol, name, stype, domain, flags):
        '''
        Callback indirectly called by Avahi for every new item corresponding
        to our query for _naoqi._tcp.
        '''
        self.timeout_time = time.time() + self.TIMEOUT
        self.nb_services_found += 1
        
        def service_resolved_cb_wrapper(*args):
            '''Callback called by Avahi. Wrapping around our object method.'''
            self.service_resolved_cb(*args)
            
        def do_nothing_error_cb_wrapper(*args):
            '''Callback called by Avahi. Wrapping around our object method.'''
            self.do_nothing_error_cb(*args)
            
        self.server.ResolveService(
            interface, protocol, name, stype, 
            domain, self.AVAHI_PROTO_UNSPEC, dbus.UInt32(0), 
            reply_handler=service_resolved_cb_wrapper,
            error_handler=do_nothing_error_cb_wrapper)

    def service_resolved_cb(self, *args):
        '''
        Callback indirectly called by Avahi when resolving a service
        we found in item_new_cb.
        '''
        self.timeout_time = time.time() + self.TIMEOUT
        #print 'service resolved', args[5]
        labels = ['interface', 'protocol', 'name', 'type', 'domain', 'host',
                  'aprotocol', 'address', 'port', 'txt', 'flags']
        entry = {
            'robot_name': str(args[labels.index('name')]),
            'host_name': str(args[labels.index('host')]),
            'ip_address': str(args[labels.index('address')]),
            'naoqi_port': int(args[labels.index('port')]),
            'local': bool(args[labels.index('flags')] &
                          self.AVAHI_LOOKUP_RESULT_LOCAL)
        }
        entry['favorite'] = os.environ.get('FAVORITE_NAO') in entry.values()
        self.services_found.append(entry)
        self.nb_services_found -= 1
        if self.nb_services_found == 0:
            self.quit()

    def do_nothing_error_cb(self, *args):
        '''
        Callback indirectly called by Avahi when an error occurs during
        the resolution of a service in item_new_cb.
        '''
        # print args
        self.nb_services_found -= 1
        if self.nb_services_found == 0:
            self.quit()

