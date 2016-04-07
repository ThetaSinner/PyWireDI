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

from PyWireDI.component import Component
from PyWireDI.scope import Scope
from inject_decorator import inject


class TestComponent(TestCase):
    def test_get_constructed_values(self):
        class TestGetConstructedValuesClazz:
            pass

        component = Component("TestGetConstructedValuesClazz", TestGetConstructedValuesClazz, Scope.Singleton)

        self.assertEquals("TestGetConstructedValuesClazz", component.get_name())
        self.assertTrue(isinstance(component.get_clazz()(), TestGetConstructedValuesClazz))
        self.assertEqual(Scope.Singleton, component.get_scope())

    def test_get_constructed_values_alt(self):
        class TestGetConstructedValuesAltClazz:
            pass

        component = Component("RandomName", TestGetConstructedValuesAltClazz, Scope.Prototype)

        self.assertEquals("RandomName", component.get_name())
        self.assertTrue(isinstance(component.get_clazz()(), TestGetConstructedValuesAltClazz))
        self.assertEqual(Scope.Prototype, component.get_scope())

    def test_get_dependencies_with_no_dependencies(self):
        class TestGetDependenciesWithNoDependenciesClazz:
            pass

        component = Component("TestGetDependenciesWithNoDependenciesClazz", TestGetDependenciesWithNoDependenciesClazz, Scope.Singleton)

        self.assertEqual(0, len(component.get_dependencies()))

    def test_get_dependencies(self):
        class TestGetDependenciesClazz:
            @inject
            def test_dependency(self):
                pass

        component = Component("TestGetDependenciesClazz", TestGetDependenciesClazz, Scope.Singleton)

        self.assertEqual(["test_dependency"], component.get_dependencies())

    def test_get_instance_always_returns_same_object_for_scope_singleton(self):
        class TestSingletonInstance:
            pass

        component = Component("TestSingletonInstance", TestSingletonInstance, Scope.Singleton)

        self.assertEqual(component.get_instance(), component.get_instance())

    def test_get_instance_always_returns_a_different_object_for_scope_prototype(self):
        class TestPrototypeInstance:
            pass

        component = Component("TestPrototypeInstance", TestPrototypeInstance, Scope.Prototype)

        self.assertNotEqual(component.get_instance(), component.get_instance())
