def minus(input_1,input_2=10):
    """minus 2 digit and return result"""
    result = input_1-input_2
    if result < 10:
        msg = "ok"
    else:
        msg = "ng"
    return result,msg


def plus(input_1,input_2=10):
    """plus 2 digit and return result"""
    result = input_1+input_2
    if result < 10:
        msg = "ok"
    else:
        msg = "ng"
    return result,msg