import datetime

from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, DictField, ReferenceField, ListField


class User(Document):
    username = StringField()
    password = StringField()
    user_data = DictField()

    @classmethod
    def sign_in(cls, new_user: dict) -> dict:
        try:
            username = new_user.get('username')
            password = new_user.get('password')
            user_data = new_user.get('user_data', {})

            if username and password:
                if User.objects(username=username).first():
                    status = False
                    result = "Username given is already taken by another user."

                else:
                    instance = cls(username=username,
                                   password=password, user_data=user_data)
                    instance.save()
                    status = True
                    result = "The user was correctly saved."

            else:
                status = False
                result = "Username or password not sent."

        except Exception as ex:
            status = False
            result = f"An error ocurred while saving the new user:{ex}"

        finally:
            return {"status": status, "result": result}

    @classmethod
    def log_in(cls, user: dict) -> dict:
        try:
            username = user.get('username')
            password = user.get('password')

            if username and password:
                user = User.objects(username=username,
                                    password=password).first()
                if user:
                    status = True
                    result = user.id

                else:
                    status = False
                    result = "Incorrect login. Check credentials."

            else:
                status = False
                result = "Username or password not sent."

        except Exception as ex:
            status = False
            result = f"An error ocurred while login:{ex}"

        finally:
            return {"status": status, "result": result}


class Answer(Document):
    date = DateTimeField(default=datetime.datetime.utcnow)
    author = StringField()
    answers = ListField()
    related_poll = StringField()

    @classmethod
    def create(cls, poll_id: str, answer_template: dict) -> dict:
        try:
            author = answer_template.get('author', 'Unknown')
            answers = answer_template.get('answers', [])
            related_poll = Poll.get_by_id(poll_id)
            if answers != [] and len(answers) == len(related_poll.first().questions) and cls._check_valid_answers(answers, related_poll.first().possible_answers):
                answer_instance = cls(
                    author=author, answers=answers, related_poll=poll_id)
                answer_instance.save()
                related_poll.update_one(
                    push__related_answers=str(answer_instance.id))
                status = True
                result = 'Everything is OK!'
            else:
                status = False
                result = "The answers list is either empty or its length doesnt fit with the poll questions list.."
        except Exception as ex:
            status = False
            result = f"An error ocurred while saving an Answer:{ex}"

        finally:
            return {"status": status, "result": result}

    @staticmethod
    def _check_valid_answers(answers: list, possible_answers: list) -> bool:
        return any([True if answer in possible_answers[index] else False for index, answer in enumerate(answers)])


class Poll(Document):
    date = DateTimeField(default=datetime.datetime.utcnow)
    author = StringField()
    labels = DictField()
    questions = ListField()
    possible_answers = ListField()
    related_answers = ListField()

    @classmethod
    def create(cls, poll_template: dict) -> dict:
        try:
            author = poll_template.get('author', 'Unknown')
            labels = poll_template.get('labels', ['default'])
            questions = poll_template.get('questions', [])
            possible_answers = poll_template.get('possible_answers', [])
            if questions != [] and len(questions) == len(possible_answers) and cls._check_answers_len(possible_answers):
                poll_instance = cls(author=author, labels=labels, questions=questions,
                                    possible_answers=possible_answers, related_answers=[])
                poll_instance.save()
                status=True
                result='Everything is OK!'
            else:
                status = False
                result = "The questions list is either empty or there is a problem with answers length.."
        except Exception as ex:
            status = False
            result = f"An error ocurred while saving a Poll:{ex}"

        finally:
            return {"status": status, "result": result}

    @classmethod
    def get_all(cls):
        try:
            output = []
            status = True
            result = cls.objects().as_pymongo()
            for index, item in enumerate(result):
                item['id'] = str(item['_id'])
                del(item['_id'])
                output.append(item)
            result = output
        except Exception as ex:
            status = False
            result = f"An error ocurred while querying all Polls:{ex}"

        finally:
            return {"status": status, "result": result}

    @classmethod
    def get_by_id(cls, id):
        try:
            status = True
            result = cls.objects(id=id)
        except Exception as ex:
            status = False
            result = f"An error ocurred while querying one Poll:{ex}"

        finally:
            return {"status": status, "result": result}

    @classmethod
    def get_by_labels(cls, labels: dict) -> list:
        try:
            output = []
            result = cls.objects(labels=labels).as_pymongo()
            for index, item in enumerate(result):
                item['id'] = str(item['_id'])
                del(item['_id'])
                output.append(item)
            status = True
            result = output
        except Exception as ex:
            status = False
            result = f"An error ocurred while querying one Poll:{ex}"

        finally:
            return {"status": status, "result": result}

    @staticmethod
    def _check_answers_len(answers_list: list) -> bool:
        return all([True if len(answers) <= 4 else False for answers in answers_list])
