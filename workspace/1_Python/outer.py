import exception_handling as eh
import sys
import traceback as tb

def main():
    try:
        eh.test()

    except:
        ob = sys.exc_info()[2]
        print(ob.tb_lineno)
        print(ob.tb_frame)
        print(ob.tb_next.tb_lineno)
        print(ob.tb_next.tb_frame)

if __name__ == '__main__':
    main()
