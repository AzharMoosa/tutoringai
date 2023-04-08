from json import JSONEncoder
from typing import Any, List

class Question:
    def __init__(self, question: str, category: str, topic: str, *args, **kwargs) -> None:
        self.question = question
        self.category = category
        self.topic = topic

    def __str__(self) -> str:
        return self.question
    
    def serialize(self):
        return {
            "question": self.question,
            "category": self.category,
            "topic": self.topic,
        }

class NumericalQuestion(Question):
    def __init__(self, question: str, category: str, topic: str, answer: int, *args, **kwargs) -> None:
        super().__init__(question, category, topic)
        self.answer = answer
        self.question_type = "numerical"

    def is_correct(self, user_answer: int):
        try:
            return self.answer == user_answer
        except ValueError:
            return False

    def __str__(self) -> str:
        return self.question
    
    def serialize(self):
        return {
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "topic": self.topic,
            "question_type": self.question_type
        }

class MultipleChoiceQuestion(Question):
    def __init__(self, question: str, category: str, topic: str, answer: int, options: List[str], text: str, *args, **kwargs) -> None:
        super().__init__(question, category, topic)
        self.answer = answer
        self.options = options
        self.text = text
        self.question_type = "mcq"

    def is_correct(self, user_answer: str):
        try:
            return self.answer == user_answer
        except ValueError:
            return False

    def __str__(self) -> str:
        return self.question
    
    def serialize(self):
        return {
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "topic": self.topic,
            "options": self.options,
            "text": self.text,
            "question_type": self.question_type
        }


class QuestionEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
