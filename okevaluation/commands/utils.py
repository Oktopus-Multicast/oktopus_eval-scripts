import contextlib, sys

@contextlib.contextmanager
def redirect_stdout(target):
    original = sys.stdout
    try:
        sys.stdout = target
        yield
    finally:
        sys.stdout = original