import re
import json
from collections import namedtuple
from json import JSONEncoder
import os
from question import Question, QuestionEncoder
from question_transformer import model, tokenizer

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


class QuestionEngine:
    @staticmethod
    def process_template(statement, answer, attributes):
        def process_attribute(x):
            tag = x.group(1)
            is_list = re.match(r"\[(.*?)\]", tag)

            if is_list:
                target_list = is_list.group(1)
                return ", ".join(attributes[target_list])

            is_list_access = re.match(r"(.*?)\[(\d)\]", tag)

            if is_list_access:
                target_list, idx = is_list_access.group(
                    1), is_list_access.group(2)
                try:
                    attribute_list = attributes[target_list]
                    return attribute_list[int(idx)]
                except:
                    raise Exception("Invalid List Access")

            if tag not in attributes:
                raise Exception("Invalid Tag")

            return attributes[tag]

        parsed_statement = re.sub(
            r'\<(.*?)\>', lambda x: process_attribute(x), statement)
        parsed_answer = re.sub(
            r'\<(.*?)\>', lambda x: process_attribute(x), answer)
        answer_value = re.findall(r'\d+', parsed_answer)[0]

        return parsed_answer, parsed_statement, answer_value

    @staticmethod
    def generate_questions():
        with open(f"{__location__}/question_bank.json") as question_bank:
            data = json.load(question_bank)
            return sum([QuestionEngine.generate_question_list(question_info) for question_info in data], [])

    @staticmethod
    def generate_question_list(question_info):
        def get_question(answer, context, max_length=128):
            input_text = f"answer: {answer}  context: {context} </s>"
            features = tokenizer([input_text], return_tensors='pt')

            output = model.generate(
                input_ids=features['input_ids'], attention_mask=features['attention_mask'], max_length=max_length)

            return tokenizer.decode(output[0])

        def generate_question(template, category, type):
            try:
                statement = template.pop("statement", None)
                answer = template.pop("answer", None)

                parsed_answer, parsed_context, answer_value = QuestionEngine.process_template(
                    statement, answer, template)

                extracted_question = re.search(
                    'question: (.+?)\?', get_question(parsed_answer, parsed_context)).group(1)
            except AttributeError:
                raise Exception("Error Generating Question")

            return Question(f"{parsed_context} {extracted_question}?", parsed_context, answer_value, category, type)

        return [generate_question(template, question_info["category"], question_info["type"]) for template in question_info["templates"]]


def update_questions():
    # TODO: Store In Database
    generated_questions = QuestionEngine.generate_questions()
    questions_json = json.dumps(
        generated_questions, indent=4, cls=QuestionEncoder)

    with open(f"{__location__}/questions.json", "w") as f:
        f.write(questions_json)


if __name__ == "__main__":
    update_questions()
