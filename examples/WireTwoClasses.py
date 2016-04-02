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

from PyWireDI.autoWire import AutoWire
from PyWireDI.inject_decorator import inject


class ClassA:
    def __init__(self):
        self.class_b = None

    @inject
    def set_class_b(self, class_b):
        self.class_b = class_b

    def run(self):
        print(self)
        print(self.class_b)

    def __repr__(self):
        return "I am ClassA"


class ClassB:
    def __repr__(self):
        return "I am ClassB"


wiring = AutoWire()

# Tell AutoWire about the classes you want it to manage.
wiring.provide(ClassA)
wiring.provide(ClassB)

# AutoWire will scan construct and scan everything you told it about and call all setters
# marked inject.
wiring.wire()

# Fetch the constructed type for ClassA and call the run method on it.
wiring.get("ClassA").run()

# Prints out
#
# I am ClassA
# I am ClassB
#

