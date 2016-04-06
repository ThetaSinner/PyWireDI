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

from PyWireDI.classScanner import ClassScanner
from PyWireDI.scope import Scope


class Component:
    def __init__(self, name, clazz, scope):
        self.name = name
        self.clazz = clazz
        self.scope = scope
        self.methods_marked_inject = []

        scanner = ClassScanner(self.clazz)
        self.methods_marked_inject.extend(scanner.methods_with_decorator("inject"))

        # This will need to change if lazy loading is going to be supported at some point.
        if self.scope is Scope.Singleton:
            self.constructed_type = clazz()

    def get_name(self):
        return self.name

    def get_clazz(self):
        return self.clazz

    def get_scope(self):
        return self.scope

    def get_dependencies(self):
        return self.methods_marked_inject

    def get_instance(self):
        if self.scope == Scope.Singleton:
            return self.constructed_type
        elif self.scope == Scope.Prototype:
            return self.clazz()
