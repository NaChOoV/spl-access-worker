import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "SPL_ACCESS_BASE_URL": os.getenv("SPL_ACCESS_BASE_URL", "http://localhost:30002/"),
    "SPL_ACCESS_TOKEN": os.getenv("SPL_ACCESS_TOKEN", "-"),
    "SOURCE_BASE_URL": os.getenv("SOURCE_BASE_URL", "-"),
    "SOURCE_USERNAME": os.getenv("SOURCE_USERNAME", "-"),
    "SOURCE_PASSWORD": os.getenv("SOURCE_PASSWORD", "-"),
}
