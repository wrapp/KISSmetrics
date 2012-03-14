from nose.twistedtools import deferred
from KISSmetrics import KM

KM_DEVELOPMENT_KEY = '2e75c2009a174100316219926aaaee8a8901a680'

class TestAlias(object):

    def setup(self):
        self.km = KM(KM_DEVELOPMENT_KEY)
        self.km.identify('pelle')

    @deferred()
    def test_alias(self):
        return self.km.alias('pelle', 'pelle@wrapp.com')

    @deferred()
    def test_set(self):
        return self.km.set({ 'gender' : 'male' })

    @deferred()
    def test_record(self):
        return self.km.record('Pelle\'s test event', { 'attr' : 'shark' })
