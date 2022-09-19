from sly import Lexer 
from dataclasses import dataclass

"""
dataclass는 sly랑 상관 없음. 
요걸 어떻게 활용했을까?
https://gist.github.com/hadware/5dc39e407b78900a1f9e71b52ebf3a36
"""

@dataclass
class CTXT:
    name: str
    nlosts: int
    scale: float
    modind: int

    def __repr__(self):
        return "CTXT({name})\n{scale}\n{modind}\n".format(
            name=self.name,
            scale=self.scale,
            modind=self.modind)

@dataclass
class PTXT:
    name: str
    nlosts: int
    scale: float

    def __repr__(self):
        return "CTXT({name})\n{scale}\n".format(
            name=self.name,
            scale=self.scale)


class MyLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { ID, NUMBER, PLUS, MINUS, TIMES, #DIVIDE, 
              ASSIGN, LPAREN, RPAREN,
              IF, ELSE, WHILE,
              CTXT, PTXT, 
              RESCALE, MODSW, BOOTSTRAP  # 동형암호 special function
             }

    # String containing ignored characters between tokens
    ignore = ' \t'
    
    # Other ignored patterns
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'    

    # Regular expression rules for tokens
    ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER  = r'\d+'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    #DIVIDE  = r'/'
    ASSIGN  = r'='
    LPAREN  = r'\('
    RPAREN  = r'\)'

    # Special cases
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['rescale'] = RESCALE
    ID['MODSW'] = MODSW
    ID['BOOTSTRAP'] = BOOTSTRAP
   
    
    def __init__(self):
        self.lineno = 0
        self

    @_(r"(0|[1-9][0-9]*)")
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    # Define a rule so we can track line numbers
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # RESCALE 동작 정의 
    
    
    # Compute column.
    #     input is the input text string
    #     token is a token instance
    def find_column(text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column    
    