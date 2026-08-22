from src.logger import logger
class DataPipeline:

    def __init__(
        self,
        reader,
        validator,
        cleaner,
        report,
        loader
    ):
        self.reader = reader
        self.validator = validator
        self.cleaner = cleaner
        self.report = report
        self.loader = loader

    def run(self):

        try:
            df = self.reader.read()
             
            valid_df, rejected_df = self.validator.validate(df)
    
            cleaned_df = self.cleaner.clean(valid_df)
    
            report_result = self.report.generate(
                original_df=df,
                valid_df=valid_df,
                rejected_df=rejected_df,
                cleaned_df=cleaned_df,
                output_file="reports/pipeline_report.txt"
            )
    
            if report_result:
                self.loader.load(
                    cleaned_df,
                    "data/clean_sales.csv"
                )

            else:
                raise Exception(
                    "Pipeline stopped because report generation failed."
                )
            logger.info("Pipeline completed successfully")
        except Exception :
              logger.exception("Pipeline excuation faild")
              raise
            