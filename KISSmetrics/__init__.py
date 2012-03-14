'''
Example usage:

km = KM('my-api-key')
km.identify('simon')
km.record('an event', {'attr': '1'})
'''

import urllib
from twisted.web.client import getPage
from datetime import datetime

KM_BASE_URL = 'https://trk.kissmetrics.com'
KM_LOG_FILE = '/tmp/kissmetrics_error.log'

class KMError(Exception):
    pass

class KM(object):
    def __init__(self, key, host=KM_BASE_URL, http_timeout=2, logging=False, log_file=KM_LOG_FILE):
        '''km = KM('my-api-key')'''
        self._id = None
        self._key = key
        self._host = host
        self._timeout = http_timeout
        self._logging = logging
        self._log_file = log_file

    def identify(self, id):
        '''km.identify('pelle')'''
        self._id = id

    def record(self, action, props={}):
        '''km.record('Pelle\'s test event', { 'attr' : 'shark' })'''
        self._check_identify()
        if isinstance(action, dict):
            self.set(action)

        props.update({'_n': action})
        return self._request('e', props)

    def set(self, data):
        '''km.set({ 'gender' : 'male' })'''
        self._check_identify()
        return self._request('s', data)

    def alias(self, name, alias_to):
        '''km.alias('pelle', 'pelle@wrapp.com')'''
        return self._request('a', {'_n': alias_to, '_p': name}, False)

    def _check_identify(self):
        if not self._id:
            raise KMError('Need to identify first (KM.identify <user>)')

    def _now(self):
        return datetime.utcnow()

    def _logm(self, msg):
        if not self._logging:
            return
        msg = self._now().strftime('<%c> ') + msg
        try:
            fh = open(self._log_file, 'a')
            fh.write(msg)
            fh.close()
        except IOError:
            raise #just re-reaise at this point

    def _create_url(self, type, data_dict):
        return self._host + '/%s?%s' % (type, urllib.urlencode(data_dict))

    def _request(self, type, data, update=True):
        def errback(e):
            raise KMError(e.message)

        # if user has defined their own _t, then include necessary _d
        if '_t' in data:
            data['_d'] = 1
        else:
            data['_t'] = self._now().strftime('%s')

        # add customer key to data sent
        data['_k'] = self._key

        if update:
            data['_p'] = self._id

        url = self._create_url(type, data)
        return getPage(url, timeout=self._timeout).addErrback(errback)

