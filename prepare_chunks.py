import json
import re
from pathlib import Path

INPUT_PATH = Path("parsed/parsed_threads.json")
OUTPUT_PATH = Path("parsed/chunks.json")

def normalize_id(text):
    return re.sub(r'[^a-z0-9_]+', '_', text.lower())

def load_threads():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def thread_to_chunk(thread):
    content_lines = [f"Thread: {thread['thread_title']}"]
    for msg in thread["messages"]:
        content_lines.append(f"{msg['user']} ({msg['timestamp']}): {msg['text'].strip()}")
    full_text = "\n".join(content_lines)

    return {
        "id": f"{normalize_id(thread['channel'])}-{normalize_id(thread['thread_title'])}",
        "channel": thread["channel"],
        "thread_title": thread["thread_title"],
        "content": full_text
    }

def convert_all_threads():
    threads = load_threads()
    chunks = [thread_to_chunk(t) for t in threads]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)
    
    print(f" Saved {len(chunks)} chunks to {OUTPUT_PATH}")


if __name__ == "__main__":
    convert_all_threads()
