import structlog


def get_staleaway_logger(name):
    """This will add a `staleaway` prefix to logger for easy configuration."""

    return structlog.get_logger(
        f"staleaway.{name}",
        project="staleaway"
    )
