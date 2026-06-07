"""Print a few FIREBALL records to understand the data shape before building an importer."""

import json
from datasets import load_dataset


def main():
    print("Streaming first 3 records from FIREBALL…")
    ds = load_dataset(
        "lara-martin/FIREBALL",
        split="train",
        streaming=True,
        trust_remote_code=True,
    )
    for i, record in enumerate(ds):
        print(f"\n{'='*60}")
        print(f"RECORD {i}")
        print('='*60)
        print(json.dumps(record, indent=2, default=str))
        if i >= 2:
            break


if __name__ == "__main__":
    main()
