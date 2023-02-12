from json import JSONEncoder


class Question:
    def __init__(self, question, context, answer, category, type,  *args, **kwargs) -> None:
        self.question = question
        self.context = context
        self.answer = answer
        self.category = category
        self.type = type

    def is_correct(self, user_answer):
        try:
            return int(self.answer) == int(user_answer)
        except ValueError:
            return False

    def __str__(self) -> str:
        return self.question


class QuestionEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
