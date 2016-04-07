# PyWireDI
Dependency Injection for Python

### Example - MVC
```python
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
```
  
