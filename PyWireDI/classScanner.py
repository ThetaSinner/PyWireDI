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

import inspect


class ClassScanner:
    def __init__(self, clazz):
        self.clazz = clazz

    def methods_with_decorator(self, decorator_name):
        results = []

        source_lines = inspect.getsourcelines(self.clazz)[0]
        next_method_is_decorated = False
        for line in source_lines:
            line = line.strip()
            if self._is_line_decorated_by_method(line, decorator_name):
                next_method_is_decorated = True

            if next_method_is_decorated and self._is_line_member_method_signature(line):
                name = line.split('def')[1].split('(')[0].strip()
                results.append(name)
                next_method_is_decorated = False

        return results

    @staticmethod
    def _is_line_decorated_by_method(line, decorator_name):
        return line.split('(')[0].strip() == '@' + decorator_name

    def _is_line_member_method_signature(self, line):
        if line.find("def") == -1:
            return False

        name = line.split('def')[1].split('(')[0].strip()

        return hasattr(self.clazz, name)
