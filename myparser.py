from sly import Parser
from mylexer import MyLexer

class BinOp():
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        
class UnOp():
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    

class MyParser(Parser):
    # Get the token list from the lexer (required)
    #
    # "pure Python only" rules simply copies Python's rules.
    #
    tokens = MyLexer.tokens
    debugfile = "parser.out"

    precedence = (
        ('nonassoc', LESSTHAN, GREATERTHAN), # pure Python only
        ('left', PLUS, MINUS),
        ('left', TIMES),
        ('right', UMINUS)
    )
    
    # Grammar rules and actions

    @_('') # empty expr. 왜 필요한지 아직 이해 못함..
    def statement(self, p):
        pass

    # 불필요한 negate를 없애기 위해서 negate(ngetate(ctxt))인 경우를 반드시 찾을 수 있어야 함. 
    # -p.expr은 UMINUS의 'abstract'한 표현일 뿐. 
    # 최종적으로 reduce된 AST는 다음과 같아야 함.
    # >>> arr = [1,2,3]
    # >>> ptxt = Plaintext(arr)
    # >>> -(3*ptxt - 2*ctxt)
    # ---->>>
    # >>> arr = -3 * ([1,2,3])
    # >>> ptxt =  Plaintext(arr)
    # >>> lib.addp(lib.multp(ctxt,-2), ptxt)
    #
    # * Plaintext는 clear text에 -3*을 붙여주지만 
    # (ptxt 만들기 전에 처리하거나, 그 자리에서 decode 가능)
    #   Ciphertext는 -2*를 multp로 하는 수 밖에 없음. 
    @_('MINUS expr %prec UMINUS')  # %prec UMINUS == 'UMINUS'의 precedence를 적용
    def expr(self, p):
        return -p.expr     

    # @_('NAME "=" expr')
    # def var_assign(self, p):
    #     return ('var_assign', p.NAME, p.expr)

    # @_('NAME "=" STRING')
    # def var_assign(self, p):
    #     return ('var_assign', p.NAME, p.STRING)

    @_('expr PLUS term')
    def expr(self, p):
        return BinOp('+', p.expr, p.term)
    #def expr(self, p):
    #    return p.expr + p.term

    @_('expr MINUS term')
    def expr(self, p):
        return p.expr - p.term

    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        return p.term * p.factor

    #@_('term DIVIDE factor')
    #def term(self, p):
    #    return p.term / p.factor

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr
