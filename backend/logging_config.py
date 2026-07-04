"""
Storyboard AI — Verbose Trace Logging Configuration.

Writes structured logs to /logs with automatic daily rotation.
All significant system events — API calls, scene analysis, image generation,
format detection, knowledge base activity, governance events — are traced here.
"""
import logging
import logging.handlers
import os
import sys
from pathlib import Path

# ── Path resolution ──────────────────────────────────────────────────────────
_BACKEND_DIR = Path(__file__).parent
_PROJECT_ROOT = _BACKEND_DIR.parent
LOGS_DIR = _PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# ── Log format ───────────────────────────────────────────────────────────────
TRACE_FORMAT = (
    "%(asctime)s.%(msecs)03d | %(levelname)-8s | %(name)-28s | "
    "%(filename)s:%(lineno)d | %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ── Custom TRACE level (below DEBUG) ─────────────────────────────────────────
TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")


def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kwargs)


logging.Logger.trace = trace  # type: ignore[attr-defined]


def configure_logging(app_name: str = "storyboard") -> logging.Logger:
    """
    Configure the global logging system.

    Outputs:
    - Console: INFO and above (coloured where supported)
    - logs/storyboard.log: DEBUG and above, daily rotation (7 days)
    - logs/trace.log: TRACE and above, rotation at 10 MB (5 backups)
    - logs/governance.log: dedicated governance audit stream
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(TRACE_LEVEL)

    formatter = logging.Formatter(TRACE_FORMAT, datefmt=DATE_FORMAT)

    # ── Console handler ───────────────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # ── Main application log (daily rotation) ────────────────────────────────
    app_log_path = LOGS_DIR / f"{app_name}.log"
    app_handler = logging.handlers.TimedRotatingFileHandler(
        app_log_path, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(formatter)
    root_logger.addHandler(app_handler)

    # ── Verbose trace log (size rotation) ────────────────────────────────────
    trace_log_path = LOGS_DIR / f"{app_name}_trace.log"
    trace_handler = logging.handlers.RotatingFileHandler(
        trace_log_path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    trace_handler.setLevel(TRACE_LEVEL)
    trace_handler.setFormatter(formatter)
    root_logger.addHandler(trace_handler)

    # ── Governance audit log (append-only, never rotated) ────────────────────
    gov_log_path = LOGS_DIR / "governance_audit.log"
    gov_handler = logging.FileHandler(gov_log_path, mode="a", encoding="utf-8")
    gov_handler.setLevel(logging.DEBUG)
    gov_handler.setFormatter(formatter)
    gov_logger = logging.getLogger("governance")
    gov_logger.addHandler(gov_handler)
    gov_logger.propagate = True

    # ── Knowledge base log ───────────────────────────────────────────────────
    kb_log_path = LOGS_DIR / "knowledge_base.log"
    kb_handler = logging.handlers.RotatingFileHandler(
        kb_log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    kb_handler.setLevel(logging.DEBUG)
    kb_handler.setFormatter(formatter)
    kb_logger = logging.getLogger("knowledge_base")
    kb_logger.addHandler(kb_handler)
    kb_logger.propagate = True

    root_logger.info(f"Logging system initialized. Log directory: {LOGS_DIR}")
    return logging.getLogger(app_name)
