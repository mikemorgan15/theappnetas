#!/usr/bin/python

import json
import sys
import os
import pandas
import logging
from theappnetas.appliance import Appliance

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(sh)

def parse_csv(csv_file):
    df = pandas.read_csv(csv_file, names=[
    	'dhcp_ip',
    	'password_old',
    	'password_new',
    	'hostname',
    	'ip_address',
    	'ip_gateway',
    	'ip_netmask',
    	'dns_servers',
    	'dns_search',
    	'ntp_servers',
    	'timezone'
    	], header=0, dtype=None)
    df = df.where((pandas.notnull(df)), None)
    q = []
    for index, row in df.iterrows():
    	dhcp_ip = row['dhcp_ip']
        password_old = row['password_old']
        password_new = row['password_new']
        hostname = row['hostname']
        ip_address = row['ip_address']
        ip_gateway = row['ip_gateway']
        ip_netmask = row['ip_netmask']
        dns_servers = row['dns_servers']
        dns_search = row['dns_search']
        ntp_servers = row['ntp_servers']
        timezone = row['timezone']
        q.append({
        	'dhcp_ip': dhcp_ip, 
        	'password_old' : password_old, 
        	'password_new': password_new, 
        	'hostname': hostname, 
        	'ip_address': ip_address, 
        	'ip_gateway': ip_gateway, 
        	'ip_netmask': ip_netmask,
        	'dns_servers': dns_servers,
        	'dns_search': dns_search,
        	'ntp_servers': ntp_servers,
        	'timezone': timezone})
    return q

def create_template_file(filename):
	f = open(filename,'w')
	f.write('dhcp_ip,password_old,password_new,hostname,ip_address,ip_gateway,ip_netmask,dns_servers,dns_search,ntp_servers,timezone')
	f.close()

def apply_config(appliance):
	result = {}
	a = Appliance(host=appliance['dhcp_ip'], username='admin', password=appliance['password_old'])
	
	if a.put_password(appliance['password_new']):
		log.info('{} - Password updated successfully'.format(appliance['hostname']))
		result['password'] = True
	else:
		log.error('{} - Password did not update'.format(appliance['hostname']))
		result['password'] = False

	a = Appliance(host=appliance['dhcp_ip'], username='admin', password=appliance['password_new'])
	
	if a.put_hostname(appliance['hostname']):
		log.info('{} - Hostname updated successfully'.format(appliance['hostname']))
		result['hostname'] = True
	else:
		log.error('{} - Hostname did not update'.format(appliance['hostname']))
		result['hostname'] = False

	if appliance['ip_address'] == 'dhcp':
		if a.post_interface(
			name='eth0',
			method='dhcp'
		):
			log.info('{} - {} updated successfully'.format(appliance['hostname'], 'eth0'))
			result['interface'] = True
		else:
			log.error('{} - {} did not update'.format(appliance['hostname'], 'eth0'))
			result['interface'] = False
	else:
		if a.post_interface(
			name='eth0', 
			method='static', 
			address=appliance['ip_address'],
			netmask=appliance['ip_netmask'],
			gateway=appliance['ip_gateway']
		):
			log.info('{} - {} updated successfully'.format(appliance['hostname'], 'eth0'))
			result['interface'] = True
		else:
			log.error('{} - {} did not update'.format(appliance['hostname'], 'eth0'))
			result['interface'] = False

	if a.post_dns_servers(
		interface='eth0', 
		servers=appliance['dns_servers']
	):
		log.info('{} - {} dns servers updated successfully'.format(appliance['hostname'], 'eth0'))
		result['dns_servers'] = True
	else:
		log.error('{} - {} dns servers did not update'.format(appliance['hostname'], 'eth0'))
		result['dns_servers'] = False

	if a.post_dns_search(
		interface='eth0',
		servers=appliance['dns_search']
	):
		log.info('{} - {} dns search domain(s) updated successfully'.format(appliance['hostname'], 'eth0'))
		result['dns_search'] = True
	else:
		log.error('{} - {} dns search domain(s) did not update'.format(appliance['hostname'], 'eth0'))
		result['dns_search'] = False

	if a.put_ntp_servers(servers=appliance['ntp_servers']):
		log.info('{} - ntp servers updated successfully'.format(appliance['hostname']))
		result['ntp_servers'] = True
	else:
		log.error('{} - ntp servers did not update'.format(appliance['hostname']))
		result['ntp_servers'] = False

	if a.put_timezone(timezone=appliance['timezone']):
		log.info('{} - timezone updated successfully'.format(appliance['hostname']))
		result['timezone'] = True
	else:
		log.error('{} - timezone did not update'.format(appliance['hostname']))
		result['timezone'] = False

	if a.put_service(service='networking', action='restart'):
		log.info('{} - networking restarted successfully'.format(appliance['hostname']))
		result['networking_restart'] = True
	else:
		log.error('{} - networking did not restart'.format(appliance['hostname']))
		result['networking_restart'] = False

	return result

if __name__ == "__main__":

	if len(sys.argv) > 1:
		if sys.argv[1] == 'template':
			if os.path.isfile('template.csv') == True:
				sys.exit('\'template.csv\' already exists. Exiting.')
			else:
				create_template_file('template.csv')
				sys.exit('\'template.csv\' created.')
		else:
			csv_file = sys.argv[1]
	else:
		print 'usage:'
		print '\'./csv_to_appliance.py appliances.csv\''
		print '\'./csv_to_appliance.py template\' - creates a blank csv template'
		sys.exit()

	appliances = parse_csv(csv_file)

	results = {}
	for appliance in appliances:
		result = apply_config(appliance)
		results[appliance['hostname']] = result

	print results
		