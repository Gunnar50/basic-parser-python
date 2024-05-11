import constants
import nodes
import _tokens
import typing

# PARSER

class Parser:
    def __init__(self, tokens: typing.List["_tokens.Token"]):
        self.tokens = tokens
        self.token_index = 1
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

    def factor(self) -> "nodes.NumberNode":
        token = self.current_token
        
        if token.token_type in (constants.TOKEN_TYPE_INT, constants.TOKEN_TYPE_FLOAT):
            self.advance()
            return nodes.NumberNode(token)

    def term(self) -> "nodes.BinaryOperationNode":
        return self.binary_operation(self.factor, (constants.TOKEN_TYPE_DIV, constants.TOKEN_TYPE_MUL))
       
    def expression(self) -> "nodes.BinaryOperationNode":
        return self.binary_operation(self.term, (constants.TOKEN_TYPE_PLUS, constants.TOKEN_TYPE_MINUS))
    
    def binary_operation(self,
                         func: typing.Callable[[], typing.Union['nodes.NumberNode', 'nodes.BinaryOperationNode']],
                         operation_tokens: typing.List[str]) -> "nodes.BinaryOperationNode":
        left: "nodes.NumberNode" | "nodes.BinaryOperationNode" = func()
        
        while self.current_token in operation_tokens:
            operation_token: None | "_tokens.Token" = self.current_token
            right: "nodes.NumberNode" = func()
            left = nodes.BinaryOperationNode(left, operation_token, right)
        
        return left