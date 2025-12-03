import json
import random
import os

TARGET_FILE = "data/targets/global_500_targets.txt"
ROTATED_FILE = "data/targets/rotated_targets.txt"

def load_targets():
    if not os.path.exists(TARGET_FILE):
        return []
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        return [t.strip() for t in f if t.strip()]

def rotate_targets():
    targets = load_targets()
    if not targets:
        return []

    # shuffle full target list
    random.shuffle(targets)

    # select first 100 for next scan batch
    batch = targets[:100]

    with open(ROTATED_FILE, "w", encoding="utf-8") as f:
        for t in batch:
            f.write(t + "\n")

    return batch

if __name__ == "__main__":
    batch = rotate_targets()
    print(f"Rotated {len(batch)} targets → rotation ready.")
