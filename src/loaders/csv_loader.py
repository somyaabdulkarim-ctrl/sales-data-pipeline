from pathlib import Path
from src.loaders.data_loader import DataLoader
from src.logger import logger

class CSVLoader(DataLoader):

    def load(self, cleaned_df, output_file):
        logger.info(f"Saving cleaned data to :{output_file}")
        try:
            Path(output_file).parent.mkdir(
                parents=True,
                exist_ok=True
            )

            cleaned_df.to_csv(
                output_file,
                index=False
            )

            logger.info(
                f"Cleaned data saved successfully to: {output_file}"
            )
        except Exception as e:
            logger.error(f"Unexcepted error while saving cleaned data : {e}")
            raise