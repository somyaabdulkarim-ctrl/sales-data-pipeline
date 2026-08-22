import pandas as pd
from src.logger import logger

class DataCleaner:

    def clean(self, valid_df):
        logger.info(f"Starting data cleaning")

        try:
            cleaned_df = valid_df.copy()
            
            cleaned_df["order_date"] = pd.to_datetime(
                cleaned_df["order_date"],
                format="mixed",
                dayfirst=True
            )

            cleaned_df["customer_name"] = (
                cleaned_df["customer_name"]
                .str.strip()
                .str.title()
            )

            cleaned_df["product"] = (
                cleaned_df["product"]
                .str.strip()
            )

            cleaned_df["country"] = (
                cleaned_df["country"]
                .str.strip()
                .str.title()
            )

            cleaned_df = cleaned_df.drop_duplicates()

            cleaned_df = cleaned_df.reset_index(drop=True)

            logger.info(f"Data cleaning completed." f" Clean raws : {len(cleaned_df)}")

            return cleaned_df    
        except Exception as e:
             logger.error(f"Unexcepted error during data cleaning :{e}")
             raise