import unittest
from indi import message
from indi.message import parts
from ddt import ddt, data, unpack


@ddt
class TestIndiMessage(unittest.TestCase):

    messages = [
        (
            '<getProperties device="CAMERA" version="2.0" />',
            message.GetProperties(version='2.0', device='CAMERA'),
        ),
        (
            '<getProperties version="2.0" />',
            message.GetProperties(version='2.0'),
        ),
        (
            '<newNumberVector device="CAMERA" name="EXPOSE"><oneNumber name="TIME">10</oneNumber></newNumberVector>',
            message.NewNumberVector(device='CAMERA', name='EXPOSE', children=[parts.OneNumber(name='TIME', value='10')]),
        ),
    ]

    @classmethod
    def message_to_dict(cls, msg):
        d = { k: v for k, v in msg.__dict__.items()}
        if 'children' in d:
            d['children'] = [cls.message_to_dict(c) for c in d['children']]
        return d

    @data(*messages)
    @unpack
    def test_from_string(self, in_xml, in_msg):
        msg = message.IndiMessage.from_string(bytes(in_xml, encoding='ascii'))
        self.assertDictEqual(self.message_to_dict(in_msg), self.message_to_dict(msg))
        self.assertEqual(in_msg.__class__, msg.__class__)

    @data(*messages)
    @unpack
    def test_to_string(self, in_xml, in_msg):
        xml = in_msg.to_string()
        self.assertEqual(bytes(in_xml, encoding='ascii'), xml)
