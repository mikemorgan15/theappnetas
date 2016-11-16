#!/usr/bin/python

# Appliance backup script

import json
from theappnetas.appliance import Appliance

app = Appliance(host='host', username='admin', password='password')
config = {}

nis_config = app.get_nis()
config['nis'] = nis_config['nis_config']

hostname = app.get_hostname()
config['hostname'] = hostname['hostname']

timezone = app.get_timezone()
config['timezone'] = timezone['timezone']

ntp_servers = app.get_ntp_servers()
config['ntp_servers'] = ntp_servers['servers']

interface_default = app.get_interface_default()
config['default_interface'] = interface_default['default_interface']

config['interfaces'] = {}
config['dns_servers'] = {}
config['dns_search'] = {}
config['static_routes'] = {}

interfaces = app.get_interfaces()
for iface in interfaces['interfaces']:
	if not iface == 'bridge0':
		interface = {}
		interfaceconfig = app.get_interface(interface=iface)
		for conf in interfaceconfig['interface']['families']:
			for key in conf:
				if not conf[key] == None and conf[key]:
					interface[key] = conf[key]
		config['interfaces'][iface] = interface

		dns_servers = app.get_dns_servers(interface=iface)
		if dns_servers['dns_nameservers']:
			config['dns_servers'][iface] = dns_servers['dns_nameservers']

		dns_search = app.get_dns_search(interface=iface)
		if dns_search['dns_search']:
			config['dns_search'][iface] = dns_search
	
		static_route = app.get_static_route(interface=iface)
		if static_route['result_data']['static_routes']:
			config['static_routes'][iface] = static_route['result_data']['static_routes']

print json.dumps(config)