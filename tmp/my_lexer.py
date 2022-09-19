from sly import Lexer

class MyLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, STRING, NAME,
            LESSTHAN, GREATERTHAN,
             LPAREN, RPAREN, ASSIGN}
    ignore = ' \t'
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'
    
    literals = {'.', '!'} # lietrals are not processed and returned 'as is'
    
    # The definition of each token in a regex pattern
    # Longer tokens needd to be defined "before" shorter ones.
    #EQUALITY = r'(===|==)'
    #INEQUALITY = r'(!==|!=)'
    #BIGGER = r'(>=|>)'
    #SMALLER = r'(<=|<)'
    LPAREN = r'\('
    RPAREN = r'\)'
    PLUS = r'\+'
    MINUS = r'\-'
    TIMES = r'\*'
    ASSIGN = r'\='
    #DIVIDE = r'\/'
    #OR = r'\|\|'
    #AND = r'\&\&'
    

    # This decorator allows us to add a logic before returning the matched token.
    @_(r"(0|[1-9][0-9]*)")
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t
    
    # Notice Identifier comes after string because most words in a string would be matched with the identifier pattern
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text    


    