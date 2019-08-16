#!/usr/bin/env python
import spacy
from spacy import tokens
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

    patterns = [{"CREDITCARD":CREDIT_CARD_PATTERN}, { "SSN": SSN_PATTERN}, {"PHONE" : PHONE_NUMBER_PATTERN}, { "EMAIL": EMAIL_PATTERN} ]
 
    class Spacy_Entity:
        def __init__(self,entity):
            self.entity = entity

        def toPacket(self):
            return {"text" : self.entity.text, "start":  self.entity.start_char, "end": self.entity.end_char, "label": self.entity.label_}
    
    class RE_Entity:
        def __init__(self,entity, type):
            self.entity = entity
            self.type = type

        def toPacket(self):
            start, end = self.entity.span()
            return {"text" : self.entity.match, "start":  start, "end": end, "label": self.entity.type}


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
                    entities.append(self.RE_Entity(m, k).toPacket())
        return entities  

    def getEntites(self, text):
        doc =self.nlp(text)
        entities = []
        for ent in doc.ents:
            if (ent.label_ == "PERSON"):
                entities.append(self.Spacy_Entity(ent).toPacket())
        return entities


def main():
 print( PiiDetector().getEntites("WASHINGTON -- In 444-22-3333 the wake of a string of abuses by New York police officers in the 1990s, " +
 "Loretta E. Lynch, the top federal (233) 423-2323 prosecutor in Brooklyn, spoke forcefully about the pain" + 
 "of a broken trust that 4444-4444-4444-4444 African-Americans test.tst@test.com  4555-4444-4444-4444felt and said the responsibility for repairing " +
 "generations of miscommunication and mistrust fell to law enforcement."))

if __name__ == '__main__':
        main()
