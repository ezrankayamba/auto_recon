import threading


def run_in_background(fn, args=None):
    x = threading.Thread(target=fn, args=args if args else ())
    x.start()
