from indi.message.IndiMessage import IndiMessage
from indi.message import checks
from indi.message.parts import OneBLOB, OneNumber, OneSwitch, OneText


class NewVector(IndiMessage):
    children_class = None
    from_client = True

    def __init__(self, device, name, timestamp=None, children=None, **junk):
        self.device = device
        self.name = name
        self.timestamp = timestamp
        self.children = checks.children(children, self.children_class)


class NewBLOBVector(NewVector):
    children_class = OneBLOB


class NewNumberVector(NewVector):
    children_class = OneNumber


class NewSwitchVector(NewVector):
    children_class = OneSwitch


class NewTextVector(NewVector):
    children_class = OneText
