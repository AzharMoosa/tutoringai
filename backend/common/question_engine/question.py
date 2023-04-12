from json import JSONEncoder
from typing import Any, List
import random

class Question:
    def __init__(self, question: str, category: str, topic: str, *args, **kwargs) -> None:
        self.question = question
        self.category = category
        self.topic = topic

    def is_correct(self, user_answer: int):
        raise "ERROR: Method Access"

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

    def is_correct(self, user_answer: str):
        try:
            return self.answer == int(user_answer)
        except ValueError:
            return False

    def __str__(self) -> str:
        return self.question
    
    def serialize(self):
        return {
            "question": self.question,
            "category": self.category,
            "topic": self.topic,
            "answer": self.answer,
            "questionType": self.question_type
        }

class MultipleChoiceQuestion(Question):
    def __init__(self, question: str, category: str, topic: str, answer: str, options: List[str], text: str, *args, **kwargs) -> None:
        super().__init__(question, category, topic)
        self.answer = answer
        self.options = options
        self.text = text
        self.question_type = "mcq"

    def is_correct(self, user_answer: str):
        try:
            return self.answer.lower() == user_answer.lower() 
        except ValueError:
            return False

    def __str__(self) -> str:
        return f"{self.text} {self.question}"
    
    def serialize(self):
        return {
            "question": f"{self.text}. {self.question}",
            "category": self.category,
            "topic": self.topic,
            "answer": self.answer,
            "options": self.options,
            "text": self.text,
            "questionType": self.question_type
        }

class TrueOrFalseQuestion(Question):
    def __init__(self, question: str, category: str, topic: str, answer: bool, statement: str, *args, **kwargs) -> None:
        super().__init__(question, category, topic)
        self.answer = answer
        self.statement = statement
        self.question_type = "true-or-false"

    def is_correct(self, user_answer: str):
        return self.answer if user_answer in ('True', 'true') else not self.answer

    def __str__(self) -> str:
        return self.question
    
    def serialize(self):
        return {
            "question": self.question,
            "category": self.category,
            "topic": self.topic,
            "answer": self.answer,
            "statement": self.statement,
            "questionType": self.question_type
        }

class QuestionEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
