import os
import subprocess
import time
import logging

# Configuration
BASE_DIR = os.path.expanduser("~/code/FluentNao")
PHOTOS_DIR = os.path.join(BASE_DIR, "data/photos/")
AUDIO_DIR = os.path.join(BASE_DIR, "data/audio/")
WHISPER_PATH = os.path.expanduser("~/.local/bin/whisper")
LOG_FILE = os.path.join(BASE_DIR, "data/monitor.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_photos():
    for filename in os.listdir(PHOTOS_DIR):
        if filename.endswith(".ppm"):
            ppm_path = os.path.join(PHOTOS_DIR, filename)
            png_path = os.path.join(PHOTOS_DIR, filename.replace(".ppm", ".png"))
            
            if not os.path.exists(png_path):
                logging.info(f"Converting {ppm_path} to {png_path}")
                try:
                    subprocess.run(["convert", ppm_path, png_path], check=True)
                    logging.info(f"Successfully converted {filename}")
                except Exception as e:
                    logging.error(f"Failed to convert {filename}: {e}")

def process_audio():
    for filename in os.listdir(AUDIO_DIR):
        if filename.endswith(".wav"):
            wav_path = os.path.join(AUDIO_DIR, filename)
            # Whisper usually outputs [filename].txt or similar
            base_name = os.path.splitext(filename)[0]
            txt_path = os.path.join(AUDIO_DIR, f"{base_name}.txt")
            
            if not os.path.exists(txt_path):
                logging.info(f"Transcribing {wav_path}")
                try:
                    # Whisper command: whisper [file] --output_dir [dir] --output_format txt
                    subprocess.run([
                        WHISPER_PATH, 
                        wav_path, 
                        "--output_dir", AUDIO_DIR, 
                        "--output_format", "txt",
                        "--model", "base" # Using base model for speed
                    ], check=True)
                    logging.info(f"Successfully transcribed {filename}")
                    
                    # Log interesting findings
                    with open(txt_path, 'r') as f:
                        transcript = f.read().strip()
                        logging.info(f"Transcript for {filename}: {transcript}")
                        if any(keyword in transcript.lower() for keyword in ["help", "emergency", "stop", "danger", "found"]):
                            logging.warning(f"INTERESTING TRANSCRIPT in {filename}: {transcript}")
                except Exception as e:
                    logging.error(f"Failed to transcribe {filename}: {e}")

def main():
    logging.info("Starting FluentNao monitor...")
    while True:
        try:
            process_photos()
            process_audio()
        except Exception as e:
            logging.error(f"Error in monitor loop: {e}")
        time.sleep(10) # Check every 10 seconds

if __name__ == "__main__":
    main()
