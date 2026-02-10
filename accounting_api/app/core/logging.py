from __future__ import annotations

import logging
import sys


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(levelname)s:%(name)s:%(message)s",
    )
