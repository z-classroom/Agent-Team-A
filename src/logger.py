import logging
from pathlib import Path

def build_logger(path: str, level: str = "INFO") -> logging.Logger:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("agent")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        fh = logging.FileHandler(path)
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger