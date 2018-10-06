import os
from pprint import pprint
from collections import OrderedDict

import pandas as pd


class SainsburysParser:
    weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']

    def __init__(self, csv_file_path):
        """:param csv_file_path:  "file/path/to/xxx.csv" """
        self.df = self.load_csv(csv_file_path)
        self.output_list = self.process_output(self.df)
        self.display(csv_file_path, self.output_list)

    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """Loads the csv file
        :param file_path: "path/to/file/xxx.csv"
        :return: DataFrame
        """
        return pd.read_csv(file_path)

    @staticmethod
    def _lower_case_df_col_names(df):
        """Converts all column names to lower case"""
        df.columns = [i.lower() for i in df.columns]
        return df

    @classmethod
    def parse_df_dates(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Converts columns with multiple days e.g.
        "mon-wed" -> mon | tue | wed """
        for col in df.columns:
            is_day_in_cols_dict = OrderedDict(
                (day, (day in col)) for day in cls.weekdays)
            if sum(is_day_in_cols_dict.values()) > 1:
                first_day_posn_in_dict = list(is_day_in_cols_dict.values()).index(True)
                last_day_posn_in_dict = len(is_day_in_cols_dict) - list(
                    is_day_in_cols_dict.values())[::-1].index(True)
                first_last_day_slice = slice(first_day_posn_in_dict, last_day_posn_in_dict)
                indiv_days = cls.weekdays[first_last_day_slice]

                for day in indiv_days:
                    df[day] = df[col]
                df = df.drop(col, axis=1)
        return df

    @classmethod
    def _parse_df_values(cls, df: pd.DataFrame) -> pd.DataFrame:
        """ Pre-processes the format for the final output:
        Returns a df with the following columns:
        day: Mon to Fri
        description: Description
        square: Value ** 2
        double: Value * 2
        is_square: whether a square or double should be used
        value: The Value
        """
        days = [day for day in cls.weekdays if day in df.columns]
        stacked_days_df = df[days].stack().reset_index()
        stacked_days_df.rename(columns={'level_0': 'index',
                                        'level_1': 'day',
                                        0: 'value'}, inplace=True)
        df_without_days = df[[i for i in df.columns if i not in cls.weekdays]].reset_index()
        mod_df = pd.merge(df_without_days, stacked_days_df, on='index')

        mod_df['square'] = mod_df['value'] ** 2
        mod_df['double'] = mod_df['value'] * 2
        mod_df['description_number'] = None
        mod_df['is_square'] = mod_df['day'].isin(['mon', 'tue', 'wed'])

        square_mask = mod_df['is_square']
        mod_df.loc[square_mask, 'description_number'] = mod_df['square']
        mod_df.loc[~square_mask, 'description_number'] = mod_df['double']
        mod_df['description'] = mod_df['description'] + ' ' + mod_df['description_number'].astype(str)

        mod_df = mod_df[['day', 'description', 'square', 'double', 'is_square', 'value']]
        return mod_df

    @staticmethod
    def _keep_square_or_double(output_list):
        for row in output_list:
            if row['is_square']:
                del row['double']
            else:
                del row['square']
            del row['is_square']
        return output_list

    @classmethod
    def process_output(cls, df: pd.DataFrame) -> list:
        """Creates a dictionary of the desired standards"""
        df = cls._lower_case_df_col_names(df)
        df = cls.parse_df_dates(df)
        df = cls._parse_df_values(df)
        output_list = df.to_dict('records')
        output_list = cls._keep_square_or_double(output_list)
        return output_list

    @staticmethod
    def display(file_path, output_list):
        """:param file_path: Full "path/to/file/xxx.csv"
        :param output_list: [{'day': 'mon', ..., 'value': 10}]
        Prints the file path, then the output list
        """
        print(os.path.basename(file_path))
        pprint(output_list)
        print('')


if __name__ == '__main__':
    import glob

    TEST_FILE_FOLDER = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '../', 'tests', 'test_csvs'))
    TEST_FILES = glob.glob(os.path.join(TEST_FILE_FOLDER, '*.csv'))
    for FILE_PATH in TEST_FILES:
        SainsburysParser(FILE_PATH)
