from models import Question
from random import randint, choice

test_bd = [
    {'question': 'test_questions1', 'answer': 'right answer1', 'options': ['incorrect answer2', 'incorrect answer3', 'incorrect answer4', 'right answer1',]},
    {'question': 'test_questions2', 'answer': 'right answer2', 'options': ['incorrect answer2', 'incorrect answer3', 'incorrect answer4', 'right answer2',]},
    {'question': 'test_questions3', 'answer': 'right answer3', 'options': ['incorrect answer2', 'incorrect answer3', 'incorrect answer4', 'right answer3',]},
    {'question': 'test_questions4', 'answer': 'right answer4', 'options': ['incorrect answer2', 'incorrect answer3', 'incorrect answer4', 'right answer4',]},
    {'question': 'test_questions5', 'answer': 'right answer5', 'options': ['incorrect answer2', 'incorrect answer3', 'incorrect answer4', 'right answer5',]},
    {'question': 'test_questions6', 'answer': 'right answer6', 'options': ['incorrect answer2', 'incorrect answer3', 'incorrect answer4', 'right answer6',]},
]

def class10_get_question() -> Question:
    question = choice(test_bd)
    return Question(**question)
