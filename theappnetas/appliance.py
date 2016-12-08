import requests 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urlparse
import urllib
import json
import logging

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(sh)

class Appliance(object):
    APIPATH = '/api/v1'
    PORT = 443
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def verify(self, response):
        if response is not None:
            if response.ok:
                return True
        else:
            return False

    def test_connectivity(self):
        try:
            response = self._get(url=self._url(path='hostname'))
        except requests.exceptions.ConnectionError:
            return False
        else:
            return True


    ''' === Appliance  === '''

    ''' POST appliance connectivity check '''
    def post_connectivity(self, **kwargs):
        params = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                params[key] = value
        response = self._post(
            url=self._url(path='appliance/connection'),
            data=self._data(parameter='connections', value=[params]))
        if self.verify(response):
            return {'result_data': response.json().get('result_data')}

    ''' PUT appliance password '''
    def put_password(self, password):
        response = self._put(
            url=self._url(path='appliance/password'), 
            data=self._data(parameter='password', value=password))
        if self.verify(response):
            return response.ok

    ''' GET sequencer info '''
    def get_sequencer(self):
        response = self._get(url=self._url(path='sequencer'))
        if self.verify(response):
            return {'result_data': response.json().get('result_data')}

    ''' PUT appliance action (reboot) '''
    def put_appliance(self, action):
        response = self._put(
            url=self._url(path='appliance',query={'action': action}),
            data=self._data(parameter=True, value=True))
        if self.verify(response):
            return response.ok


    ''' === DNS servers === '''

    ''' GET appliance DNS servers '''
    def get_dns_servers(self, interface):
        response = self._get(url=self._url(path='interface/{}/dns_nameserver'.format(interface)))
        if self.verify(response):
            dhcp = response.json().get('result_data').get('dhcp_dns_nameservers')
            static = response.json().get('result_data').get('dns_nameservers')
            return {'dhcp_dns_nameservers': dhcp, 'dns_nameservers': static}

    ''' POST appliance DNS servers '''
    def post_dns_servers(self, interface, servers):
        response = self._post(
            url=self._url(path='interface/{}/dns_nameserver'.format(interface)), 
            data='{"dns_nameservers": %s}' % servers)
        if self.verify(response):
            return response.ok

    ''' DELETE DNS servers from an interface '''
    def delete_dns_servers(self, interface, family='inet'):
        response = self._delete(
            url=self._url(path='interface/{}/dns_nameserver'.format(interface), query={'family': family}))
        if response.json().get('status') == 404:
            return False
        if self.verify(response):
            return response.ok


    ''' === DNS search domains === '''

    ''' GET appliance DNS search domains '''
    def get_dns_search(self, interface):
        response = self._get(url=self._url(path='interface/{}/dns_search'.format(interface)))
        if self.verify(response):
            dhcp = response.json().get('result_data').get('dhcp_dns_search')
            static = response.json().get('result_data').get('dns_search')
            return {'dhcp_dns_search': dhcp, 'dns_search': static}

    ''' POST appliance DNS search domains '''
    def post_dns_search(self, interface, servers):
        response = self._post(
            url=self._url(path='interface/{}/dns_search'.format(interface)), 
            data=self._data(parameter='dns_search', value=[servers]))
        if self.verify(response):
            return response.ok

    ''' DELETE DNS search domains from an interface '''
    def delete_dns_search(self, interface, family='inet'):
        response = self._delete(
            url=self._url(path='interface/{}/dns_search'.format(interface), query={'family': family}))
        if response.json().get('status') == 404:
            return False
        if self.verify(response):
            return response.ok


    ''' === Appliance hostname === '''

    ''' GET appliance hostname '''
    def get_hostname(self):
        response = self._get(url=self._url(path='hostname'))
        if self.verify(response):
            return {'hostname': response.json().get('result_data').get('hostname')}

    ''' PUT appliance hostname '''
    def put_hostname(self, hostname=None):
        response = self._put(
            url=self._url(path='hostname'), 
            data=self._data(parameter='hostname', value=hostname))
        if self.verify(response):
            return response.ok


    ''' === NTP servers === '''

    ''' GET appliance NTP servers '''
    def get_ntp_servers(self):
        response = self._get(url=self._url(path='ntp'))
        if self.verify(response):
            return {'servers': response.json().get('result_data').get('servers')}

    ''' PUT appliance NTP servers '''
    def put_ntp_servers(self, servers):
        response = self._put(
            url=self._url(path='ntp'), 
            data='{"servers": %s}' % servers)
        if self.verify(response):
            return response.ok

    ''' DELETE NTP servers from an interface '''
    def delete_ntp_servers(self, servers):
        response = self._delete(
            url=self._url(path='ntp'),
            data=self._data(parameter='servers', value=servers))
        if self.verify(response):
            return response.ok


    ''' === Appliance timezone === '''

    ''' GET appliance timezone '''
    def get_timezone(self):
        response = self._get(url=self._url(path='timezone'))
        if self.verify(response):
            return {'timezone': response.json().get('result_data').get('timezone')}

    ''' GET list of possible timezones '''
    def get_timezone_capability(self):
        response = self._get(url=self._url(path='timezone/capability'))
        if self.verify(response):
            return {'valid_timezones': response.json().get('result_data').get('valid_timezones')}

    ''' PUT timezone '''
    def put_timezone(self, timezone):
        response = self._put(
            url=self._url(path='timezone'),
            data=self._data(parameter='timezone', value=timezone))
        if self.verify(response):
            return response.ok


    ''' === Network interfaces === '''

    ''' GET list of active interfaces '''
    def get_interfaces(self, config_state='active'):
        response = self._get(url=self._url(
            path='interface', 
            query={'config_state': config_state}))
        if response.json().get('status') == 404:
            return False
        if self.verify(response):
            return {'interfaces': response.json().get('result_data').get('names')}

    ''' GET info config of a specific interface '''
    def get_interface(self, interface, config_state='active'):
        response = self._get(url=self._url(
            path='interface/{}'.format(interface), 
            query={'config_state': config_state}))
        if self.verify(response):
            return {'interface': response.json().get('result_data')}

    ''' GET default interface '''
    def get_interface_default(self):
        response = self._get(url=self._url(path='interface/default'))
        if self.verify(response):
            return {'default_interface': response.json().get('result_data').get('name')}

    ''' PUT discard pending interface changes '''
    def put_interface_discard_changes(self):
        response = self._put(
            url=self._url(path='interface', query={'action': 'discard'}),
            data=self._data(parameter=True, value=True))
        if self.verify(response):
            return response.ok

    ''' POST create new interface '''
    def post_interface(self, **kwargs):
        interface = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                interface[key] = value
        response = self._post(
            url=self._url(
                path='interface'),
                data=json.dumps(interface)
            )
        if self.verify(response):
            return response.ok

    ''' DELETE interface '''
    def delete_interface(self, interface):
        response = self._delete(
            url=self._url(
                path='interface/{}'.format(interface)
                )
            )
        if self.verify(response):
            return response.ok


    ''' === NIS Config === '''

    ''' GET NIS config '''
    def get_nis(self):
        response = self._get(url=self._url(path='nis'))
        if self.verify(response):
            return {'nis_config': response.json().get('result_data')}

    def post_nis(self, **kwargs):
        nis_config = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                nis_config[key] = value
        response = self._post(
            url=self._url(
                path='nis',
                query={'restart_services': 'true'}),
            data=json.dumps(nis_config)            
            )
        print json.dumps(nis_config) 
        print response.json
        if self.verify(response):
            return response.ok

    def delete_nis(self):
        response = self._delete(
            url=self._url(
                path='nis',
                query={'restart_services': 'true'}
                )
            )
        if self.verify(response):
            return response.ok


    ''' === Services === '''

    ''' GET service list '''
    def get_services(self, get_detailed_info='false'):
        response = self._get(
            url=self._url(
                path='service', 
                query={'get_detailed_info': get_detailed_info}
                )
            )
        if self.verify(response):
            return {'services': response.json().get('result_data').get('services')}

    ''' GET service status '''
    def get_service(self, service):
        response = self._get(url=self._url(path='service/{}'.format(service)))
        if self.verify(response):
            return {'result_data': response.json().get('result_data')}

    ''' PUT perform action on service '''
    def put_service(self, service, action):
        response = self._put(
            url=self._url(path='service/{}'.format(service), query={'action': action}),
            data=self._data(parameter=True, value=True))
        if self.verify(response):
            return response.ok


    ''' === Routes === '''

    ''' GET routing table '''
    def get_route(self, family='inet'):
        response = self._get(url=self._url(path='route', query={'family': family}))
        if self.verify(response):
            return {'result_data': response.json().get('result_data')}

    ''' GET static routes by interface '''
    def get_static_route(self, interface, config_state='active', family='inet'):
        response = self._get(
            url=self._url(path='interface/{}/static_route'.format(interface), 
                query={'config_state': config_state, 'family': family}))
        if self.verify(response):
            return {'result_data': response.json().get('result_data')}

    ''' POST static route to interface '''
    def post_static_route(self, interface, **kwargs):
        params = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                params[key] = value
        response = self._post(
            url=self._url(path='interface/{}/static_route'.format(interface)),
            data=self._data(parameter='static_routes', value=[params]))
        if self.verify(response):
            return {'result_data': response.json().get('result_data')}

    ''' DELETE static routes from an interface '''
    def delete_static_route(self, interface, family='inet'):
        response = self._delete(
            url=self._url(path='interface/{}/static_route'.format(interface),
                query={'family': family}))
        if self.verify(response):
            return response.ok


    ''' === Wireless === '''

    ''' GET wireless networks '''
    def get_wireless_networks(self):
        response = self._get(url=self._url(path='wireless_network'))
        if self.verify(response):
            return {'result_data': response.json().get('result_data')}


    def _auth(self):
        return (self.username, self.password)

    def _url(self, path, query=None):
        if query is None:
            query = {}
        query_string = urllib.urlencode(query)
        url = urlparse.ParseResult(
        	scheme = 'https',
        	netloc = '{}:{}'.format(self.host, self.PORT),
        	path = '{}/{}/'.format(self.APIPATH, path),
        	params = None,
        	query = urllib.urlencode(query),
        	fragment = None)
        return url.geturl()

    def _data(self, parameter, value):
        return json.dumps({parameter: value})

    def _get(self, url=None):
        try:
            result = requests.get(url, verify=False, auth=self._auth())
        except Exception as e:
            log.error('(GET) Connection failed to {} - {}'.format(url, e))
            return None
        return result

    def _post(self, url=None, data=None):
        try:
            result = requests.post(url, headers=self.HEADERS, verify=False, auth=self._auth(), data=data)
        except Exception as e:
            log.error('(POST) Connection failed to {} - {}'.format(url, e))
            return None
        return result

    def _put(self, url=None, data=None):
        try:
            result = requests.put(url, headers=self.HEADERS, verify=False, auth=self._auth(), data=data)
        except Exception as e:
            log.error('(PUT) Connection failed to {} - {}'.format(url, e))
            return None
        return result

    def _delete(self, url=None):
        try:
            result = requests.delete(url, verify=False, auth=self._auth())
        except Exception as e:
            log.error('(DELETE) Connection failed to {} - {}'.format(url, e))
            return None
        return result
