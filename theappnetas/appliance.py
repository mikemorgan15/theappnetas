import requests 
import urlparse
import urllib

class Appliance(object):
    APIPATH = '/api/v1'
    PORT = 5443

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def verify(self, response):
       if response.ok:
            return True
        else:
            raise requests.exceptions.HTTPError 

    def hostname(self):
        response = self._get(url=self._url(path='hostname'))
        if self.verify(response):
            return response.get('result_data').get('hostname')

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

    def _get(self, url=None):
        return requests.get(url, verify=False, auth=self._auth())
