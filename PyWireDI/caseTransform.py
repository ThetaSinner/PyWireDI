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


class CaseTransform:
    @staticmethod
    def pascal_case_to_underscore(pascal_case):
        result = ""
        for letter in pascal_case:
            if letter.isupper():
                result = result + "_" + letter.lower()
            else:
                result += letter

        if len(result) is not 0 and result[0] == '_':
            result = result[1:]

        return result

    @staticmethod
    def underscore_to_pascal_case(pascal_case):
        result = ""
        last_was_underscore = True
        for letter in pascal_case:
            if last_was_underscore and letter != '_':
                result += letter.upper()
                last_was_underscore = False
            else:
                if letter == '_':
                    last_was_underscore = True
                else:
                    result += letter

        if len(result) is not 0 and result[0].islower():
            result = result[0].upper() + result[1:]

        return result
