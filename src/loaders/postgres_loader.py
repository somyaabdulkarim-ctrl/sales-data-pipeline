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
                batch_size=500
                inserted_rows = 0
                
                for start in range(0,len(cleaned_df),batch_size):
                    end=start+batch_size
                    batch= cleaned_df.iloc[start:end]
                    batch_values=[]

                    for _, row in batch.iterrows():    
                        values = (
                        int(row["order_id"]),
                        row["order_date"],
                        row["customer_name"],
                        row["product"],
                        int(row["quantity"]),
                        row["unit_price"],
                        row["country"]
                        )
                        batch_values.append(values)
        
                    cursor.executemany(insert_query, batch_values)
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