#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tornado-geopy geocoding library.
# https://github.com/heynemann/tornado-geopy

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Bernardo Heynemann heynemann@gmail.com


import logging

from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.concurrent import return_future
from geopy.geocoders import GoogleV3 as GeoPyGeoCoder


class BoundingBox(object):
    def __init__(self, south_west_point, north_east_point):
        self.south_west_point = south_west_point
        self.north_east_point = north_east_point

    def to_query(self):
        return "%s,%s|%s,%s" % (
            self.south_west_point[0],
            self.south_west_point[1],
            self.north_east_point[0],
            self.north_east_point[1],
        )


class GoogleV3(GeoPyGeoCoder):
    def __init__(self, io_loop=None, *args, **kw):
        super(GoogleV3, self).__init__(*args, **kw)
        self.io_loop = io_loop or IOLoop.instance()
        self.client = AsyncHTTPClient(self.io_loop)

    def geocode_url(self, url, exactly_one=True, callback=None):
        '''Fetches the url and returns the result.'''
        logging.debug("Fetching %s..." % url)
        request = HTTPRequest(url, method="GET")

        self.client.fetch(request, callback=self.handle_geocode_url(exactly_one, callback))

    def handle_geocode_url(self, exactly_one, callback):
        def handle(http_response):
            callback(self.parse_json(http_response.body, exactly_one))
        return handle

    @return_future
    def geocode(self, string, bounds=None, region=None,
                language=None, sensor=False, exactly_one=False, callback=None):
        if isinstance(string, unicode):
            string = string.encode('utf-8')

        if bounds is not None and not isinstance(bounds, BoundingBox):
            raise ValueError("Please use tornado_geopy.geocoders.BoundingBox to specify a bounding box.")

        params = {
            'address': self.format_string % string,
            'sensor': str(sensor).lower()
        }

        if bounds:
            params['bounds'] = bounds.to_query()
        if region:
            params['region'] = region
        if language:
            params['language'] = language

        if not self.premier:
            url = self.get_url(params)
        else:
            url = self.get_signed_url(params)

        return self.geocode_url(url, exactly_one, callback=callback)
