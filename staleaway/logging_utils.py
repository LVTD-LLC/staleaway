import logfire


def scrubbing_callback(m: logfire.ScrubMatch):
    # Returning None retains Logfire's default scrubbing, including cookies.
    # Never opt authentication or analytics cookies out of that protection.
    return None
