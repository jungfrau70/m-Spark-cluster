import traceback as tb
def test():
#     sal = -1
    try:
        if sal < 0 :
            raise Exception('Salary Can not be Less Than 0.')
    except Exception as Argument:
        print("An Exception Occured. ", Argument)
        raise
    
