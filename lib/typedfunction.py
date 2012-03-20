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

def argtypes(*args_argtypes, **kwargs_argtypes):

    def wrap(f):

        def call(*args, **kwargs):
            for i in range(min(len(args_argtypes), len(args))):
                typecheck(args[i], args_argtypes[i])

            for k in [k for k in kwargs_argtypes if k in kwargs]:
                typecheck(kwargs[k], kwargs_argtypes[k])

            return f(*args, **kwargs)

        setattr(call, '__arg_argtypes__', args_argtypes)
        setattr(call, '__kwarg_argtypes__', kwargs_argtypes)

        return call
    return wrap

def rettypes(*ret_types):

    def wrap(f):

        def call(*args, **kwargs):
            i = f(*args, **kwargs)
            if(isinstance(i, tuple)):
                t = tuple(map(type, args))
                if(t in ret_types) or (t == ret_types):
                    return i
                else:
                    raise TypeError("Return type does not match")
            else:
                raise TypeError("Return type does not match")

        setattr(call, '__ret_types__', ret_types)

        return call
    return wrap

if __name__ == "__main__":

    @argtypes(int)
    @rettypes(int)
    def f(x):
        return x + 1
    print(f(1))
    print(f('1'))

    @argtypes([int, list])
    @rettypes(None)
    def j(k):
        if isinstance(k, int):
            print("~" * k)
        else:
            print(k)

    @argtypes(None)
    @rettypes(int)
    def retfail():
        return "FALZORZ"

    retfail()

    j(9)
    j([9000, 9001])
    j({1: 2, 2: 3, 3: 4})
