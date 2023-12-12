def trampoline(func, *args, **kwargs):
    while True:
        result = func(*args, **kwargs)
        try:
            if not result.empty:
                return result
        except:
            pass