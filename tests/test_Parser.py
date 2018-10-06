import glob
import os

import pandas as pd
import pytest

from Parser.parser import SainsburysParser

test_file_folder = os.path.join(os.path.dirname(__file__),
                                'test_csvs')
test_files = glob.glob(os.path.join(test_file_folder, '*.csv'))


def test_load_csv():
    file_path = os.path.join(test_file_folder, '1.csv')
    expected_df = pd.DataFrame(
        {'mon': {0: 1},
         'tue': {0: 5},
         'some_column1': {0: 'data'},
         'wed': {0: 2},
         'thu': {0: 3},
         'fri': {0: 3},
         'description': {0: 'first_desc'}}
    )
    df = SainsburysParser.load_csv(file_path)
    pd.testing.assert_frame_equal(df, expected_df)


def test_lower_case_df_col_names():
    df = pd.DataFrame(columns=["HelLO", "HeySaiNsBurYz"])
    df = SainsburysParser._lower_case_df_col_names(df)
    assert all(df.columns == ["hello", "heysainsburyz"])


@pytest.mark.parametrize(
    "df", [
        pd.DataFrame({'mon-tue': [1], 'wed': [2], 'thu-fri': [3]}),
        pd.DataFrame({'montue': [1], 'wed': [2], 'thu-fri': [3]}),
        pd.DataFrame({'mon-thu': [1], 'fri': [3]}),
        pd.DataFrame({'montuewed': [1], 'thu': [2], 'fri': [3]})
    ])
def test_parse_days_that_the_dates_correctly_parsed(df):
    """Checks that the Columns are correctly made."""
    df = SainsburysParser.parse_df_dates(df)
    weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
    assert all([day in df.columns for day in weekdays])


def test_parse_dates_for_their_values():
    df = pd.DataFrame({'mon-tue': [1], 'wed': [2], 'thu-fri': [3]})
    df = SainsburysParser.parse_df_dates(df)
    pd.testing.assert_frame_equal(
        df,
        pd.DataFrame({'mon': [1], 'tue': [1], 'wed': [2],
                      'thu': [3], 'fri': [3]}),
        check_like=True)  # ignores column order


def test_parse_df_values():
    df = pd.DataFrame({'mon': [3, 4], 'tue': [4, 5], 'wed': [5, 6],
                       'thu': [6, 7], 'fri': [6, 7],
                       'some_column1': ["data", "more data"],
                       'description': ["first_desc", "second_desc"]})
    mod_df = SainsburysParser._parse_df_values(df)
    assert mod_df.loc[0].to_dict() == {
        'day': 'mon',
        'description': 'first_desc 9',
        'square': 9,
        'double': 6,
        'is_square': True,
        'value': 3}

    assert mod_df.loc[3].to_dict() == {
        'day': 'thu',
        'description': 'first_desc 12',
        'square': 36,
        'double': 12,
        'is_square': False,
        'value': 6}


def test_keep_square_or_double():
    output_list = [
        {'day': 'wed',
         'description': 'second_desc 36',
         'square': '36',
         'double': '12',
         'is_square': True,
         'value': 6},
        {'day': 'thu',
         'description': 'second_desc 14',
         'square': '49',
         'double': '14',
         'is_square': False,
         'value': 7}]
    expected_output_list = [
        {'day': 'wed',
         'description': 'second_desc 36',
         'square': '36',
         'value': 6},
        {'day': 'thu',
         'description': 'second_desc 14',
         'double': '14',
         'value': 7}
    ]
    assert SainsburysParser._keep_square_or_double(
        output_list) == expected_output_list
