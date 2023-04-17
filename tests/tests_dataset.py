import pytest
import pandas as pd
from data_preprocessing import process_steam_data


def test_steam_data():
    # Load the dataset (replace with actual file path)
    steam_data = pd.read_csv('Data/all_data.csv')

    # Process the dataset
    processed_steam_data = process_steam_data(steam_data)

    # Check if the processed dataset has the required columns
    expected_columns = [
        'uid', 'id', 'owned', 'publisher', 'genres', 'app_name', 'title', 'url',
        'release_date', 'tags', 'discount_price', 'reviews_url', 'specs',
        'price', 'early_access', 'developer', 'sentiment', 'metascore'
    ]
    for column in expected_columns:
        assert column in processed_steam_data.columns

    # Check if the processed dataset has no null values in required columns
    required_columns_no_nulls = [
        'uid', 'id', 'owned', 'publisher', 'genres', 'app_name', 'title',
        'release_date', 'tags', 'specs', 'price', 'early_access', 'developer',
        'sentiment'
    ]
    assert processed_steam_data[required_columns_no_nulls].isnull().sum().sum() == 0

    # Check if 'owned' values are either 0 or 1
    assert set(processed_steam_data['owned'].unique()).issubset({0, 1})

if __name__ == "__main__":
    pytest.main([__file__])
