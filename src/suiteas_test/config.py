"""Configuration for running the test suite."""
import os

from dotenv import load_dotenv
from pydantic import TypeAdapter

load_dotenv()

FAST_TESTS = TypeAdapter(bool).validate_python(
    os.getenv("SUITEAS_FAST_TESTS", default="False"),
)
