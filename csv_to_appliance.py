#!/usr/bin/python

''' CSV-to-Appliance configuration script for AppNeta 9.x appliances '''

''' Run './csv_to_appliance.py appliances.csv' to configure from CSV file '''
''' Run './csv_to_appliance.py template' to generate blank csv template '''

''' To use, put the current IP of the appliance in the dhcp_ip column, '''
''' and then populate the other columns with desired config settings. '''

''' Check 'csv_to_appliance_example.csv' for an example of how the .csv '''
''' file should be populated. '''

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
    	'timezone',
    	'nis_address',
    	'nis_sitekey',
    	'nis_port',
    	'nis_protocol',
    	'nis_ssl',
    	'nis_relay',
    	'nis_tunnel'
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
        nis_address = row['nis_address']
        nis_sitekey = row['nis_sitekey']
        nis_port = row['nis_port']
        nis_protocol = row['nis_protocol']
        nis_ssl = row['nis_ssl']
        nis_relay = row['nis_relay']
        nis_tunnel = row['nis_tunnel']
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
        	'timezone': timezone,
        	'nis_address': nis_address,
        	'nis_sitekey': nis_sitekey,
        	'nis_port': nis_port,
        	'nis_protocol': nis_protocol,
        	'nis_ssl': nis_ssl,
        	'nis_relay': nis_relay,
        	'nis_tunnel': nis_tunnel
        	})
    return q

def create_template_file(filename):
	f = open(filename,'w')
	f.write('dhcp_ip,password_old,password_new,hostname,ip_address,ip_gateway,ip_netmask,dns_servers,dns_search,ntp_servers,timezone,nis_address,nis_sitekey,nis_port,nis_protocol,nis_ssl,nis_relay,nis_tunnel')
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
	
	if a.post_nis(
		address=appliance['nis_address'], 
		site_key=appliance['nis_sitekey'],
		ports=str(appliance['nis_port']),
		relay_addresses=appliance['nis_relay'],
		ssl=str(appliance['nis_ssl']),
		protocol=appliance['nis_protocol'],
		tunnel_url=appliance['nis_tunnel']):
		log.info('{} - nis config applied successfully'.format(appliance['hostname']))
		result['nis_config'] = True
	else:
		log.error('{} - nis config was not applied'.format(appliance['hostname']))
		result['nis_config'] = False
	
	if a.put_appliance(action='reboot'):
		log.info('{} - appliance rebooted successfully'.format(appliance['hostname']))
		result['appliance_reboot'] = True
	else:
		log.error('{} - appliance did not reboot'.format(appliance['hostname']))
		result['appliance_reboot'] = False
	
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
		