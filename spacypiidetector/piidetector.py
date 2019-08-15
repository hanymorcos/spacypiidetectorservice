#!/usr/bin/env python
import spacy
from spacy.matcher import Matcher

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
        self.matcher = Matcher(self.nlp.vocab)
        for p in self.patterns:
           for k, v in p.items() : 
              self.matcher.add(k,None,[v])

    def getEntites(self, text):
        doc =self.nlp(str(text, 'utf-8'))
        entities = []
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            entities.append( {"match_id" : match_id, "string_id": string_id, "start": start, "end": end, "text": span.text })

        return entities


def main():
 PiiDetector().getEntites(" 555-55-5555 ")

if __name__ == '__main__':
        main()
