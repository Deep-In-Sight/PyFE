from sly import Parser 
from my_lexer import MyLexer

class MyParser(Parser):
    tokens = MyLexer.tokens

    # Un-comment the following line to output the parser logs for debugging any conflicts
    # debugfile = 'parser.out'

    # This sets the order of execution. The last values will have a higher precedence
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES),#, DIVIDE),
        ('right', UMINUS),
        )

    def __init__(self):
        self.stack = list() 
        self.names = { }

    @property
    def last_item_on_stack(self):
        return self.stack[-1] if len(self.stack) > 0 else None

    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    # @_('expr DIVIDE expr')
    # def expr(self, p):
    #     return p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f'Undefined name {p.NAME!r}')
            return 0