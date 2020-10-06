import datetime

from flask import current_app

from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, DictField, ReferenceField, ListField


class Poll(Document):
    date = DateTimeField(default=datetime.datetime.utcnow)
    author = StringField()
    labels = ListField()
    questions = ListField()
    possible_answers = ListField()

    @classmethod
    def create(cls, poll_template: dict) -> bool:
        author = poll_template.get('author', 'Unknown')
        labels = poll_template.get('labels', ['default'])
        questions = poll_template.get('questions', [])
        possible_answers = poll_template.get('possible_answers', [])
        current_app.logger.info(f"{author}   {labels}   {questions}   {possible_answers}")
        if questions != [] and len(questions) == len(possible_answers):
            poll_instance = cls(author=author, labels=labels, questions=questions, possible_answers=possible_answers)
            poll_instance.save()
            return True
        return False

    @classmethod
    def get_all(cls):
        output = []
        result = cls.objects().as_pymongo()
        for index, item in enumerate(result):
            item['id'] = str(item['_id'])
            del(item['_id'])
            output.append(item)
        return list(result)



class Answer(Document):
    date = DateTimeField(default=datetime.datetime.utcnow)
    author = StringField()
    answers = ListField(StringField)
    related_poll = ReferenceField(Poll)

    @classmethod
    def create(cls, poll_id: str, answer_template: dict) -> bool:
        author = answer_template.get('author', 'Unknown')
        questions = answer_template.get('questions', [])

        if questions != []:
            poll_instance = cls(author=author, questions=questions)
            instance.save()
            return True
        return False
