import time


def time_left(timestamp):
    """Convert a timestamp into how long to wait for it."""
    if timestamp is None:
        return None
    return max(0.0, timestamp - time.time())


def timed_out(timestamp):
    """Check if a timestamp has been reached."""
    if timestamp is None:
        return False
    return timestamp < time.time()


def make_timeout(delay_seconds):
    """Convert a delay (in seconds) into a timestamp."""
    if delay_seconds is None:
        return None
    return time.time() + delay_seconds
