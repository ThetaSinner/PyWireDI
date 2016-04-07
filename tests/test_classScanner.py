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

from classScanner import ClassScanner
from inject_decorator import inject


class TestClassScanner(TestCase):
    def test_scan_class_with_no_decorators(self):
        class TestClassWithNoDecorators:
            pass

        class_scanner = ClassScanner(TestClassWithNoDecorators)

        self.assertEqual(0, len(class_scanner.methods_with_decorator("inject")))

    def test_scan_class_with_no_matching_decorators(self):
        class TestClassWithNoMatchingDecorators:
            @staticmethod
            def get_number():
                pass

        class_scanner = ClassScanner(TestClassWithNoMatchingDecorators)

        self.assertEqual(0, len(class_scanner.methods_with_decorator("inject")))

    def test_scan_class_with_one_matching_decorator(self):
        class TestClassWithOneMatchingDecorators:
            @inject
            def set_property(self):
                pass

        class_scanner = ClassScanner(TestClassWithOneMatchingDecorators)

        methods_with_decorator = class_scanner.methods_with_decorator("inject")
        self.assertEqual(1, len(methods_with_decorator))
        self.assertEqual("set_property", methods_with_decorator[0])

    def test_scan_class_with_multiple_matching_decorators(self):
        class TestClassWithMultipleMatchingDecorators:
            @inject
            def set_property(self):
                pass

            @inject
            def set_field(self):
                pass

        class_scanner = ClassScanner(TestClassWithMultipleMatchingDecorators)

        methods_with_decorator = class_scanner.methods_with_decorator("inject")
        self.assertEqual(2, len(methods_with_decorator))
        self.assertEqual("set_property", methods_with_decorator[0])
        self.assertEqual("set_field", methods_with_decorator[1])

    def test_scan_class_with_multiple_mixed_decorators(self):
        class TestClassWithMultipleMixedDecorators:
            @inject
            def set_property(self):
                pass

            @staticmethod
            def operation():
                pass

            @inject
            def set_field(self):
                pass

            @classmethod
            def action(cls):
                pass

        class_scanner = ClassScanner(TestClassWithMultipleMixedDecorators)

        methods_with_decorator = class_scanner.methods_with_decorator("inject")
        self.assertEqual(2, len(methods_with_decorator))
        self.assertEqual("set_property", methods_with_decorator[0])
        self.assertEqual("set_field", methods_with_decorator[1])
