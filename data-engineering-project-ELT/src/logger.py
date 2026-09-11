import logging
import os


# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)


# Configure logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger(__name__)