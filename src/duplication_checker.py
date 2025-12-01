import os
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==============================================================
#  DIGITAL SENTINEL MODULE — duplication_checker.py
#  Purpose: Detect and handle duplicate scan results
#  by hashing file contents and filtering identical findings
# ==============================================================

LOG_DIR = "data/logs"
REPORT_DIR = "data/reports"
HASH_INDEX_FILE = os.path.join(LOG_DIR, "hash_index.txt")


def hash_file_content(file_path):
    """Compute a SHA256 hash of a file content (safe read)."""
    try:
        with open(file_path, "rb") as f:
            content = f.read()
            return hashlib.sha256(content).hexdigest()
    except Exception as e:
        print(f"[WARN] Cannot hash file {file_path}: {e}")
        return None


def check_duplicates():
    """Scan reports/logs for duplicates and remove redundant entries."""
    print("🔍 [INFO] Duplication Checker Running...")

    all_files = []
    for base_dir in [LOG_DIR, REPORT_DIR]:
        if os.path.exists(base_dir):
            for root, _, files in os.walk(base_dir):
                for name in files:
                    if name.endswith(".json") or name.endswith(".txt") or name.endswith(".log"):
                        all_files.append(os.path.join(root, name))

    if not all_files:
        print("[WARN] No files found to check for duplicates.")
        return

    print(f"[INFO] Found {len(all_files)} files to check for duplicates...")

    unique_hashes = {}
    duplicates = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(hash_file_content, f): f for f in all_files}
        for future in as_completed(futures):
            file_path = futures[future]
            hash_value = future.result()
            if not hash_value:
                continue
            if hash_value in unique_hashes:
                duplicates.append(file_path)
            else:
                unique_hashes[hash_value] = file_path

    # Save index of unique hashes for later comparison
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(HASH_INDEX_FILE, "w") as idx:
            for h, path in unique_hashes.items():
                idx.write(f"{h} {path}\n")
    except Exception as e:
        print(f"[WARN] Could not write hash index: {e}")

    if duplicates:
        print(f"[INFO] {len(duplicates)} duplicate files detected:")
        for d in duplicates:
            print(f"   🗑️ {d}")
            try:
                os.remove(d)
            except Exception as e:
                print(f"[WARN] Could not remove {d}: {e}")
    else:
        print("[INFO] No duplicates found. ✅")

    print("✅ Duplication Checker finished.\n")
