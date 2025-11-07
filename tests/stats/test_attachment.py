from __future__ import annotations
import pytest
from pathlib import Path
import numpy as np

from memoryfm.stats.attachment import (
    renyi_entropy,
    attachment_index_counts,
    attachment_index_list,
    attachment,
    weighted_attachment,
    # hill_number_counts,
    # hillnumber,
)
import memoryfm as mfm


json_file = Path(__file__).resolve().parent.parent / "data/json/canonical_json.json"
sclog = mfm.ScrobbleLog.from_json(json_file)


class TestRenyiEntropy:
    def test_renyi_entropy(self):
        counts = [10, 10, 10]
        assert renyi_entropy(counts) == pytest.approx(np.log10(3))


class TestAttachment:
    def test_attachment_index_counts(self):
        counts = []
        assert np.isnan(attachment_index_counts(counts, 2))

    def test_attachment_index_list(self):
        sample = [1, 2, 1, 3, 2, 3]
        assert attachment_index_list(sample) == pytest.approx(
            100 * np.exp(-np.log10(3))
        )

    def test_attachment_index_list_empty(self):
        sample = []
        assert np.isnan(attachment_index_list(sample))

    def test_attachment(self):
        assert attachment(sclog, by="album", freq="7D").iloc[0] == pytest.approx(
            attachment_index_counts([5, 1])
        )

    def test_weighted_attachment(self):
        assert weighted_attachment(sclog, freq="D").iloc[1] == pytest.approx(
            100 * np.log2(1.25)
        )
