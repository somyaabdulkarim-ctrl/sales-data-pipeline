from pathlib import Path
from src.logger import logger

class PipelineReport:

    def generate(
        self,
        original_df,
        valid_df,
        rejected_df,
        cleaned_df,
        output_file
    ):
        """
        Generate a text report that summarises the pipeline results.

        Parameters:
            original_df: DataFrame before validation.
            valid_df: DataFrame containing rows that passed validation.
            rejected_df: DataFrame containing rejected rows and reasons.
            cleaned_df: Final DataFrame after cleaning.
            output_file: Path where the report will be saved.
        """
        logger.info("Starting pipeline report generation.")
        try:
            total_rows = len(original_df)
            valid_rows = len(valid_df)
            rejected_rows = len(rejected_df)
            cleaned_rows = len(cleaned_df)

            duplicates_removed = valid_rows - cleaned_rows

            # Ensure the output folder exists.
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as file:

                file.write("SALES DATA PIPELINE REPORT\n")
                file.write("=" * 50 + "\n\n")

                file.write("PIPELINE SUMMARY\n")
                file.write("-" * 50 + "\n")

                file.write(f"Total rows: {total_rows}\n")
                file.write(f"Valid rows: {valid_rows}\n")
                file.write(f"Rejected rows: {rejected_rows}\n")
                file.write(f"Cleaned rows: {cleaned_rows}\n")
                file.write(f"Duplicates removed: {duplicates_removed}\n\n")

                file.write("VALIDATION CHECK\n")
                file.write("-" * 50 + "\n")

                if total_rows == valid_rows + rejected_rows:
                    file.write(
                        "Validation row count check: PASSED\n"
                    )
                else:
                    file.write(
                        "Validation row count check: FAILED\n"
                    )

                file.write(
                    f"Expected total: {total_rows}\n"
                )

                file.write(
                    f"Valid + rejected: {valid_rows + rejected_rows}\n\n"
                )

                file.write("REJECTION SUMMARY\n")
                file.write("-" * 50 + "\n")

                if rejected_df.empty:
                    file.write("No rows were rejected.\n\n")

                else:
                    rejection_counts = (
                        rejected_df["rejection_reason"]
                        .value_counts()
                    )

                    for reason, count in rejection_counts.items():
                        file.write(f"{reason}: {count}\n")

                    file.write("\n")

                    file.write("REJECTED ROW DETAILS\n")
                    file.write("-" * 50 + "\n")

                    for index, row in rejected_df.iterrows():
                        file.write(f"Original row index: {index}\n")

                        for column in rejected_df.columns:
                            file.write(
                                f"{column}: {row[column]}\n"
                            )

                        file.write("-" * 50 + "\n")

                file.write("\nEND OF REPORT\n")

            logger.info(f"Pipeline report saved successfully to : {output_path}")
            return True

        except PermissionError:
            logger.error(f"Permission denied while saving report to :{output_file}")
            raise
        except Exception as e:
            logger.error(f"Unexcepted error during report generation : {e}")
            raise
