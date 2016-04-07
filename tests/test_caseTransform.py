"""
Copyright 2016 Gregory Jensen

This file is part of PyWireDI.

PyWireDI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyWireDI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyWireDI.  If not, see <http://www.gnu.org/licenses/>.
"""

from unittest import TestCase

from caseTransform import CaseTransform


class TestCaseTransform(TestCase):
    def test_pascal_case_to_underscore(self):
        self.assertEquals("test_case", CaseTransform().pascal_case_to_underscore("TestCase"))
        self.assertEquals("test_case", CaseTransform().pascal_case_to_underscore("testCase"))

    def test_underscore_to_pascal_case(self):
        self.assertEquals("TestCase", CaseTransform().underscore_to_pascal_case("test_case"))
