import json
from datetime import date
import logging

logger = logging.getLogger(__name__)

def load_data():
    file_path = f"./data/YT_data_{date.today()}"

    try:
        logger.info(f"Processing file: YT_data_{date.today()}")

        with open(file_path,'r', encoding='utf-8') as raw_data:
            # Use this for small json dataset
            # if large json dataset, user streaming parser 
            # such as Node.js stream-json, Python ijson, or line‑by‑line NDJSON processing
            data = json.load(raw_data)

            return data

    except FileNotFoundError:
        logger.error(f"File not found:{file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file:{file_path}")
        raise