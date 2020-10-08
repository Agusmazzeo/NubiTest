from unittest import TestCase, mock
from mongoengine import connect, disconnect

from nubi_test.models.mongo import Poll, Answer


class TestPoll(TestCase):

    poll_template_1 = {
        "author": "Martin",
        "labels": {"test": True, "prod": False},
        "questions": ["Que dia es?", "Como estas?"],
        "possible_answers": [["Lunes", "Martes"], ["Todo bien", "Todo mal"]]
    }

    poll_template_2 = {
        "author": "Juan",
        "labels": {"test": True},
        "questions": ["De que cuadro sos?", "Vas a la cancha?"],
        "possible_answers": [["River", "Racing"], ["Se", "Na"]]
    }


    @classmethod
    def setUpClass(cls):
        cls.database = connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_create(self):
        self.database.drop_database('mongoenginetest')
        result = Poll.create(self.poll_template_1)

        assert result == dict(status=True, result='Everything is OK!')

        check_poll = Poll.objects().first()
        
        assert check_poll.author == "Martin"
        assert check_poll.labels == {"test": True, "prod": False}
        assert check_poll.questions == ["Que dia es?", "Como estas?"]
        assert check_poll.possible_answers == [["Lunes", "Martes"], ["Todo bien", "Todo mal"]]

    def test_get_all(self):
        self.database.drop_database('mongoenginetest')
        result = Poll.create(self.poll_template_1)
        assert result == dict(status=True, result='Everything is OK!')
        result = Poll.create(self.poll_template_2)
        assert result == dict(status=True, result='Everything is OK!')
        
        check_poll = Poll.get_all()
        assert len(check_poll) == 2
        assert check_poll[0]["author"] == "Martin"
        assert check_poll[1]["author"] == "Juan"