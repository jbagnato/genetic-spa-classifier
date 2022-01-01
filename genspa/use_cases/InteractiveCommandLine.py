# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import importlib

import json

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from PyInquirer import Validator, ValidationError


style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})



class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

class InteractiveCommandLine:

    def create(self, answers:dict, filename:str='data'):
        data = { 
            "name": filename,
            "sources" :
                {"D": {
                        "name":answers["SourceName"],
                        "class" : "D",
                        "transformationQuery": answers["source_tr"],
                        "path" : answers["sourcepath"],
                        "directory": answers["sourcedir"],
                        "format" : answers["sourceformat"]
                        }
            },
            "pk": [answers["pk"]],
            "TR": [{"class":x, "params":self.paramForTransformation(x, answers.get(x,''))} for x in answers["transformationObject"]],
            "DQ": [{'class':x} for x in answers["dataQuality"]],
            "target":{
                "path" : answers["targetpath"],
                "directory": answers["targetdir"],
                "format" : answers["targetformat"]
                }
            }
        with open(filename + '.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def paramForTransformation(self, trName:str, trCustomValue:str)->str:
        my_module = importlib.import_module("ingesta.data_access.sidetransformation")
        TrClass = getattr(my_module, trName)
        instance = TrClass(None, {'class':trName})
        aMap = instance.paramsMap()
        fkey = list(aMap.keys())[0]
        aMap[fkey]=trCustomValue
        return aMap

    def run(self,filename:str='data'):
        print('Hi, Lets create a new Q.')

        questions = [
            {
                'type': 'list',
                'name': 'entity',
                'message': 'What do You need?',
                'choices': ['A', 'B'],
                'filter': lambda val: val.lower()
            },
            {
                'type': 'input',
                'name': 'SourceName',
                'message': 'Whay is the name?',
                'default': 'Jhon'
            },
            {
        'type': 'checkbox',
        'qmark': '😃',
        'message': 'Select TR',
        'name': 'transformationObject',
        'choices': [ 
            Separator('= Transformations ='),
            {
                'name': 'A'
            },
            {
                'name': 'B'
            },
            {
                'name': 'C'
            },
            {
                'name': 'D'
            },
            Separator('= TOPIC 2 ='),
            {
                'name': 'E'
            },
            {
                'name': 'F'
            },
            Separator('= Special ='),
            {
                'name': 'G','checked': True
            },
            {
                'name': 'H','checked': True
            }
        ],
        'validate': lambda answer: 'You must choose at least one TR.' if len(answer) == 0 else True
    },
                {
                'type': 'confirm',
                'name': 'toBeSaved',
                'message': 'Finish!, Save Json File?',
                'default': True
            }
        ]

        answers = prompt(questions, style=style)
        print('Chosen:')
        pprint(answers)
        if answers['toBeSaved']:
            self.create(answers, filename)

