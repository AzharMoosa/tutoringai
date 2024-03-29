from pymongo import MongoClient
from dotenv import load_dotenv
import os
from typing import Union, List
import json
from json import JSONEncoder
import cloudinary
import cloudinary.uploader
from backend.common.question_engine.graphics_question import *
from backend.common.question_engine.text_to_graphics_question import TextToGraphicsQuestion

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

class GraphicsQuestionEngine:
    @staticmethod
    def __push_to_question_bank(questions: List[GraphicalQuestion]) -> None:
        questions_json = json.dumps(questions, indent=4, cls=GraphicQuestionEncoder)
        db = client["Questions"]
        question_bank = db["question_bank"]
        question_bank.insert_many(json.loads(questions_json))

    @staticmethod
    def __parse_template(template: dict) -> List[GraphicalQuestion]:
        return TextToGraphicsQuestion.generate_questions(template["text"], template["category"])

    @staticmethod
    def __get_templates():
        return [{ "category" : "trigonometry", "text" : "A triangle has side lengths 1, 2, 3." },
                { "category" : "trigonometry", "text" : "In this triangle, the side lengths are 1, 2, 3." },
                { "category" : "trigonometry", "text" : "Suppose we have a triangle with side lengths 1, 2, 3." },
                { "category" : "rectangle", "text" : "A rectangle has width 2 and height 3." },
                { "category" : "rectangle", "text" : "In this rectangle, the width is 2 and height is 3." },
                { "category" : "rectangle", "text" : "Suppose we have a rectangle with width 2 and height 3." },
                { "category" : "circle", "text" : "A circle has radius 2." },
                { "category" : "circle", "text" : "In this circle, the radius is 2." },
                { "category" : "circle", "text" : "Suppose we have a circle with radius 2." }]
    
    @staticmethod
    def create_graphics_engine():
        # Change Directory To Graphics Engine
        os.chdir(f"{__location__}/../graphical_engine")
        
        # Make Graphics Engine Executable
        if os.system("make clean && make") != 0:
            raise Exception("Cannot Create Graphical Engine")

        print("Created Graphical Engine Executable")

    @staticmethod
    def generate_graphical_questions(clear_db=False):
        templates = GraphicsQuestionEngine.__get_templates()

        if clear_db:
            db = client["Questions"]
            question_bank = db["question_bank"]
            question_bank.drop()

        for i, template in enumerate(templates):
            print(f"============ PARSING TEMPLATE {i} ============")
            # 1 - Parse Template & Generate Question Variants
            question_variants = GraphicsQuestionEngine.__parse_template(template)

            print(f"Generated {len(question_variants)} Question Variants")

            question_sets = [GraphicalQuestionSet(question_variants, template["category"])]

            print(f"Generated {len(question_sets)} Question Sets")

            # 3 - Push To Question Bank
            GraphicsQuestionEngine.__push_to_question_bank(question_sets)

            print(f"Successfully Added {len(question_sets)} Questions Sets!")
            print(f"==== GENERATED QUESTIONS FOR TEMPLATE {i} ====")
        
        os.system("make clean")

if __name__ == "__main__":
    GraphicsQuestionEngine.create_graphics_engine()
    GraphicsQuestionEngine.generate_graphical_questions()