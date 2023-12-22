import re

class Validations:
    def email(self, email):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if(re.fullmatch(regex, email)):
            return True
        return False
        
    
