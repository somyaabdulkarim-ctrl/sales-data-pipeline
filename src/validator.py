import pandas as pd
from src.logger import logger


class DataValidator:
    

    def validate_order_id(self, df):
        order_id_mask = (
        df["order_id"].notna()
        & (df["order_id"].astype(str).str.strip() != "")
        )
        return order_id_mask

    def validate_order_date(self, df):
        order_date_mask = pd.to_datetime(
            df["order_date"],
            format="mixed",
            dayfirst=True,
            errors="coerce"
        ).notna()

        return order_date_mask


    def validate_customer_name(self, df):
        customer_name_mask = (
            df["customer_name"].notna()
            & (df["customer_name"].astype(str).str.strip() != "")
        )
        return customer_name_mask


    def validate_product(self, df):
        product_mask = (
            df["product"].notna()
            & (df["product"].astype(str).str.strip() != "")
        )
        return product_mask


    def validate_quantity(self, df):
        quantity_numeric = pd.to_numeric(
            df["quantity"],
            errors="coerce"
        )

        quantity_mask = (
            quantity_numeric.notna()
            & (quantity_numeric > 0)
        )

        return quantity_mask


    def validate_unit_price(self, df):
        unit_price_numeric = pd.to_numeric(
            df["unit_price"],
            errors="coerce"
        )

        unit_price_mask = (
            unit_price_numeric.notna()
            & (unit_price_numeric > 0)
        )

        return unit_price_mask


    def validate_country(self, df):
        country_mask = (
            df["country"].notna()
            & (df["country"].astype(str).str.strip() != "")
        )
        return country_mask


    def validate(self, df):
        try:
            logger.info("Starting data validation.")
            order_id_valid = self.validate_order_id(df)
            order_date_valid = self.validate_order_date(df)
            customer_name_valid = self.validate_customer_name(df)
            product_valid = self.validate_product(df)
            quantity_valid = self.validate_quantity(df)
            unit_price_valid = self.validate_unit_price(df)
            country_valid = self.validate_country(df)
    
            valid_mask = (
                order_id_valid
                & order_date_valid
                & customer_name_valid
                & product_valid
                & quantity_valid
                & unit_price_valid
                & country_valid
            )
    
            valid_df = df[valid_mask].copy()
            rejected_df = df[~valid_mask].copy()
    
            rejected_df["rejection_reason"] = ""
    
            rejected_df.loc[
                ~order_id_valid,
                "rejection_reason"
            ] += "Order ID is missing; "
    
            rejected_df.loc[
                ~order_date_valid,
                "rejection_reason"
            ] += "Order date is invalid or missing; "
    
            rejected_df.loc[
                ~customer_name_valid,
                "rejection_reason"
            ] += "Customer name is missing; "
    
            rejected_df.loc[
                ~product_valid,
                "rejection_reason"
            ] += "Product is missing; "
    
            rejected_df.loc[
                ~quantity_valid,
                "rejection_reason"
            ] += "Quantity must be a number greater than 0; "
    
            rejected_df.loc[
                ~unit_price_valid,
                "rejection_reason"
            ] += "Unit price must be a number greater than 0; "
    
            rejected_df.loc[
                ~country_valid,
                "rejection_reason"
            ] += "Country is missing; "
    
            rejected_df["rejection_reason"] = (
                rejected_df["rejection_reason"]
                .str.rstrip("; ")
            )
            logger.info(
        f"Validation completed. "
        f"Valid rows: {len(valid_df)}, "
        f"Rejected rows: {len(rejected_df)}"
    )
            return valid_df, rejected_df
        
        except Exception as e:
           logger.error(f"Unexpected error during data validation: {e}")
           raise
# Testing Git version control  
# New validation feature   
# New Validation Comments Adding to the validation file   