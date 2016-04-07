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

from autoWire import AutoWire
from inject_decorator import inject
from post_construct_decorator import post_construct
from scope import Scope


class TestAutoWire(TestCase):
    def test_handle_plain_class_as_singleton(self):
        class PlainClassAsSingleton:
            def __repr__(self):
                return "plain singleton"

        autowire = AutoWire()
        autowire.provide(PlainClassAsSingleton)
        autowire.wire()

        self.assertEqual("plain singleton", str(autowire.get("PlainClassAsSingleton")))

    def test_handle_plain_class_as_prototype(self):
        class PlainClassAsPrototype:
            def __repr__(self):
                return "plain prototype"

        autowire = AutoWire()
        autowire.provide(PlainClassAsPrototype, scope=Scope.Prototype)
        autowire.wire()

        self.assertEqual("plain prototype", str(autowire.get("PlainClassAsPrototype")))
        self.assertNotEqual(autowire.get("PlainClassAsPrototype"), autowire.get("PlainClassAsPrototype"))

    def test_inject_plain_class_as_dependency_into_singleton(self):
        class PlainDependency:
            def __repr__(self):
                return "plain dependency"

        class SingletonWithPlainClassDependency:
            def __init__(self):
                self.plain_dependency = None

            def __repr__(self):
                return "singleton with plain class dependency - " + str(self.plain_dependency)

            @inject
            def set_plain_dependency(self, plain_dependency):
                self.plain_dependency = plain_dependency

        autowire = AutoWire()
        autowire.provide(PlainDependency)
        autowire.provide(SingletonWithPlainClassDependency)
        autowire.wire()

        self.assertEqual("singleton with plain class dependency - plain dependency",
                         str(autowire.get("SingletonWithPlainClassDependency")))

    def test_inject_chain_of_singletons(self):
        class ChainOfSingletonsEndPoint:
            def __repr__(self):
                return "end point"

        class ChainOfSingletonsMiddleLink:
            def __init__(self):
                self.end_point = None

            def __repr__(self):
                return "middle link - " + str(self.end_point)

            @inject
            def set_chain_of_singletons_end_point(self, chain_of_singletons_end_point):
                self.end_point = chain_of_singletons_end_point

        class ChainOfSingletonsFirstLink:
            def __init__(self):
                self.middle_link = None

            def __repr__(self):
                return "first link - " + str(self.middle_link)

            @inject
            def set_chain_of_singletons_middle_link(self, chain_of_singletons_middle_link):
                self.middle_link = chain_of_singletons_middle_link

        autowire = AutoWire()
        autowire.provide(ChainOfSingletonsEndPoint)
        autowire.provide(ChainOfSingletonsMiddleLink)
        autowire.provide(ChainOfSingletonsFirstLink)
        autowire.wire()

        self.assertEqual("first link - middle link - end point", str(autowire.get("ChainOfSingletonsFirstLink")))

    def test_two_singletons_with_dependency_on_same_prototype(self):
        class ThePrototypeWhichTwoSingletonsDependOn:
            pass

        class ClassOneWithDependencyOnPrototype:
            def __init__(self):
                self.my_prototype = None

            @inject
            def set_the_prototype_which_two_singletons_depend_on(self, the_prototype_which_two_singletons_depend_on):
                self.my_prototype = the_prototype_which_two_singletons_depend_on

        class ClassTwoWithDependencyOnPrototype:
            def __init__(self):
                self.my_prototype = None

            @inject
            def set_the_prototype_which_two_singletons_depend_on(self, the_prototype_which_two_singletons_depend_on):
                self.my_prototype = the_prototype_which_two_singletons_depend_on

        autowire = AutoWire()
        autowire.provide(ThePrototypeWhichTwoSingletonsDependOn, scope=Scope.Prototype)
        autowire.provide(ClassOneWithDependencyOnPrototype)
        autowire.provide(ClassTwoWithDependencyOnPrototype)
        autowire.wire()

        self.assertNotEqual(autowire.get("ClassOneWithDependencyOnPrototype").my_prototype,
                            autowire.get("ClassTwoWithDependencyOnPrototype").my_prototype)

    def test_post_construct_after_singleton_wired(self):
        class SingletonWithPostConstruct:
            def __init__(self):
                self.state = "constructed"

            def __repr__(self):
                return self.state

            @post_construct
            def setup(self):
                self.state = "post-constructed"

        autowire = AutoWire()
        autowire.provide(SingletonWithPostConstruct)
        autowire.wire()

        self.assertEqual("post-constructed", str(autowire.get("SingletonWithPostConstruct")))

    def test_post_construct_prototype_on_request(self):
        class PrototypeWithPostConstruct:
            def __init__(self):
                self.state = "constructed"

            @post_construct
            def setup(self):
                self.state = "post-constructed"

        autowire = AutoWire()
        autowire.provide(PrototypeWithPostConstruct, scope=Scope.Prototype)
        autowire.wire()

        self.assertNotEqual(autowire.get("PrototypeWithPostConstruct"), autowire.get("PrototypeWithPostConstruct"))
        self.assertEqual("post-constructed", autowire.get("PrototypeWithPostConstruct").state)

    def test_inject_auto_wire_into_singleton_so_it_can_access_components(self):
        class AnytimePrototype:
            def __repr__(self):
                return "anytime"

        class SingletonWhichDependsOnAutoWire:
            def __init__(self):
                self.auto_wire = None

            @inject
            def set_auto_wire(self, auto_wire):
                self.auto_wire = auto_wire

            def load_anytime_prototype(self):
                return self.auto_wire.get("AnytimePrototype")

        autowire = AutoWire()
        autowire.provide(AnytimePrototype, scope=Scope.Prototype)
        autowire.provide(SingletonWhichDependsOnAutoWire)
        autowire.wire()

        self.assertEqual("anytime", str(autowire.get("SingletonWhichDependsOnAutoWire").load_anytime_prototype()))

        self.assertNotEqual(autowire.get("SingletonWhichDependsOnAutoWire").load_anytime_prototype(),
                            autowire.get("SingletonWhichDependsOnAutoWire").load_anytime_prototype())

    def test_prototype_with_dependency_on_singleton_gets_dependency_wired_when_it_is_requested(self):
        class PrototypeDependency:
            def __repr__(self):
                return "prototype dependency"

        class PrototypeWithDependency:
            def __init__(self):
                self.my_dependency = None

            @inject
            def set_prototype_dependency(self, prototype_dependency):
                self.my_dependency = prototype_dependency

        autowire = AutoWire()
        autowire.provide(PrototypeDependency)
        autowire.provide(PrototypeWithDependency, scope=Scope.Prototype)
        autowire.wire()

        self.assertEqual("prototype dependency", str(autowire.get("PrototypeWithDependency").my_dependency))

        self.assertNotEqual(autowire.get("PrototypeWithDependency"),
                            autowire.get("PrototypeWithDependency"))

        self.assertEqual(autowire.get("PrototypeWithDependency").my_dependency,
                         autowire.get("PrototypeWithDependency").my_dependency)

    def test_singleton_post_construct_runs_after_dependencies_wired(self):
        class SingletonDependencyToBeInjectedBeforePostConstruct:
            def __repr__(self):
                return "the dependency"

        class SingletonClassToReceiveDependenciesBeforePostConstruct:
            def __init__(self):
                self.my_dependency = None
                self.state = "very bad"

            @inject
            def set_singleton_dependency_to_be_injected_before_post_construct(self, my_dependency):
                self.my_dependency = my_dependency

            @post_construct
            def setup(self):
                self.state = "bad"

                if self.my_dependency is not None:
                    self.state = "good - " + str(self.my_dependency)

        autowire = AutoWire()
        autowire.provide(SingletonDependencyToBeInjectedBeforePostConstruct)
        autowire.provide(SingletonClassToReceiveDependenciesBeforePostConstruct)
        autowire.wire()

        self.assertEqual("good - the dependency",
                         autowire.get("SingletonClassToReceiveDependenciesBeforePostConstruct").state)

    def test_prototype_post_construct_runs_after_dependencies_wired(self):
        class PrototypeDependencyToBeInjectedBeforePostConstruct:
            def __repr__(self):
                return "the dependency"

        class PrototypeClassToReceiveDependenciesBeforePostConstruct:
            def __init__(self):
                self.my_dependency = None
                self.state = "very bad"

            @inject
            def set_prototype_dependency_to_be_injected_before_post_construct(self, my_dependency):
                self.my_dependency = my_dependency

            @post_construct
            def setup(self):
                self.state = "bad"

                if self.my_dependency is not None:
                    self.state = "good - " + str(self.my_dependency)

        autowire = AutoWire()
        autowire.provide(PrototypeDependencyToBeInjectedBeforePostConstruct)
        autowire.provide(PrototypeClassToReceiveDependenciesBeforePostConstruct, scope=Scope.Prototype)
        autowire.wire()

        self.assertEqual("good - the dependency",
                         autowire.get("PrototypeClassToReceiveDependenciesBeforePostConstruct").state)

        self.assertNotEqual(autowire.get("PrototypeClassToReceiveDependenciesBeforePostConstruct"),
                            autowire.get("PrototypeClassToReceiveDependenciesBeforePostConstruct"))

    def test_alternate_setter_name(self):
        class DependencyForAlternateName:
            def __repr__(self):
                return "alternate"

        class ClassWithAlternateSetter:
            def __init__(self):
                self.my_dependency = None

            def __repr__(self):
                return "alt - " + str(self.my_dependency)

            @inject
            def setDependencyForAlternateName(self, my_dependency):
                self.my_dependency = my_dependency

        autowire = AutoWire()
        autowire.provide(DependencyForAlternateName)
        autowire.provide(ClassWithAlternateSetter)
        autowire.wire()

        self.assertEqual("alt - alternate", str(autowire.get("ClassWithAlternateSetter")))
