#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tornado-geopy geocoding library.
# https://github.com/heynemann/tornado-geopy

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Bernardo Heynemann heynemann@gmail.com

from tornado.testing import AsyncTestCase, gen_test
from preggy import expect

from tornado_geopy.geocoders import GoogleV3, BoundingBox


class GoogleV3GeoCoderTestCase(AsyncTestCase):

    def test_can_geocode_address(self):
        g = GoogleV3(io_loop=self.io_loop)
        g.geocode(u"10900 Euclid Ave in Cleveland", callback=self.stop)
        results = self.wait()
        expect(results).to_length(1)
        place, (lat, lng) = results[0]
        expect(place).to_equal(u"10900 Euclid Avenue, Cleveland, OH 44106, USA")
        expect(lat).to_equal(41.5072596)
        expect(lng).to_equal(-81.6070113)


class GoogleV3GeoCoderTestCaseUsingGenTest(AsyncTestCase):

    @gen_test
    def test_can_geocode_address(self):
        g = GoogleV3(io_loop=self.io_loop)
        results = yield g.geocode(u"10900 Euclid Ave in Cleveland")
        expect(results).to_length(1)
        place, (lat, lng) = results[0]
        expect(place).to_equal(u"10900 Euclid Avenue, Cleveland, OH 44106, USA")
        expect(lat).to_equal(41.5072596)
        expect(lng).to_equal(-81.6070113)

    @gen_test
    def test_can_geocode_address_with_region(self):
        g = GoogleV3(io_loop=self.io_loop)
        results = yield g.geocode(u"Toledo", region="ES")
        expect(results).to_length(1)

        place, (lat, lng) = results[0]
        expect(place).to_equal(u"Toledo, Spain")
        expect(lat).to_equal(39.8628316)
        expect(lng).to_equal(-4.027323099999999)

    @gen_test
    def test_can_geocode_address_with_bounds(self):
        g = GoogleV3(io_loop=self.io_loop)
        west = -22.917274
        south = -43.186623
        east = -22.906078
        north = -43.162494
        box = BoundingBox((west, south), (east, north))
        results = yield g.geocode(u"Avenida Rio Branco", bounds=box)
        expect(results).to_length(1)

        place, (lat, lng) = results[0]
        expect(place).to_equal(u"Avenida Rio Branco, Rio de Janeiro, Brazil")
        expect(lat).to_equal(-22.9049854)
        expect(lng).to_equal(-43.1777056)

    @gen_test
    def test_can_geocode_address_in_portuguese(self):
        g = GoogleV3(io_loop=self.io_loop)
        west = -22.917274
        south = -43.186623
        east = -22.906078
        north = -43.162494
        box = BoundingBox((west, south), (east, north))
        results = yield g.geocode(u"Avenida Rio Branco", bounds=box, language="pt-BR")
        expect(results).to_length(1)

        place, (lat, lng) = results[0]
        expect(place).to_equal(u"Avenida Rio Branco, Rio de Janeiro, República Federativa do Brasil")
        expect(lat).to_equal(-22.9049854)
        expect(lng).to_equal(-43.1777056)
