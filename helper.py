def helpermethod(method):
    def dec_meth(*args, **kwargs):
        print(method)
        return method(*args, **kwargs)
    return dec_meth


