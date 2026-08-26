import schedule
import subprocess
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

STREAM_URL = os.getenv("STREAM_URL")
RECORD_SECONDS = int(os.getenv("RECORD_SECONDS", "3600"))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./recordings")
RECORD_TIME = os.getenv("RECORD_TIME", "08:00")
KEEP_DAYS = int(os.getenv("KEEP_DAYS", "7"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

os.makedirs(OUTPUT_DIR, exist_ok=True)
logger.add("radio.log", rotation="1 week", retention="4 weeks")

def rotate_recordings():
    cutoff = datetime.now() - timedelta(days=KEEP_DAYS)
    for fname in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, fname)
        if not os.path.isfile(path):
            continue
        try:
            ts_str = fname.replace("nagranie_", "").replace(".mp3", "")
            ts = datetime.strptime(ts_str, "%Y-%m-%d_%H-%M")
        except Exception:
            continue
        if ts < cutoff:
            logger.info(f"Usuwam stare nagranie: {path}")
            os.remove(path)

def record_once(out_file):
    cmd = [
        "ffmpeg", "-y",
        "-i", STREAM_URL,
        "-t", str(RECORD_SECONDS),
        "-c", "copy",
        out_file
    ]
    logger.info(f"Start ffmpeg: {out_file}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg zakończył się kodem {result.returncode}")
    logger.info(f"Zakończono nagrywanie: {out_file}")

def record():
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    out_file = os.path.join(OUTPUT_DIR, f"nagranie_{ts}.mp3")

    rotate_recordings()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Nagrywanie próba {attempt}/{MAX_RETRIES}")
            record_once(out_file)
            break
        except Exception as e:
            logger.error(f"Błąd nagrywania: {e}")
            if attempt == MAX_RETRIES:
                logger.error("Wyczerpano próby nagrywania.")
            else:
                time.sleep(10)

schedule.every().day.at(RECORD_TIME).do(record)

logger.info("Worker uruchomiony, czeka na zadania...")

while True:
    schedule.run_pending()
    time.sleep(1)
