from .IndiMessage import  IndiMessage
from . import checks
from .parts import DefBLOB, DefLight, DefNumber, DefSwitch, DefText
from . import const


class DefVector(IndiMessage):
    from_device = True
    children_class = None

    def __init__(self, device, name, state, label=None, group=None, timestamp=None, message=None, children=None, **junk):
        self.device = device
        self.name = name
        self.state = checks.dictionary(state, const.State)
        self.label = label
        self.group = group
        self.timestamp = timestamp
        self.message = message
        self.children = checks.children(children, self.children_class)


class DefWritableVector(DefVector):
    children_class = None

    def __init__(self, *args, perm, timeout=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.perm = checks.dictionary(perm, const.Permissions)
        self.timeout = timeout


class DefBLOBVector(DefWritableVector):
    children_class = DefBLOB


class DefLightVector(DefVector):
    children_class = DefLight


class DefNumberVector(DefWritableVector):
    children_class = DefNumber


class DefSwitchVector(DefWritableVector):
    children_class = DefSwitch

    def __init__(self, *args, rule, **kwargs):
        super().__init__(*args, **kwargs)
        self.rule = checks.dictionary(rule, const.SwitchRule)


class DefTextVector(DefWritableVector):
    children_class = DefText
