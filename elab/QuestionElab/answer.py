import json
class Answer: 
    def __init__(self, language, condition, element, input, output, answer): # data members (instance variables) 
        self.language = language
        self.condition = condition
        self.element = element
        self.input = input
        self.output = output
        self.answer = answer

    # def show(self):
    #     print(json.dumps(self))