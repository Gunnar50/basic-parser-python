import basic 

while True:
    text = input("basic > ")
    result, error = basic.run(text, file_name="<stdin>")
    
    if error:
        print(error)
    else:
        print(result)
    