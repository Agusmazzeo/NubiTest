from unittest import TestCase, mock
from mongoengine import connect, disconnect

from nubi_test.models.mongo import Poll, Answer


class TestPoll(TestCase):

    poll_template = {
        "author": "Martin",
        "labels": {"test": True, "prod": False},
        "questions": ["Que dia es?", "Como estas?"],
        "possible_answers": [["Lunes", "Martes"], ["Todo bien", "Todo mal"]]
    }

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_create(self):
        result = Poll.create(self.poll_template)

        assert result == dict(status=True, result='Everything is OK!')

        check_poll = Poll.objects().first()
        
        assert check_poll.author == "Martin"
        assert check_poll.labels == {"test": True, "prod": False}
        assert check_poll.questions == ["Que dia es?", "Como estas?"]
        assert check_poll.possible_answers == [["Lunes", "Martes"], ["Todo bien", "Todo mal"]]