import pytest

from electricity_analyse.stats_utils import (
    mean,
    stddev_sample,
    summarize
)


def test_mean():
    result = mean([1.0, 2.0, 3.0, 4.0])
    assert result == pytest.approx(2.5)


def test_mean_empty_values_raises():
    with pytest.raises(ValueError, match="requires at least one value",):
        mean([])


def test_sample_standard_deviation():
    result = stddev_sample([1.0, 2.0, 3.0])
    assert result == pytest.approx(1.0)


def test_sample_standard_deviation_requires_two_values():
    with pytest.raises(ValueError, match="requires at least two values",):
        stddev_sample([1.0])


def test_summarize():
    mean_value, std_value = summarize([1.0, 2.0, 3.0])
    assert mean_value == pytest.approx(2.0)
    assert std_value == pytest.approx(1.0)
