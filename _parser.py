import _nodes
import _tokens
import typing

# PARSER

class Parser:
    def __init__(self, tokens: typing.List["_tokens.Token"]):
        self.tokens = tokens
        self.token_index = -1
        self.current_token: typing.Optional["_tokens.Token"] = None
        self.advance()

    def advance(self) -> typing.Optional["_tokens.Token"]:
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token
    
    def parse(self):
        result = self.expression()
        return result

    def factor(self) -> "_nodes.NumberNode":
        token = self.current_token
        
        if token._type in (_tokens.TokenType.INT, _tokens.TokenType.FLOAT):
            self.advance()
            return _nodes.NumberNode(token)

    def term(self) -> "_nodes.BinaryOperationNode":
        return self.binary_operation(self.factor, (_tokens.TokenType.DIV, _tokens.TokenType.MUL))
       
    def expression(self) -> "_nodes.BinaryOperationNode":
        return self.binary_operation(self.term, (_tokens.TokenType.PLUS, _tokens.TokenType.MINUS))
    
    def binary_operation(self,
                         func: typing.Callable[[], typing.Union['_nodes.NumberNode', '_nodes.BinaryOperationNode']],
                         operation_tokens: typing.List[str]) -> "_nodes.BinaryOperationNode":
        left: "_nodes.NumberNode" | "_nodes.BinaryOperationNode" = func()
        
        while self.current_token._type in operation_tokens:
            operation_token: None | "_tokens.Token" = self.current_token
            self.advance()
            right: "_nodes.NumberNode" = func()
            left = _nodes.BinaryOperationNode(left, operation_token, right)
        
        return left