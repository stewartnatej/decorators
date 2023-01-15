from functools import wraps


# basic try/except which allows processing to continue
# used like @try_except
def try_except(func):
    @wraps(func)  # keeps the metadata from the decorated function
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"!! Failure on {f.__name__} function with args: {args}")
            print(f"\tException type: {type(e).__name__}. Message: {e}")
    return wrapper


# try/except, allowing specific types of exceptions
# used like @try_except(FileNotFoundError, ValueError)
def try_except(*exception_types):
    def my_decorator(f):
        @wraps(f)  # keeps the metadata from the decorated function
        def wrapper(*args, **kwargs):
            try:
                f(*args, **kwargs)
                return True
            except exception_types as e:
                if isinstance(e, exception_types):
                    print(f"!! Failure on {f.__name__} function with args: {args}")
                    print(f"\tException type: {type(e).__name__}. Message: {e}")
                return False

        return wrapper
    return my_decorator
    
    
def try_except(attempts=1, reset=None):
    """
    decorator which allows processing to continue if the decorated function throws an exception.
    includes options to retry multiple times, and use a reset/validation function.
    motivation was random failures with ArcGIS API for Python. the same failure message was received
    before and after executing a function. retrying was not desired if the function actually succeeded

    attempts:
    parameter is an integer. this gives you the option to run the function multiple times.
    this is useful if you want to change the parameters,
    or if the function randomly fails for unknown reasons and may succeed with the same parameters

    reset:
    parameter is a function, with no parenthesis.
    this is useful if you want to retry, but need to do some cleanup first.
    decorator logic could be expanded to perform validation before the retry.
    recommendation: your_reset_func should be defined in the same scope as the function you are decorating

    using the decorator:                                                                \n
    one try/except, and no reset/validation: @try_except() or @try_except(1)            \n
    three try/except, and no reset/validation: @try_except(3)                           \n
    one try/except, plus reset/validation: @try_except(1, your_reset_func)              \n
    three try/except, plus reset/validation: @try_except(3, your_reset_func)
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            """inner function is required for making multiple attempts"""
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)

                # handle the exception
                except Exception as e:
                    print(f"!! Failure on {func.__name__} function attempt #{i + 1}")
                    print(f"\tArgs: {args}")
                    print(f"\tException type: {type(e).__name__}. Message: {e}")

                    # optional function that will run before the next attempt
                    if reset:
                        reset(*args)

            # if this point is reached, the desired function never succeeded
            print('\tNo further attempts')

        return inner
    return wrapper
