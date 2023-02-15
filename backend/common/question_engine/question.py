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
    
    def serialize(self):
        return {
            "question": self.question,
            "context": self.context,
            "answer": self.answer,
            "category": self.category,
            "type": self.type
        }


class QuestionEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
