# python -B .
# ----------------------------------------------------------
import sys
# import os
# sys.path.append(os.getcwd())
# list(map(lambda x:print(x), sys.path))
print('')
for pathItem in sys.path:
    print(pathItem)
print('')

import sys
print(['sys.dont_write_bytecode before',sys.dont_write_bytecode,])
sys.dont_write_bytecode = True
print(['sys.dont_write_bytecode after',sys.dont_write_bytecode,])
# ----------------------------------------------------------

import src.example
