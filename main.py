from src.reader import CSVReader
from src.validator import DataValidator
from src.cleaner import DataCleaner
from src.report import PipelineReport
#from src.loaders.csv_loader import CSVLoader
from src.loaders.postgres_loader import PostgresLoader
from src.pipeline import DataPipeline
from src.logger import logger
from src.config import RAW_DATA_PATH

logger.info("Pipeline Started")
reader=CSVReader(RAW_DATA_PATH)
validator=DataValidator()
cleaner=DataCleaner()
report=PipelineReport()
#loader=CSVLoader()
loader=PostgresLoader()
pipeline=DataPipeline(
    reader,
    validator,
    cleaner,
    report,
    loader
)
pipeline.run()

