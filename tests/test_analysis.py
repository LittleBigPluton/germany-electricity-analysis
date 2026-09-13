import pandas as pd
import pytest

from electricity_analyse.analysis import (
    add_daily_consumption_from_hourly,
    add_daily_totals,
    comparison_days,
    compute_stats_table,
    create_monthly_summary,
    set_date_index
)
from electricity_analyse.config import (
    ALL_DAILY_CATEGORIES,
    ENERGY_TYPES_RENEWABLE,
    MWH_SUFFIX
)


def make_daily_generation_frame() -> pd.DataFrame:
    data = {"Date": ["2025-01-02", "2025-01-01"],}

    for category in ALL_DAILY_CATEGORIES:
        column = f"{category}{MWH_SUFFIX}"
        if category in ENERGY_TYPES_RENEWABLE:
            data[column] = ["10", "20"]
        else:
            data[column] = ["5", "10"]

    return pd.DataFrame(data)


def test_add_daily_totals():
    df = make_daily_generation_frame()
    result = add_daily_totals(df)
    renewable_count = len(ENERGY_TYPES_RENEWABLE)
    conventional_count = (len(ALL_DAILY_CATEGORIES) - renewable_count)
    expected_renewable = [renewable_count * 10, renewable_count * 20]
    expected_conventional = [conventional_count * 5, conventional_count * 10]
    assert result["Total Renewable"].tolist() == expected_renewable
    assert result["Total Conventional"].tolist() == expected_conventional
    expected_production = [expected_renewable[0] + expected_conventional[0], expected_renewable[1] + expected_conventional[1]]
    assert result["Total Production"].tolist() == expected_production

    # Function should not mutate the input dataframe.
    assert "Total Renewable" not in df.columns
    assert "Total Conventional" not in df.columns
    assert "Total Production" not in df.columns


def test_set_date_index_sorts_dates_and_preserves_input():
    df = pd.DataFrame({"Date": ["2025-01-03", "2025-01-01", "2025-01-02"], "value": [30, 10, 20]})
    result = set_date_index(df, "Date")
    expected_index = pd.DatetimeIndex(["2025-01-01", "2025-01-02", "2025-01-03"], name="Date")
    pd.testing.assert_index_equal(result.index, expected_index)
    assert result["value"].tolist() == [10, 20, 30]
    assert "Date" in df.columns
    assert not isinstance(df.index, pd.DatetimeIndex)


def test_set_date_index_rejects_invalid_date():
    df = pd.DataFrame({"Date": ["2025-01-01", "not-a-date"], "value": [1, 2]})
    with pytest.raises(ValueError, match="Failed to parse"):
        set_date_index(df, "Date")


def test_add_daily_consumption_from_hourly():
    daily_index = pd.date_range("2025-01-01", periods=2, freq="D", name="Date")
    df_daily = pd.DataFrame(index=daily_index, data={"Total Production": [100.0, 200.0]})
    df_hourly = pd.DataFrame({"Date": ["2025-01-01 00:00", "2025-01-01 01:00", "2025-01-02 00:00", "2025-01-02 01:00"],
                              "Consumption": ["10", "20", "30", "40"]})

    result = add_daily_consumption_from_hourly(df_daily_indexed=df_daily,
                                               df_hourly_consumption=df_hourly,
                                               hourly_date_col="Date",
                                               hourly_value_col="Consumption")
    assert result["Total Consumption"].tolist() == [30.0, 70.0]

    # Input should not be modified.
    assert "Total Consumption" not in df_daily.columns


def test_comparison_days_returns_only_matching_dates():
    df = pd.DataFrame({"production": [120.0, 80.0, 150.0], "consumption": [100.0, 100.0, 140.0]},
                      index=pd.date_range("2025-01-01", periods=3, freq="D"))

    result = comparison_days(df, "production", "consumption")
    assert result == ["2025-01-01", "2025-01-03"]


def test_compute_stats_table():
    df = pd.DataFrame({"wind": [10.0, 20.0, 30.0], "Total Renewable": [20.0, 40.0, 60.0]})
    result = compute_stats_table(df, category_columns=["wind"], extra_columns=["Total Renewable"])
    assert result.loc["wind", "mean"] == pytest.approx(20.0)
    assert result.loc["wind", "std"] == pytest.approx(10.0)
    assert result.loc["wind", "cv_percent"] == pytest.approx(50.0)
    assert result.loc["Total Renewable", "mean"] == pytest.approx(40.0)


def test_create_monthly_summary():
    df = pd.DataFrame({"Date": ["2025-01-01", "2025-01-02", "2025-02-01"],
                       "Total Production": [100.0, 200.0, 200.0],
                       "Total Consumption": [90.0, 180.0, 220.0],
                       "Total Renewable": [50.0, 100.0, 120.0],
                       "Total Conventional": [50.0, 100.0, 80.0],
                       "Renewable Share": [50.0, 50.0, 60.0],
                       "Residual Load": [40.0, 80.0, 100.0]})

    result = create_monthly_summary(df)
    assert result["Month"].tolist() == ["2025-01", "2025-02"]

    january = result.iloc[0]
    assert january["Total Production [MWh]"] == pytest.approx(300.0)
    assert january["Total Consumption [MWh]"] == pytest.approx(270.0)
    assert january["Net Balance [MWh]"] == pytest.approx(30.0)
    assert january["Total Renewable [MWh]"] == pytest.approx(150.0)
    assert january["Renewable Share [%]"] == pytest.approx(50.0)
    assert january["Residual Load [MWh]"] == pytest.approx(120.0)
