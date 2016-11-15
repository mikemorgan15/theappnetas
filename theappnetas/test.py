from appliance import Appliance
app = Appliance('appliance_hostname','admin','password')

''' Gets sequencer info '''
get_sequencer = app.get_sequencer()
print 'Sequencer info - {}'.format(get_sequencer)

'''Tests connectivity to a host. Parameters - 'server', 'port' (optional), and 'check_type' (TCP or Ping)'''
post_connectivity = app.post_connectivity(server='google.com', port='80', check_type='TCP')
print 'Connectivity check - {}'.format(post_connectivity)

''' Change appliance password.  Parameter - 'password'.  Returns 'True' on success. '''
put_password = app.put_password(password='password')
print 'Password changed - {}'.format(put_password)

''' Get appliance hostname '''
get_hostname = app.get_hostname()
print 'Appliance hostname = {}'.format(get_hostname)

''' Update appliance hostname.  Parameter - 'hostname'.  Returns 'True' on success. '''
put_hostname = app.put_hostname(hostname='mikedeskm25')
print 'Change hostname - {}'.format(put_hostname)

''' Get NTP servers '''
get_ntp_servers = app.get_ntp_servers()
print 'NTP server list - {}'.format(get_ntp_servers)

''' Update NTP servers.  Parameter - 'servers' (list).  Returns 'True' on success. '''
put_ntp_servers = app.put_ntp_servers(servers=['1.2.3.4', '5.6.7.8'])
print 'Change NTP servers - {}'.format(put_ntp_servers)

''' Get DNS servers for a specific interface.  Parameter - 'interface' '''
get_dns_servers = app.get_dns_servers(interface='eth0')
print 'DNS server list - {}'.format(get_dns_servers)

''' Update DNS servers for a specific interface.  Parameters - 'interface', 'servers' (list) '''
post_dns_servers = app.post_dns_servers(interface='eth0', servers=['8.8.8.8','8.8.4.4'])
print 'Change DNS servers - {}'.format(post_dns_servers)

''' Delete DNS servers for a specific interface.  Parameters - 'interface'.  Returns 'True' on success, 'False' if no servers deleted. '''
delete_dns_servers = app.delete_dns_servers(interface='eth1')
print 'Delete DNS servers - {}'.format(delete_dns_servers)

''' Get DNS search domains for a specific interface.  Parameter - 'interface' '''
get_dns_search = app.get_dns_search(interface='eth0')
print 'DNS search domain list - {}'.format(get_dns_search)

''' Update DNS search domains for a specific interface.  Parameters - 'interface', servers (list).  Returns 'True' on success. '''
post_dns_search = app.post_dns_search(interface='eth0', servers=['jaalam.net', 'appneta.com'])
print 'Update DNS search domains - {}'.format(post_dns_search)

''' Delete DNS search domains for a specific interface.  Parameter - 'interface'.  Returns 'True' on success, 'False' if no servers deleted. '''
delete_dns_search = app.delete_dns_search(interface='eth1')
print 'Delete DNS search domains - {}'.format(delete_dns_search)

''' Get appliance timezone '''
get_timezone = app.get_timezone()
print 'Appliance timezone - {}'.format(get_timezone)

''' Get list of valid timezones from appliance '''
get_timezone_capability = app.get_timezone_capability()
print 'Available timezones - {}'.format(get_timezone_capability)

''' Update appliance timezone.  Parameter - 'timezone'.  Returns 'True' on success. '''
put_timezone = app.put_timezone(timezone='America/Vancouver')
print 'Update timezone - {}'.format(put_timezone)

''' Get list of interfaces '''
get_interfaces = app.get_interfaces()
print 'List interfaces - {}'.format(get_interfaces)

''' Get default interface '''
get_interface_default = app.get_interface_default()
print 'Default interface - {}'.format(get_interface_default)

''' Discard pending interface changes.  Returns 'True' on success. '''
put_interface_discard_changes = app.put_interface_discard_changes()
print 'Discard uncommitted interface changes - {}'.format(put_interface_discard_changes)

''' Update interface settings.  Accepts any/all interface creation parameters.  Returns 'True' on success. '''
post_interface = app.post_interface(name='eth1', method='static', address='10.0.0.2', netmask='255.255.255.0', gateway='10.0.0.1')
print 'Update interface - {}'.format(post_interface)

''' Delete an interface.  Parameter - 'interface'.  Returns 'True' on success, 'False' if no servers deleted. '''
delete_interface = app.delete_interface(interface='eth1')
print 'Delete interface - {}'.format(delete_interface)

''' Get list of services '''
get_services = app.get_services()
print 'List services - {}'.format(get_services)

''' Get info on a specific service. Parameter - 'service' '''
get_service = app.get_service(service='networking')
print 'Info on a specific service - {}'.format(get_service)

''' Perform an action on a service (start, restart, stop).  Parameters - 'service', 'action'.  Returns 'True' on success. '''
put_service = app.put_service(service='pathview-sequencer', action='restart')
print 'Perform an action on a service - {}'.format(put_service)

''' Get appliance routing table '''
get_route = app.get_route()
print 'Routing table - {}'.format(get_route)

''' Get static routes for an interface.  Parameter - 'interface' '''
get_static_route = app.get_static_route(interface='eth0')
print 'Static routes from an interface - {}'.format(get_static_route)

''' Delete static routes for an interface.  Parameter - 'interface'.  Returns 'True' on success. '''
delete_static_route = app.delete_static_route(interface='eth0')
print 'Delete static route - {}'.format(delete_static_route)

''' Get a list of in-range wifi networks '''
get_wireless_networks = app.get_wireless_networks()
print 'Wireless networks in range - {}'.format(get_wireless_networks)