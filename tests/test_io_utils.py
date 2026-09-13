import math
import pytest

from electricity_analyse.io_utils import (
    parse_float,
    read_daily_generation_df
)


@pytest.mark.parametrize(("raw_value", "expected"), [ ("1,234", 1234.0), (" 500 ", 500.0), ("12.5", 12.5), ("-42", -42.0)])
def test_parse_float(raw_value, expected):
    assert parse_float(raw_value) == pytest.approx(expected)


def test_parse_float_empty_string_returns_nan():
    result = parse_float("")
    assert math.isnan(result)


def test_read_daily_generation_df_removes_thousands_separator(tmp_path):
    csv_path = tmp_path / "daily.csv"
    csv_path.write_text(("Date;Generation\n" '2025-01-01;"1,234"\n' '2025-01-02;"2,345"\n'), encoding="utf-8")
    result = read_daily_generation_df(csv_path)
    assert result["Generation"].tolist() == ["1234", "2345",]


def test_read_daily_generation_df_missing_file(tmp_path):
    missing_path = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError):
        read_daily_generation_df(missing_path)
