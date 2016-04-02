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

from PyWireDI.caseTransform import CaseTransform
from PyWireDI.classScanner import ClassScanner
from PyWireDI.component import Component
from PyWireDI.scope import Scope


class AutoWire:
    def __init__(self):
        self.type_manager_list = {}

    def provide(self, clazz, name=None, scope=None):
        if name is None:
            name = clazz.__name__

        if scope is None:
            scope = Scope.Singleton

        self.type_manager_list[name] = Component(name, clazz, scope)

    @staticmethod
    def get_inject_property_name_from_method_name(method_name):
        inject_property_name = ""

        if method_name.find("set_") != -1:
            inject_property_name = method_name[4:]
        elif method_name.find("set") != -1:
            inject_property_name = method_name[3:]
            inject_property_name = CaseTransform.pascal_case_to_underscore(inject_property_name)

        return inject_property_name

    def wire(self):
        for type_manager_key in self.type_manager_list:
            type_manager = self.type_manager_list[type_manager_key]
            if type_manager.get_scope() is Scope.Singleton:
                self.auto_wire_managed_type(type_manager)

        self._post_construct()

    def auto_wire_managed_type(self, managed_type):
        built_clazz = managed_type.get_instance()

        for dependency_setter_method_names in managed_type.get_dependencies():
            dependency = self.get_inject_property_name_from_method_name(dependency_setter_method_names)
            dependency = CaseTransform.underscore_to_pascal_case(dependency)

            if dependency == "AutoWire":
                getattr(built_clazz, dependency_setter_method_names)(self)
            else:
                getattr(built_clazz, dependency_setter_method_names)(self.get(dependency))

        return built_clazz

    def get(self, clazz_name):
        managed_type = self.type_manager_list[clazz_name]
        if managed_type.get_scope() is Scope.Singleton:
            return managed_type.get_instance()
        elif managed_type.get_scope() is Scope.Prototype:
            return self.auto_wire_managed_type(managed_type)

    def _post_construct(self):
        for type_manager_key in self.type_manager_list:
            type_manager = self.type_manager_list[type_manager_key]
            if type_manager.get_scope() is Scope.Singleton:
                post_construct_methods = ClassScanner(type_manager.get_clazz()).methods_with_decorator("post_construct")
                if len(post_construct_methods) > 0:
                    getattr(type_manager.get_instance(), post_construct_methods[0])()
