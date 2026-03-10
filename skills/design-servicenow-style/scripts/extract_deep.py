#!/usr/bin/env python3
"""
Deep extraction script - runs with proper rate limiting.
Extracts full-depth data from ServiceNow Figma files.

Usage:
    python extract_deep.py --token YOUR_PAT --file-key KEY [--page-ids id1,id2,...] [--all-pages]

Respects rate limits with 8-second intervals between requests.
Writes progress to output/progress.json so it can resume after interruption.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

API_BASE = "https://api.figma.com/v1"
INTERVAL = 8  # seconds between requests - safe for Starter Full seat (10/min)


def api_get(token, url, params=None, max_retries=3):
    """Rate-limited API request with retry on 429."""
    headers = {"X-Figma-Token": token}
    for attempt in range(max_retries):
        resp = requests.get(f"{API_BASE}{url}", headers=headers, params=params)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 120))
            print(f"  ⚠ Rate limited (attempt {attempt+1}). Waiting {retry_after}s...")
            time.sleep(retry_after + 5)
        else:
            print(f"  ✗ HTTP {resp.status_code}: {resp.text[:200]}")
            return None
    return None


def extract_file(token, file_key, output_dir, page_ids=None, all_pages=False):
    """Extract full data from a Figma file."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    progress_file = out / "progress.json"

    # Load or init progress
    if progress_file.exists():
        with open(progress_file) as f:
            progress = json.load(f)
    else:
        progress = {"completed_pages": [], "file_key": file_key}

    # Step 1: Get file structure if not done
    structure_file = out / "file_structure.json"
    if not structure_file.exists():
        print("[1] Getting file structure (depth=2)...")
        data = api_get(token, f"/files/{file_key}", {"depth": 2})
        if data:
            with open(structure_file, "w") as f:
                json.dump(data, f, indent=2)
            print(f"  ✓ {data.get('name', 'Unknown')} - {len(data.get('document',{}).get('children',[]))} pages")
        else:
            print("  ✗ Failed to get file structure")
            return
        time.sleep(INTERVAL)
    else:
        with open(structure_file) as f:
            data = json.load(f)
        print(f"[1] File structure already cached: {data.get('name','')}")

    # Step 2: Get styles
    styles_file = out / "styles.json"
    if not styles_file.exists():
        print("[2] Getting styles...")
        styles = api_get(token, f"/files/{file_key}/styles")
        if styles:
            with open(styles_file, "w") as f:
                json.dump(styles, f, indent=2)
            meta = styles.get("meta", {}).get("styles", [])
            print(f"  ✓ {len(meta)} styles")
        time.sleep(INTERVAL)
    else:
        print("[2] Styles already cached")

    # Step 3: Get components
    comp_file = out / "components.json"
    if not comp_file.exists():
        print("[3] Getting components...")
        comps = api_get(token, f"/files/{file_key}/components")
        if comps:
            with open(comp_file, "w") as f:
                json.dump(comps, f, indent=2)
            meta = comps.get("meta", {}).get("components", [])
            print(f"  ✓ {len(meta)} components")
        time.sleep(INTERVAL)
    else:
        print("[3] Components already cached")

    # Step 4: Get component sets
    sets_file = out / "component_sets.json"
    if not sets_file.exists():
        print("[4] Getting component sets...")
        sets = api_get(token, f"/files/{file_key}/component_sets")
        if sets:
            with open(sets_file, "w") as f:
                json.dump(sets, f, indent=2)
            meta = sets.get("meta", {}).get("component_sets", [])
            print(f"  ✓ {len(meta)} component sets")
        time.sleep(INTERVAL)
    else:
        print("[4] Component sets already cached")

    # Step 5: Deep-extract pages
    pages = data.get("document", {}).get("children", [])

    if page_ids:
        target_pages = [p for p in pages if p["id"] in page_ids]
    elif all_pages:
        target_pages = pages
    else:
        # Default: extract key pages (guidelines, getting started, component categories)
        key_names = ["Guidelines", "Getting started", "Cover"]
        target_pages = [p for p in pages if any(k.lower() in p.get("name", "").lower() for k in key_names)]
        # Also include category folders
        target_pages.extend([p for p in pages if p.get("name", "").startswith("📂")])

    remaining = [p for p in target_pages if p["id"] not in progress["completed_pages"]]
    print(f"\n[5] Deep-extracting {len(remaining)} pages ({len(progress['completed_pages'])} already done)...")

    for i, page in enumerate(remaining):
        pid = page["id"]
        pname = page.get("name", "Unknown")
        safe_id = pid.replace(":", "_")

        page_file = out / f"page_{safe_id}.json"
        if page_file.exists():
            progress["completed_pages"].append(pid)
            continue

        print(f"\n  [{i+1}/{len(remaining)}] {pname} (ID: {pid})...")
        node_data = api_get(token, f"/files/{file_key}/nodes", {"ids": pid, "depth": 10})
        if node_data:
            with open(page_file, "w") as f:
                json.dump(node_data, f, indent=2)
            fsize = os.path.getsize(page_file)
            print(f"  ✓ Saved ({fsize:,} bytes)")
            progress["completed_pages"].append(pid)
        else:
            print(f"  ✗ Failed")

        # Save progress
        with open(progress_file, "w") as f:
            json.dump(progress, f, indent=2)

        time.sleep(INTERVAL)

    print(f"\n✓ Extraction complete. {len(progress['completed_pages'])} pages extracted.")
    with open(progress_file, "w") as f:
        json.dump(progress, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Deep Figma extraction with rate limiting")
    parser.add_argument("--token", required=True)
    parser.add_argument("--file-key", required=True)
    parser.add_argument("--output-dir", default="output/deep")
    parser.add_argument("--page-ids", help="Comma-separated page IDs to extract")
    parser.add_argument("--all-pages", action="store_true", help="Extract ALL pages (slow)")
    args = parser.parse_args()

    page_ids = args.page_ids.split(",") if args.page_ids else None
    extract_file(args.token, args.file_key, args.output_dir, page_ids, args.all_pages)


if __name__ == "__main__":
    main()
