from __future__ import annotations
from typing import TYPE_CHECKING
from math import exp, log

import pytest
from memoryfm.models.service_enums import (
    ChartKindColumn,
    Frequency,
)
import memoryfm.services.attachment_service as attserv

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


kind = ChartKindColumn.Album
freq = Frequency.W
username = "lazulinoother"
from_ts, to_ts = None, None

renyi_entropy_expected = {1: -(5 * log(5 / 6) + log(1 / 6)) / 6, 2: -log(26 / 36)}
att_index_expected = {k: 100 * exp(-v) for k, v in renyi_entropy_expected.items()}


def test_get_renyi_entropy(seeded_db: Session):
    for alpha, value in renyi_entropy_expected.items():
        entropy = attserv.get_renyi_entropy_by_username(
            seeded_db, username, kind, from_ts, to_ts, freq, alpha
        )
        assert entropy is not None
        assert len(entropy) == 1
        assert entropy[0]["value"] == pytest.approx(value, rel=pow(10, -10))


def test_get_attachment_index(seeded_db: Session):
    for alpha, value in att_index_expected.items():
        att_index = attserv.get_attachment_index_by_username(
            seeded_db, username, kind, from_ts, to_ts, freq, alpha
        )
        assert att_index is not None
        assert len(att_index) == 1
        assert att_index[0].get("value") == pytest.approx(value, rel=pow(10, -8))
