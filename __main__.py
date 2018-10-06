import os
import yaml

from Parser.parser import SainsburysParser
import glob

if __name__ == '__main__':

    def list_all_csv_files_in_config_path() -> list:
        """Returns a list of  all the csv files found in the path
        specified in the config.yaml file.
        """
        config = yaml.load(open(os.path.join(os.path.dirname(__file__),
                                             "config.yaml"), 'r'))
        folder_path = config['relative_file_path']
        csv_file_folder = os.path.abspath(os.path.join(
            os.path.dirname(__file__), folder_path))
        csv_files = glob.glob(os.path.join(csv_file_folder, '*.csv'))
        return csv_files


    for file_path in list_all_csv_files_in_config_path():
        SainsburysParser(file_path)
