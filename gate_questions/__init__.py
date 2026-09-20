"""Unified GATE Question Bank Aggregator and Schema Validator."""

import logging
from typing import Any

from .algorithms import QUESTIONS as ALGO_Q
from .coa import QUESTIONS as COA_Q
from .compiler_design import QUESTIONS as CD_Q
from .computer_networks import QUESTIONS as CN_Q
from .databases import QUESTIONS as DB_Q
from .digital_logic import QUESTIONS as DL_Q
from .discrete_math import QUESTIONS as DM_Q
from .engineering_math import QUESTIONS as EM_Q
from .general_aptitude import QUESTIONS as GA_Q
from .operating_systems import QUESTIONS as OS_Q
from .programming_ds import QUESTIONS as PDS_Q
from .pyqs import PYQS as PYQ_LIST

logger = logging.getLogger(__name__)

_RAW_LISTS = [
    OS_Q,
    PDS_Q,
    COA_Q,
    ALGO_Q,
    DM_Q,
    EM_Q,
    TOC_Q := __import__("gate_questions.toc", fromlist=["QUESTIONS"]).QUESTIONS,
    CD_Q,
    DB_Q,
    CN_Q,
    DL_Q,
    GA_Q,
    PYQ_LIST,
]


def _validate_and_merge() -> list[dict[str, Any]]:
    seen_ids: set[str] = set()
    merged: list[dict[str, Any]] = []

    for sublist in _RAW_LISTS:
        for q in sublist:
            qid = q.get("id")
            if not qid:
                raise ValueError(f"Question missing 'id': {q}")
            if qid in seen_ids:
                logger.warning(f"Duplicate question ID ignored: {qid}")
                continue
            # Validate required fields
            for field in ("subject", "topic", "type", "marks", "q", "answer", "explanation"):
                if field not in q:
                    raise ValueError(f"Question {qid} missing field '{field}'")
            seen_ids.add(qid)
            merged.append(q)

    return merged


ALL_GATE_QUESTIONS: list[dict[str, Any]] = _validate_and_merge()

__all__ = ["ALL_GATE_QUESTIONS"]
