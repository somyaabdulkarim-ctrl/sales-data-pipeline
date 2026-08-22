import pandas as pd

from src.logger import logger


class CSVReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):

        logger.info(
            f"Reading CSV file from: {self.file_path}"
        )

        try:
            df = pd.read_csv(self.file_path)

            logger.info(
                f"CSV file read successfully. "
                f"Rows loaded: {len(df)}"
            )

            return df

        except FileNotFoundError:
            logger.error(
                f"CSV file not found: {self.file_path}"
            )
            raise

        except PermissionError:
            logger.error(
                f"Permission denied while reading CSV file: "
                f"{self.file_path}"
            )
            raise

        except pd.errors.EmptyDataError:
            logger.error(
                f"CSV file is empty: {self.file_path}"
            )
            raise

        except pd.errors.ParserError as e:
            logger.error(
                f"Failed to parse CSV file "
                f"{self.file_path}: {e}"
            )
            raise

        except Exception as e:
            logger.error(
                f"Unexpected error while reading "
                f"{self.file_path}: {e}"
            )
            raise