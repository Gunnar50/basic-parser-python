import typing
import _tokens
import _parser
import _lexer

# RUN
def run(text: str, file_name: str):
    # Generate tokens    
    lexer = _lexer.Lexer(text, file_name)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    
    # Generate AST
    parser = _parser.Parser(tokens)
    ast = parser.parse()

    return ast, None

if __name__ == '__main__':
    while True:
        text = input("basic > ")
        result, error = run(text, file_name="<stdin>")
        
        if error:
            print(error)
        else:
            print(result)
    
