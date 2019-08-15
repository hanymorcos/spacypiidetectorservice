#!/usr/bin/env python
import spacy
from spacy.matcher import Matcher
import re

class PiiDetector:
    #https://stackoverflow.com/questions/4087468/ssn-regex-for-123-45-6789-or-xxx-xx-xxxx
    SSN_PATTERN = "^\d{3}[ -]?\d{2}[ -]?\d{4}$"

    #https://daxondata.com/javascript-php-and-regular-expressions-for-international-and-us-phone-number-formats
    PHONE_NUMBER_PATTERN = "\d?(\s?|-?|\+?|\.?)((\(\d{1,4}\))|(\d{1,3})|\s?)(\s?|-?|\.?)((\(\d{1,3}\))|(\d{1,3})|\s?)(\s?|-?|\.?)((\(\d{1,3}\))|(\d{1,3})|\s?)(\s?|-?|\.?)\d{3}(-|\.|\s)\d{4}"
    
    #https://emailregex.com/
    EMAIL_PATTERN = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    #http://www.richardsramblings.com/regex/credit-card-numbers/
    CREDIT_CARD_PATTERN = "^(?:3[47]\d{2}([\s\-]?)\d{6}([\s\-]?)\d|(?:(?:4\d|5[1-5]|65)\d{2}|6011)([\s\-]?)\d{4}([\s\-]?)\d{4}([\s\-]?))\d{4}$"

    patterns = [{"SSN": {"TEXT"   : {"REGEX": SSN_PATTERN}}},
                {"PHONENUMBER": {"TEXT" : {"REGEX": PHONE_NUMBER_PATTERN}}},
                {"EMAILPATTERN": {"TEXT" : {"REGEX": EMAIL_PATTERN}}},
                {"CREDITCARD": {"TEXT" : {"REGEX": CREDIT_CARD_PATTERN}}}
              ]
 
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def getpatterns(self,text):
        entities = []
        nstr = text
        for p in self.patterns:
            for k, v in p:
                regex = re.compile(v)
                offset = 0
                for m in regex.finditer(nstr):
                    start, end = m.span()
                    start = start - offset
                    end = end - offset
                    nstr = nstr[:start] + nstr[end:]
                    offset = end-start
                    entities.append({k:m.match})
        return entities  

    def getEntites(self, text):
        doc =self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append( {"text" : ent.text, "start_char":  ent.start_char, "end_char": ent.end_char, "label": ent.label_})

        print(entities)
        return entities


def main():
 PiiDetector().getEntites(" 555-55-5555 ")

if __name__ == '__main__':
        main()
