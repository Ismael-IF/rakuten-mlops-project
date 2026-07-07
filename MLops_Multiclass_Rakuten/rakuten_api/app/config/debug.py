# -*- coding: utf-8 -*-

DEBUG = True


def log(module, func,  message, variable=None ):
    
    if DEBUG:
        print ('\n***************************************************************************************************************')
        print ('[DEBUG]==>', 'Module :','[', module,'],', 'Function :', '[', func, '],',  'message :', '[', message ,']' )
        if variable is not None:
         print ('[DEBUG]==> variable :', '[', variable ,']' )     
        print ('***************************************************************************************************************\n')
            
