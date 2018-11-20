#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2002-2018 "Neo4j,"
# Neo4j Sweden AB [http://neo4j.com]
#
# This file is part of Neo4j.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import division

from datetime import time
from unittest import TestCase

from pytz import timezone

from neotime import Time
from neotime.arithmetic import nano_add, nano_div


eastern = timezone("US/Eastern")


class TimeTestCase(TestCase):

    def test_bad_attribute(self):
        t = Time(12, 34, 56.789)
        with self.assertRaises(AttributeError):
            _ = t.x

    def test_simple_time(self):
        t = Time(12, 34, 56.789)
        self.assertEqual(t.hour_minute_second, (12, 34, 56.789))
        self.assertEqual(t.ticks, 45296.789)
        self.assertEqual(t.hour, 12)
        self.assertEqual(t.minute, 34)
        self.assertEqual(t.second, 56.789)

    def test_midnight(self):
        t = Time(0, 0, 0)
        self.assertEqual(t.hour_minute_second, (0, 0, 0))
        self.assertEqual(t.ticks, 0)
        self.assertEqual(t.hour, 0)
        self.assertEqual(t.minute, 0)
        self.assertEqual(t.second, 0)

    def test_nanosecond_precision(self):
        t = Time(12, 34, 56.789123456)
        self.assertEqual(t.hour_minute_second, (12, 34, 56.789123456))
        self.assertEqual(t.ticks, 45296.789123456)
        self.assertEqual(t.hour, 12)
        self.assertEqual(t.minute, 34)
        self.assertEqual(t.second, 56.789123456)

    def test_str(self):
        t = Time(12, 34, 56.789123456)
        self.assertEqual(str(t), "12:34:56.789123456")

    def test_now_without_tz(self):
        t = Time.now()
        self.assertIsInstance(t, Time)

    def test_now_with_tz(self):
        t = Time.now(tz=eastern)
        self.assertIsInstance(t, Time)
        self.assertEqual(t.tzinfo, eastern)

    def test_utc_now(self):
        t = Time.utc_now()
        self.assertIsInstance(t, Time)

    def test_from_native(self):
        native = time(12, 34, 56, 789123)
        t = Time.from_native(native)
        self.assertEqual(t.hour, native.hour)
        self.assertEqual(t.minute, native.minute)
        self.assertEqual(t.second, nano_add(native.second, nano_div(native.microsecond, 1000000)))

    def test_to_native(self):
        t = Time(12, 34, 56.789123456)
        native = t.to_native()
        self.assertEqual(t.hour, native.hour)
        self.assertEqual(t.minute, native.minute)
        self.assertEqual(56.789123, nano_add(native.second, nano_div(native.microsecond, 1000000)))

    def test_iso_format(self):
        t = Time(12, 34, 56.789123456)
        self.assertEqual("12:34:56.789123456", t.iso_format())

    def test_iso_format_with_trailing_zeroes(self):
        t = Time(12, 34, 56.789)
        self.assertEqual("12:34:56.789000000", t.iso_format())
