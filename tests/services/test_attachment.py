from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

import pytest
from memoryfm.models.service_enums import (
    ChartKindColumn,
    Frequency,
)
import memoryfm.services.attachment_service as attserv

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


kind = ChartKindColumn.Track
freq = Frequency.W
username = "lazulinoother"
from_ts, to_ts = None, None


# Scrobbles counts of distinct tracks on different days.
daily_counts = np.array(
    [
        [1, 1, 3],  # Day 0
        [4, 1, 1],  # Day 1
    ]
)
# Scrobble Counts for distinct tracks
# Purposely chosen data with no overlap in days, for simplicity.
track_counts = np.array([1, 1, 3, 4, 1, 1])
# Proportions
props: np.typing.NDArray = track_counts / np.sum(track_counts)
# Renyi Entropy - full history
renyi_entropy_expected = {
    1: -np.sum(props * np.log(props)),
    2: -np.log(np.sum(props**2)),
}
# Attachment Index - full history
att_index_expected = {k: 100 * np.exp(-v) for k, v in renyi_entropy_expected.items()}

# Max total count was on Day 1 --> 6
maxct = np.max(daily_counts.sum(axis=1))
# Total count on Day 0 ---> 5
day_0ct = np.sum(daily_counts[0])
# Day 0 Weight --> log2(1 + 5/6)
weight_0 = np.log1p(day_0ct / maxct) / np.log(2)
# Day 0 proportions
props_0 = np.array(daily_counts[0]) / np.sum(daily_counts[0])
# Day 0 Renyi Entropy
entropy_day_0 = -np.sum(props_0 * np.log(props_0))
# Day 0 Weighted Attachment
wtd_att_index_expected = weight_0 * 100 * np.exp(-entropy_day_0)


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


def test_get_weighted_attachment_index(seeded_db: Session):
    wtd_att_index = attserv.get_weighted_attachment_index_by_username(
        seeded_db,
        username,
        kind,
        from_ts,
        to_ts,
        freq=Frequency.D,
    )
    assert wtd_att_index is not None
    assert len(wtd_att_index) == 2
    assert wtd_att_index[0].get("value") == pytest.approx(wtd_att_index_expected)


def test_get_attachment_moments(seeded_db: Session):
    moments = attserv.get_attachment_moments(
        seeded_db, username, kind, from_ts, to_ts, freq=Frequency.D
    )
    assert moments is not None
    assert len(moments) == 2
    assert moments[1].get("track") == "Anything We Want"
