#!/usr/bin/env python3
"""
Data Download Tool for Pleio DataHub

Lists available datasets and downloads selected files using azcopy.
"""

import json
import os
import subprocess
import sys
from typing import Optional

import requests

API_BASE = "https://datahub.pleio.nl/api/v1"
DATA_DIR = "/app/data"


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def fetch_datasets(limit: int = 25, classification: int = 4) -> list:
    """Fetch available datasets from the API."""
    url = f"{API_BASE}/files/"
    params = {"limit": limit, "classification": classification}
    headers = {"Accept": "application/json"}

    print(f"\nFetching datasets from {url}...")
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data.get("results", [])


def get_download_url(file_id: int) -> Optional[dict]:
    """Get download URL with SAS token for a file."""
    url = f"{API_BASE}/files/{file_id}/download/"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()


def download_file(download_url: str, filename: str) -> bool:
    """Download file using azcopy."""
    output_path = os.path.join(DATA_DIR, filename)

    print(f"\nDownloading to: {output_path}")
    print("Using azcopy for optimized transfer...")

    try:
        result = subprocess.run(
            ["azcopy", "copy", download_url, output_path],
            check=True,
            capture_output=False,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Download failed: {e}")
        return False
    except FileNotFoundError:
        print("Error: azcopy not found. Please ensure it's installed.")
        return False


def display_datasets(datasets: list) -> None:
    """Display datasets in a formatted table."""
    print("\n" + "=" * 100)
    print("AVAILABLE DATASETS")
    print("=" * 100)
    print(f"{'#':<4} {'Name':<40} {'Size':<10} {'Zone':<25} {'Study':<20}")
    print("-" * 100)

    for i, ds in enumerate(datasets, 1):
        name = ds.get("name", "Unknown")[:38]
        size = format_size(ds.get("size", 0))
        zone = (ds.get("zone") or {}).get("name", "N/A")[:23]
        study = (ds.get("study") or {}).get("name", "N/A")[:18]

        print(f"{i:<4} {name:<40} {size:<10} {zone:<25} {study:<20}")

    print("=" * 100)
    print(f"Total: {len(datasets)} datasets")


def display_dataset_details(dataset: dict) -> None:
    """Display detailed information about a dataset."""
    print("\n" + "-" * 60)
    print("DATASET DETAILS")
    print("-" * 60)
    print(f"  ID:             {dataset.get('id')}")
    print(f"  Name:           {dataset.get('name')}")
    print(f"  Size:           {format_size(dataset.get('size', 0))}")
    print(f"  Zone:           {(dataset.get('zone') or {}).get('name', 'N/A')}")
    print(f"  Study:          {(dataset.get('study') or {}).get('name', 'N/A')}")
    print(f"  Classification: {(dataset.get('classification') or {}).get('name', 'N/A')}")
    print(f"  Extension:      {(dataset.get('extension') or {}).get('name', 'N/A')}")
    print(f"  Downloads:      {dataset.get('nr_downloads', 0)}")
    print(f"  Published:      {dataset.get('published', False)}")
    print("-" * 60)


def interactive_menu(datasets: list) -> None:
    """Run interactive download menu."""
    while True:
        display_datasets(datasets)

        print("\nOptions:")
        print("  Enter number (1-{}) to select dataset".format(len(datasets)))
        print("  'a' - Download all datasets")
        print("  'r' - Refresh dataset list")
        print("  'q' - Quit")

        choice = input("\nYour choice: ").strip().lower()

        if choice == "q":
            print("\nExiting...")
            break
        elif choice == "r":
            datasets = fetch_datasets()
            continue
        elif choice == "a":
            confirm = input(f"\nDownload ALL {len(datasets)} datasets? (yes/no): ").strip().lower()
            if confirm == "yes":
                for ds in datasets:
                    download_single(ds)
            continue

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(datasets):
                dataset = datasets[idx]
                display_dataset_details(dataset)

                action = input("\nDownload this file? (y/n): ").strip().lower()
                if action == "y":
                    download_single(dataset)
            else:
                print(f"\nInvalid selection. Enter 1-{len(datasets)}")
        except ValueError:
            print("\nInvalid input. Enter a number or command.")


def download_single(dataset: dict) -> None:
    """Download a single dataset."""
    file_id = dataset.get("id")
    filename = dataset.get("name", f"file_{file_id}")

    print(f"\nPreparing download for: {filename}")

    try:
        download_info = get_download_url(file_id)
        download_url = download_info.get("download_url")

        if not download_url:
            print("Error: Could not obtain download URL")
            return

        success = download_file(download_url, filename)

        if success:
            print(f"\nDownload complete: {filename}")
        else:
            print(f"\nDownload failed: {filename}")

    except requests.RequestException as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("  PLEIO DATAHUB DOWNLOAD TOOL")
    print("  Dutch Offshore Wind GIS Data")
    print("=" * 60)

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        datasets = fetch_datasets()

        if not datasets:
            print("\nNo datasets found.")
            return

        print(f"\nFound {len(datasets)} datasets")

        interactive_menu(datasets)

    except requests.RequestException as e:
        print(f"\nFailed to fetch datasets: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
