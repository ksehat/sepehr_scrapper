def trampoline(func, *args, **kwargs):
    while True:
        result = func(*args, **kwargs)
        try:
            if result[0]:
                if result[1].empty:
                    return 'There are no flights at this date.'
                else:
                    return result[1]
        except:
            pass