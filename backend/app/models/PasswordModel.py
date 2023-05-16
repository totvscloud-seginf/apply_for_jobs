from dataclasses import dataclass

@dataclass
class RequestPassword:
    def __init__(self, email, password, max_views, valid_days, use_symbols, use_numbers, use_words, length):
        self.email = email
        self.password = password
        self.max_views  = max_views
        self.valid_days = valid_days 
        self.use_symbols = use_symbols
        self.use_numbers = use_numbers
        self.use_words = use_words
        self.length = length
