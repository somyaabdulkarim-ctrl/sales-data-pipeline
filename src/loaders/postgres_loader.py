from src.loaders.data_loader import DataLoader
from src.loaders.database import get_database_connection
from src.logger import logger


class PostgresLoader(DataLoader):

    def load(self, cleaned_df, output_file=None):
        connection = None
        cursor = None
        
        try:
                logger.info("Starting PostgreSQL load")
                logger.info(f"Rows received: {len(cleaned_df)}")
                connection = get_database_connection()
                cursor = connection.cursor()
        
                insert_query = """
                INSERT INTO sales_data
                (order_id, order_date, customer_name, product, quantity, unit_price, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING
                """
                inserted_rows = 0
                for _, row in cleaned_df.iterrows():
                    values = (
                        int(row["order_id"]),
                        row["order_date"],
                        row["customer_name"],
                        row["product"],
                        int(row["quantity"]),
                        row["unit_price"],
                        row["country"]
                    )
        
                    cursor.execute(insert_query, values)
                    inserted_rows += cursor.rowcount
        
                connection.commit()
                skipped_rows = len(cleaned_df) - inserted_rows
                logger.info(f"Rows inserted: {inserted_rows}")
                logger.info(f"Rows skipped: {skipped_rows}")
                logger.info("PostgreSQL load completed successfully")
        
        except Exception:
                if connection:
                    connection.rollback()
                raise
        
        finally:
                if cursor:
                    cursor.close()
        
                if connection:
                    connection.close()