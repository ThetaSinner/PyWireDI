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
