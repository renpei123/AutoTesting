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
        
class ASCAControlError(MyException):
    def __init__(self, code = 10003, message = 'ASCA Test validate failed', args = ('ASCA Test validate failed',)):
        self.args = args
        self.message = message
        self.code = code

class IWRefreshError(MyException):
    def __init__(self, code = 10003, message = 'IW Refresh Test validate failed', args=('IW Refresh Test validate failed',)):
        self.args = args
        self.message = message
        self.code = code


class RowcountError(MyException):
    def __init__(self, code = 10003, message = 'Rowcount Test validate failed', args=('Rowcount Test validate failed',)):
        self.args = args
        self.message = message
        self.code = code

class SampleDataError(MyException):
    def __init__(self, code = 10003, message = 'Sample Data Test validate failed', args=('Sample Data Test validate failed',)):
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