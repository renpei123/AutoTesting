#/usr/bin
# -*- coding: utf-8 -*-
class MyException(Exception):
 
    def __init__(self, *args):
        self.args = args
        
class JobStreamError(MyException):
    def __init__(self, code = 10001, message = 'The job stream test failed', args = ('job stream test failed',)):
        self.args = args
        self.message = message
        self.code = code
        
        
class loginoutError(MyException):
    def __init__(self):
        self.args = ('退出异常',)
        self.message = '退出异常'
        self.code = 200     
        
if __name__ == "__main__": 
    if (1!=0):
        raise JobStreamError()        