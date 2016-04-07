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

from autoWire import AutoWire
from inject_decorator import inject
from post_construct_decorator import post_construct


class Model:
    def __init__(self):
        self.value = "model value"

    def get_value(self):
        return self.value


class View:
    def __init__(self):
        self.controller = None

    @inject
    def set_controller(self, controller):
        self.controller = controller

    @staticmethod
    def display_value(value):
        print(value)


class Controller:
    def __init__(self):
        self.model = None
        self.view = None

    @inject
    def set_model(self, model):
        self.model = model

    @inject
    def set_view(self, view):
        self.view = view

    @post_construct
    def init_mvc(self):
        val = self.model.get_value()
        self.view.display_value(val)


autowire = AutoWire()
autowire.provide(Model)
autowire.provide(View)
autowire.provide(Controller)
autowire.wire()
