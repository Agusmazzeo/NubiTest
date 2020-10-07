import datetime

from flask import current_app

from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, DictField, ReferenceField, ListField


class Answer(Document):
    date = DateTimeField(default=datetime.datetime.utcnow)
    author = StringField()
    answers = ListField()
    related_poll = StringField()

    @classmethod
    def create(cls, poll_id: str, answer_template: dict) -> dict:
        author = answer_template.get('author', 'Unknown')
        answers = answer_template.get('answers', [])
        related_poll = Poll.get_by_id(poll_id)
        if answers != [] and len(answers) == len(related_poll.first().questions) and cls._check_valid_answers(answers, related_poll.first().possible_answers):
            answer_instance = cls(
                author=author, answers=answers, related_poll=poll_id)
            answer_instance.save()
            related_poll.update_one(push__related_answers=str(answer_instance.id))
            return dict(status=True, result='Everything is OK!')
        else:
            error = "The answers list is either empty or its length doesnt fit with the poll questions list.."
        return dict(status=False, result=error)

    @staticmethod
    def _check_valid_answers(answers:list, possible_answers:list)->bool:
        return any([True for index, answer in enumerate(answers) if answer in possible_answers[index]])


class Poll(Document):
    date = DateTimeField(default=datetime.datetime.utcnow)
    author = StringField()
    labels = ListField()
    questions = ListField()
    possible_answers = ListField()
    related_answers = ListField()

    @classmethod
    def create(cls, poll_template: dict) -> dict:
        author = poll_template.get('author', 'Unknown')
        labels = poll_template.get('labels', ['default'])
        questions = poll_template.get('questions', [])
        possible_answers = poll_template.get('possible_answers', [])
        current_app.logger.info(
            f"{author}   {labels}   {questions}   {possible_answers}")
        if questions != [] and len(questions) == len(possible_answers):
            poll_instance = cls(author=author, labels=labels, questions=questions,
                                possible_answers=possible_answers, related_answers=[])
            poll_instance.save()
            return dict(status=True, result='Everything is OK!')
        else:
            error = "The questions list is either empty or its length doesnt fit with the possible answers list.."
        return dict(status=False, result=error)

    @classmethod
    def get_all(cls):
        output = []
        result = cls.objects().as_pymongo()
        for index, item in enumerate(result):
            item['id'] = str(item['_id'])
            del(item['_id'])
            output.append(item)
        return list(result)

    @classmethod
    def get_by_id(cls, id):
        result = cls.objects(id=id)
        return result
