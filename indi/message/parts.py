import xml.etree.cElementTree as ET
from . import checks
from . import const


class IndiMessagePart:
    @classmethod
    def tag_name(cls):
        return cls.__name__[:1].lower() + cls.__name__[1:]

    @classmethod
    def _all_subclasses(cls):
        return cls.__subclasses__()

    @classmethod
    def from_xml(cls, xml):
        tag = xml.tag
        message_class = None

        for subclass in cls._all_subclasses():
            if subclass.tag_name() == tag:
                message_class = subclass

        if not message_class:
            raise Exception(f'Invalid part: {tag}')

        kwargs = xml.attrib

        kwargs['value'] = xml.text.strip() if xml.text else None

        return message_class(**kwargs)

    def to_xml(self, parent):
        kwargs = {k: str(v) for k, v in self.__dict__.items() if v is not None and k not in ('value',)}

        element = ET.SubElement(parent, self.__class__.tag_name(), **kwargs)
        if hasattr(self, 'value') and self.value is not None:
            element.text = str(self.value)

        return element


class DefIndiMessagePart(IndiMessagePart):
    def __init__(self, name: str, label: str=None, **junk):
        self.name = name
        self.label = label


class DefBLOB(DefIndiMessagePart):
    pass


class DefLight(DefIndiMessagePart):
    pass


class DefNumber(DefIndiMessagePart):
    def __init__(self, name: str, format, min, max, step, label: str=None, **junk):
        super().__init__(name, label)
        self.format = format
        self.min = min
        self.max = max
        self.step = step


class DefSwitch(DefIndiMessagePart):
    pass


class DefText(DefIndiMessagePart):
    pass


class OneIndiMessagePart(IndiMessagePart):
    def __init__(self, name, value, **junk):
        self.name = name
        self.value = value


class OneBLOB(OneIndiMessagePart):
    def __init__(self, name, size, format, value, **junk):
        super().__init__(name, value)
        self.size = size
        self.format = format


class OneLight(OneIndiMessagePart):
    def __init__(self, name, value, **junk):
        super().__init__(name, checks.dictionary(value, const.State))


class OneNumber(OneIndiMessagePart):
    pass


class OneSwitch(OneIndiMessagePart):
    def __init__(self, name, value, **junk):
        super().__init__(name, checks.dictionary(value, const.SwitchState))


class OneText(OneIndiMessagePart):
    pass
