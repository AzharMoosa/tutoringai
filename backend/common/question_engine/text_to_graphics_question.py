from typing import List, Union
import re
import random
from graphics_question import *
import os
import cloudinary
import cloudinary.uploader

class TextToGraphicsQuestion:
    @staticmethod
    def __randomize_numbers(text: str):
        numbers = re.findall(r'\d+', text)

        for number in numbers:
            new_number = str(random.randint(1, 10))
            text = text.replace(number, new_number)
        
        return text
    
    @staticmethod
    def __find_numbers(text: str):
        return [float(s) for s in re.findall(r'\d+', text)]
    
    @staticmethod
    def __generate_shape_image(shape: Union[Triangle, Rectangle, Circle]):
        command = "./graphical_engine "
        # Generate Shape Using Graphics Engine
        if isinstance(shape, Triangle):
            shape.__class__ = Triangle
            command += f"{shape} {shape.a} {shape.b} {shape.c}"
        elif isinstance(shape, Rectangle):
            shape.__class__ = Rectangle
            command += f"{shape} {shape.width} {shape.height}"
        elif isinstance(shape, Circle):
            shape.__class__ = Circle
            command += f"{shape} {shape.radius}"

        os.system(command)
        # Get Image & Store In Cloudinary
        cloudinary.config(cloud_name=os.getenv("CLOUD_NAME"), api_key=os.getenv("CLOUDINARY_API"), api_secret=os.getenv("CLOUDINARY_API_SECRET"))
        upload_result = cloudinary.uploader.upload(f'{shape}.png')
        os.remove(f'{shape}.png')
        return upload_result["url"]

    @staticmethod
    def __generate_triangle_questions(text, area_questions=10, angle_questions=10) -> List[TriangleQuestion]:
        questions = []
        # Generate Area Questions
        for _ in range(area_questions):
            question = TextToGraphicsQuestion.__randomize_numbers(text) + " What is the area of the triangle?"
            A, B, C = TextToGraphicsQuestion.__find_numbers(question)
            if (A + B > C and A + C > B and B + C > A):
                triangle = Triangle(A, B, C)
                area = triangle.calculate_area()
                image_url = TextToGraphicsQuestion.__generate_shape_image(triangle)
                questions.append(TriangleQuestion(question, "trigonometry", triangle, "graphical", "area", area, image_url))
        
        return questions
    
    @staticmethod
    def __generate_rectangle_questions(text, area_questions=10):
        questions = []
        # Generate Area Questions
        for _ in range(area_questions):
            question = TextToGraphicsQuestion.__randomize_numbers(text) + " What is the area of the rectangle?"
            WIDTH, HEIGHT = TextToGraphicsQuestion.__find_numbers(question)
            rectangle = Rectangle(WIDTH, HEIGHT)
            area = rectangle.calculate_area()
            image_url = TextToGraphicsQuestion.__generate_shape_image(rectangle)
            questions.append(RectangleQuestion(question, "rectangle", rectangle, "graphical", "area", area, image_url))
        
        return questions
    
    @staticmethod
    def __generate_circle_questions(text, area_questions=10, circumference_questions=10):
        questions = []
        # Generate Area Questions
        for _ in range(area_questions):
            question = TextToGraphicsQuestion.__randomize_numbers(text) + " What is the area of the circle?"
            numbers = TextToGraphicsQuestion.__find_numbers(question)
            circle = Circle(numbers[0])
            area = circle.calculate_area()
            image_url = TextToGraphicsQuestion.__generate_shape_image(circle)
            questions.append(CircleQuestion(question, "circle", circle, "graphical", "area", area, image_url))
        
        for _ in range(circumference_questions):
            question = TextToGraphicsQuestion.__randomize_numbers(text) + " What is the circumference of the circle?"
            numbers = TextToGraphicsQuestion.__find_numbers(question)
            circle = Circle(numbers[0])
            circumference = circle.calculate_circumference()
            image_url = TextToGraphicsQuestion.__generate_shape_image(circle)
            questions.append(CircleQuestion(question, "circle", circle, "graphical", "circumference", circumference, image_url))

        return questions

    @staticmethod
    def generate_questions(text: str, category: str) -> List[GraphicalQuestion]:
        if (category == "trigonometry"):
            return TextToGraphicsQuestion.__generate_triangle_questions(text)
        elif (category == "rectangle"):
            return TextToGraphicsQuestion.__generate_rectangle_questions(text)
        elif (category == "circle"):
            return TextToGraphicsQuestion.__generate_circle_questions(text)
        else:
            raise Exception(f"Graphical Question Type {category} Not Defined")

