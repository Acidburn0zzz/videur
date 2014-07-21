import os
import unittest
import time

from webtest import TestApp
from nginxtest.server import NginxServer

from support import TestMyNginx


@unittest.skipIf(True, "Needs refactoring")
class TestRateLimiting(TestMyNginx):

    def setUp(self):
        super(TestRateLimiting, self).setUp()
        self.start_server()
        # see https://github.com/openresty/lua-nginx-module/issues/379
        self.app = TestApp(self.nginx.root_url, lint=True)

    def tearDown(self):
        self.stop_server()
        super(TestRateLimiting, self).tearDown()

    def test_rate(self):
        # the 3rd call should be returning a 429
        self.app.get('/dashboard', status=200, headers={'User-Agent': 'Me'})
        self.app.get('/dashboard', status=200, headers={'User-Agent': 'Me'})
        self.app.get('/dashboard', status=404, headers={'User-Agent': 'Me'})

    def test_rate2(self):
        # the 3rd call should be returning a 200
        # because the blacklist is ttled
        self.app.get('/dashboard', status=200, headers={'User-Agent': 'Me'})
        self.app.get('/dashboard', status=200, headers={'User-Agent': 'Me'})
        time.sleep(.4)
        self.app.get('/dashboard', status=200, headers={'User-Agent': 'Me'})
