"""Configuration settings, environment variables, and global constants."""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from docx.shared import RGBColor

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "video_synopsis_ai")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "synopses")

mongo_client = AsyncIOMotorClient(MONGO_URI)
synopsis_collection = mongo_client[MONGO_DB_NAME][MONGO_COLLECTION]

OUTPUT_DIR = os.path.join(os.getcwd(), "generated_exports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BRAND_COLOR = "#1a73e8"
BRAND_COLOR_RGB = RGBColor(0x1A, 0x73, 0xE8)
TEXT_COLOR_RGB = RGBColor(0x20, 0x21, 0x24)
MUTED_RGB = RGBColor(0x80, 0x86, 0x8B)
