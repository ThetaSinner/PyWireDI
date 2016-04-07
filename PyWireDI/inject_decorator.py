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


def inject(method):
    def forward_method(*args, **kwargs):
        return method(*args, **kwargs)

    return forward_method
