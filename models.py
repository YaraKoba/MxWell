from dataclasses import dataclass
from typing import List

class Result:
    def __init__(self):
        self.right_ans = 0
        self.incorrect_ans = 0
        
    def add_right_ans(self):
        self.right_ans += 1
    
    def add_incorrect_ans(self):
        self.incorrect_ans += 1
        
    def clear_right_ans(self):
        self.right_ans = 0


class Quiz:
    def __init__(self, i: int):
        self.b_questions_were = []
        self.i = i
        
    def add_questions(self, question):
        self.b_questions_were.append(question)
    
    def is_uniq_questions(self, question):
        return question in self.b_questions_were

    def minus_i(self):
        self.i -= 1
    
    def plus_i(self):
        self.i += 1

@dataclass
class Question:
    question: str
    answer: str
    options: List[str]

