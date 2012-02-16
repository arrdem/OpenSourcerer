#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   TypedFunction.py

def typecheck(instance, t):
    if isinstance(t, list):
        if not type(instance) in t:
            raise TypeError("Argument type %s not in the permitted types list" % (type(instance)))
    else:
        if not isinstance(instance, t):
            raise TypeError("Argument was of type %s, not type %s" % (type(instance), t))

def types(*args_types, **kwargs_types):
    def wrap(f):
        def call(*args, **kwargs):
            for i in range(min(len(args_types), len(args))):
                typecheck(args[i], args_types[i])

            for k in [k for k in kwargs_types if k in kwargs]:
                typecheck(kwargs[k], kwargs_types[k])

            return f(*args, **kwargs)

        setattr(call, '__arg_types__', args_types)
        setattr(call, '__kwarg_types__', kwargs_types)

        return call
    return wrap

if __name__ == "__main__" or 1:
    @types(int)
    def f(x):
        return x+1
    print f(1)
    #print f('1')

    @types([int, list])
    def j(k):
        if isinstance(k, int):
            print "~"*k
        else:
            print k

    j(9)
    j([9000, 9001])
    j({1:2, 2:3, 3:4})
