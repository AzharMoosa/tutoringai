from typing import Union, List
from json import JSONEncoder
import math

class GraphicQuestionEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Shape:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        raise Exception("Cannot Get String Representation of Shape")

class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float, *args, **kwargs) -> None:
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    def __str__(self) -> str:
        return "triangle"

    def calculate_area(self):
        s = (self.a + self.b + self.c) / 2.0
        area = math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
        return area

    def serialize(self):
        return {
            "a": self.a,
            "b": self.b,
            "c": self.c
        }

class Rectangle(Shape):
    def __init__(self, width: float, height: float, *args, **kwargs) -> None:
        super().__init__()
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return "rectangle"
    
    def calculate_area(self):
        return self.width * self.height

    def serialize(self):
        return {
            "width": self.width,
            "height": self.height,
        }

class Circle(Shape):
    def __init__(self, radius: float, *args, **kwargs) -> None:
        super().__init__()
        self.radius = radius

    def __str__(self) -> str:
        return "circle"
    
    def calculate_area(self):
        return math.pi * math.pow(self.radius, 2.0)
    
    def calculate_circumference(self):
        return 2.0 * math.pi * self.radius

    def serialize(self):
        return {
            "radius": self.radius,
        }
    
class GraphicalQuestion:
    def __init__(self, question: str, category: str, *args, **kwargs) -> None:
        self.question = question
        self.category = category

    def is_correct(self, user_answer: int):
        raise "ERROR: Method Access"

    def __str__(self) -> str:
        return self.question
    
    def serialize(self):
        return {
            "question": self.question,
            "category": self.category,
        }

class GraphicalQuestionSet:
    def __init__(self, questions: List[GraphicalQuestion], category: str, *args, **kwargs) -> None:
        self.questions = questions
        self.category = category
    
    def serialize(self):
        return {
            "questions": self.questions,
            "category": self.category,
        }
    
class TriangleQuestion(GraphicalQuestion):
    def __init__(self, question: str, category: str, triangle: Triangle, topic: str, answer: float, imageUrl: str, *args, **kwargs) -> None:
        super().__init__(question, category, *args, **kwargs)
        self.triangle = triangle
        self.question_type = "graphical"
        self.topic = topic
        self.answer = answer
        self.imageUrl = imageUrl

    def is_correct(self, user_answer: str):
        try:
            return math.isclose(self.answer, float(user_answer), rel_tol=1e-3)
        except ValueError:
            return False

    def __str__(self) -> str:
        return self.question
    
    def get_triangle_properties(self):
        try:
            return self.triangle.serialize()
        except:
            return Triangle(**self.triangle).serialize()
    
    def serialize(self):
        return {
            "question": self.question,
            "category": self.category,
            "triangle": self.get_triangle_properties(),
            "questionType": self.question_type,
            "topic": self.topic,
            "answer": self.answer,
            "imageUrl": self.imageUrl
        }
    
class RectangleQuestion(GraphicalQuestion):
    def __init__(self, question: str, category: str, rectangle: Rectangle, topic: str, answer: float, imageUrl: str, *args, **kwargs) -> None:
        super().__init__(question, category, *args, **kwargs)
        self.rectangle = rectangle
        self.question_type = "graphical"
        self.topic = topic
        self.answer = answer
        self.imageUrl = imageUrl

    def is_correct(self, user_answer: str):
        try:
            return math.isclose(self.answer, float(user_answer), rel_tol=1e-3)
        except ValueError:
            return False

    def __str__(self) -> str:
        return self.question
    
    def get_rectangle_properties(self):
        try:
            return self.rectangle.serialize()
        except:
            return Rectangle(**self.rectangle).serialize()
    
    def serialize(self):
        return {
            "question": self.question,
            "category": self.category,
            "rectangle": self.get_rectangle_properties(),
            "questionType": self.question_type,
            "topic": self.topic,
            "answer": self.answer,
            "imageUrl": self.imageUrl
        }
    
class CircleQuestion(GraphicalQuestion):
    def __init__(self, question: str, category: str, circle: Circle, topic: str, answer: float, imageUrl: str, *args, **kwargs) -> None:
        super().__init__(question, category, *args, **kwargs)
        self.circle = circle
        self.question_type = "graphical"
        self.topic = topic
        self.answer = answer
        self.imageUrl = imageUrl

    def is_correct(self, user_answer: str):
        try:
            return math.isclose(self.answer, float(user_answer), rel_tol=1e-3)
        except ValueError:
            return False

    def __str__(self) -> str:
        return self.question
    
    def get_circle_properties(self):
        try:
            return self.circle.serialize()
        except:
            return Circle(**self.circle).serialize()
    
    def serialize(self):
        return {
            "question": self.question,
            "category": self.category,
            "circle": self.get_circle_properties(),
            "questionType": self.question_type,
            "topic": self.topic,
            "answer": self.answer,
            "imageUrl": self.imageUrl
        }