#!/usr/bin/env python3
"""
Data Download Tool for GIS Data APIs

Lists available datasets and downloads selected files using azcopy.
Designed for both interactive and programmatic (agentic) use.

Usage:
    # List available datasets
    python data_download.py list
    python data_download.py --json list
    python data_download.py --limit 50 --json list

    # Show dataset details
    python data_download.py info --id 123
    python data_download.py --json info --index 5

    # Download datasets
    python data_download.py download --id 123
    python data_download.py download --id 123 456 789
    python data_download.py download --index 1 2 3
    python data_download.py download --all

    # Search datasets
    python data_download.py search "keyword"
    python data_download.py --json search "keyword"

    # Custom API/output directory
    python data_download.py --api-base https://api.example.com/v1 list

Note: Global options (--json, --limit, --api-base, --output-dir) must come BEFORE the subcommand.
"""

import argparse
import json
import os
import subprocess
import sys
from typing import Optional

import requests

# Default configuration
DEFAULT_API_BASE = "https://datahub.pleio.nl/api/v1"
DEFAULT_DATA_DIR = "./data"
DEFAULT_LIMIT = 25
DEFAULT_CLASSIFICATION = 4


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def fetch_datasets(
    api_base: str,
    limit: int = DEFAULT_LIMIT,
    classification: Optional[int] = DEFAULT_CLASSIFICATION,
) -> list:
    """Fetch available datasets from the API."""
    url = f"{api_base}/files/"
    params = {"limit": limit}
    if classification is not None:
        params["classification"] = classification
    headers = {"Accept": "application/json"}

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data.get("results", [])


def get_download_url(api_base: str, file_id: int) -> Optional[dict]:
    """Get download URL with SAS token for a file."""
    url = f"{api_base}/files/{file_id}/download/"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()


def download_file(download_url: str, output_path: str, use_azcopy: bool = True) -> bool:
    """Download file using azcopy or requests fallback."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    if use_azcopy:
        try:
            result = subprocess.run(
                ["azcopy", "copy", download_url, output_path],
                check=True,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"azcopy failed: {e.stderr}", file=sys.stderr)
            return False
        except FileNotFoundError:
            print("Warning: azcopy not found, falling back to requests", file=sys.stderr)

    # Fallback to requests
    try:
        response = requests.get(download_url, stream=True, timeout=300)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Download failed: {e}", file=sys.stderr)
        return False


def format_dataset_table(datasets: list) -> str:
    """Format datasets as a table string."""
    lines = []
    lines.append("=" * 100)
    lines.append(f"{'#':<4} {'ID':<8} {'Name':<35} {'Size':<10} {'Zone':<22} {'Study':<18}")
    lines.append("-" * 100)

    for i, ds in enumerate(datasets, 1):
        name = ds.get("name", "Unknown")[:33]
        size = format_size(ds.get("size", 0))
        zone = (ds.get("zone") or {}).get("name", "N/A")[:20]
        study = (ds.get("study") or {}).get("name", "N/A")[:16]
        file_id = ds.get("id", "N/A")

        lines.append(f"{i:<4} {file_id:<8} {name:<35} {size:<10} {zone:<22} {study:<18}")

    lines.append("=" * 100)
    lines.append(f"Total: {len(datasets)} datasets")
    return "\n".join(lines)


def format_dataset_details(dataset: dict) -> str:
    """Format detailed information about a dataset."""
    lines = []
    lines.append("-" * 60)
    lines.append("DATASET DETAILS")
    lines.append("-" * 60)
    lines.append(f"  ID:             {dataset.get('id')}")
    lines.append(f"  Name:           {dataset.get('name')}")
    lines.append(f"  Size:           {format_size(dataset.get('size', 0))}")
    lines.append(f"  Zone:           {(dataset.get('zone') or {}).get('name', 'N/A')}")
    lines.append(f"  Study:          {(dataset.get('study') or {}).get('name', 'N/A')}")
    lines.append(f"  Classification: {(dataset.get('classification') or {}).get('name', 'N/A')}")
    lines.append(f"  Extension:      {(dataset.get('extension') or {}).get('name', 'N/A')}")
    lines.append(f"  Downloads:      {dataset.get('nr_downloads', 0)}")
    lines.append(f"  Published:      {dataset.get('published', False)}")
    lines.append("-" * 60)
    return "\n".join(lines)


def download_dataset(
    dataset: dict,
    api_base: str,
    output_dir: str,
    use_azcopy: bool = True,
) -> dict:
    """Download a single dataset. Returns result dict."""
    file_id = dataset.get("id")
    filename = dataset.get("name", f"file_{file_id}")
    output_path = os.path.join(output_dir, filename)

    result = {
        "id": file_id,
        "name": filename,
        "output_path": output_path,
        "success": False,
        "error": None,
    }

    try:
        download_info = get_download_url(api_base, file_id)
        download_url = download_info.get("download_url")

        if not download_url:
            result["error"] = "Could not obtain download URL"
            return result

        success = download_file(download_url, output_path, use_azcopy)
        result["success"] = success
        if not success:
            result["error"] = "Download failed"

    except requests.RequestException as e:
        result["error"] = f"API error: {e}"
    except Exception as e:
        result["error"] = f"Unexpected error: {e}"

    return result


# ============================================================================
# Command handlers
# ============================================================================


def cmd_list(args) -> int:
    """List available datasets."""
    try:
        datasets = fetch_datasets(
            api_base=args.api_base,
            limit=args.limit,
            classification=args.classification,
        )

        if not datasets:
            if args.json:
                print(json.dumps({"datasets": [], "count": 0}))
            else:
                print("No datasets found.")
            return 0

        if args.json:
            output = {
                "datasets": datasets,
                "count": len(datasets),
            }
            print(json.dumps(output, indent=2))
        else:
            print(format_dataset_table(datasets))

        return 0

    except requests.RequestException as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Failed to fetch datasets: {e}", file=sys.stderr)
        return 1


def cmd_info(args) -> int:
    """Show dataset details."""
    try:
        datasets = fetch_datasets(
            api_base=args.api_base,
            limit=args.limit,
            classification=args.classification,
        )

        target_dataset = None

        if args.id:
            for ds in datasets:
                if ds.get("id") == args.id:
                    target_dataset = ds
                    break
            if not target_dataset:
                error_msg = f"Dataset with ID {args.id} not found"
                if args.json:
                    print(json.dumps({"error": error_msg}))
                else:
                    print(error_msg, file=sys.stderr)
                return 1

        elif args.index:
            if 1 <= args.index <= len(datasets):
                target_dataset = datasets[args.index - 1]
            else:
                error_msg = f"Invalid index {args.index}. Valid range: 1-{len(datasets)}"
                if args.json:
                    print(json.dumps({"error": error_msg}))
                else:
                    print(error_msg, file=sys.stderr)
                return 1

        if args.json:
            print(json.dumps(target_dataset, indent=2))
        else:
            print(format_dataset_details(target_dataset))

        return 0

    except requests.RequestException as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Failed to fetch datasets: {e}", file=sys.stderr)
        return 1


def cmd_download(args) -> int:
    """Download datasets."""
    try:
        datasets = fetch_datasets(
            api_base=args.api_base,
            limit=args.limit,
            classification=args.classification,
        )

        if not datasets:
            if args.json:
                print(json.dumps({"error": "No datasets found"}))
            else:
                print("No datasets found.", file=sys.stderr)
            return 1

        # Determine which datasets to download
        to_download = []

        if args.all:
            to_download = datasets
        elif args.id:
            id_set = set(args.id)
            for ds in datasets:
                if ds.get("id") in id_set:
                    to_download.append(ds)
            missing = id_set - {ds.get("id") for ds in to_download}
            if missing:
                print(f"Warning: IDs not found: {missing}", file=sys.stderr)
        elif args.index:
            for idx in args.index:
                if 1 <= idx <= len(datasets):
                    to_download.append(datasets[idx - 1])
                else:
                    print(f"Warning: Invalid index {idx}, skipping", file=sys.stderr)

        if not to_download:
            if args.json:
                print(json.dumps({"error": "No datasets matched selection"}))
            else:
                print("No datasets matched selection.", file=sys.stderr)
            return 1

        # Ensure output directory exists
        os.makedirs(args.output_dir, exist_ok=True)

        # Download each dataset
        results = []
        for ds in to_download:
            if not args.json:
                print(f"Downloading: {ds.get('name')}...")

            result = download_dataset(
                dataset=ds,
                api_base=args.api_base,
                output_dir=args.output_dir,
                use_azcopy=not args.no_azcopy,
            )
            results.append(result)

            if not args.json:
                if result["success"]:
                    print(f"  ✓ Saved to: {result['output_path']}")
                else:
                    print(f"  ✗ Failed: {result['error']}")

        if args.json:
            output = {
                "results": results,
                "total": len(results),
                "successful": sum(1 for r in results if r["success"]),
                "failed": sum(1 for r in results if not r["success"]),
            }
            print(json.dumps(output, indent=2))
        else:
            successful = sum(1 for r in results if r["success"])
            print(f"\nComplete: {successful}/{len(results)} downloads successful")

        # Return non-zero if any downloads failed
        return 0 if all(r["success"] for r in results) else 1

    except requests.RequestException as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Failed to fetch datasets: {e}", file=sys.stderr)
        return 1


def cmd_search(args) -> int:
    """Search datasets by keyword."""
    try:
        datasets = fetch_datasets(
            api_base=args.api_base,
            limit=args.limit,
            classification=args.classification,
        )

        keyword = args.keyword.lower()
        matches = []

        for ds in datasets:
            searchable = " ".join([
                ds.get("name", ""),
                (ds.get("zone") or {}).get("name", ""),
                (ds.get("study") or {}).get("name", ""),
            ]).lower()

            if keyword in searchable:
                matches.append(ds)

        if args.json:
            output = {
                "query": args.keyword,
                "datasets": matches,
                "count": len(matches),
            }
            print(json.dumps(output, indent=2))
        else:
            if matches:
                print(f"Found {len(matches)} datasets matching '{args.keyword}':\n")
                print(format_dataset_table(matches))
            else:
                print(f"No datasets found matching '{args.keyword}'")

        return 0

    except requests.RequestException as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Failed to fetch datasets: {e}", file=sys.stderr)
        return 1


# ============================================================================
# Main entry point
# ============================================================================


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Download GIS data from APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                          List all datasets
  %(prog)s --json list                   List as JSON (for parsing)
  %(prog)s --limit 50 list               List with custom limit
  %(prog)s info --id 123                 Show details for dataset ID 123
  %(prog)s --json info --index 5         Show 5th dataset as JSON
  %(prog)s download --id 123 456         Download datasets by ID
  %(prog)s download --index 1 2 3        Download by list index
  %(prog)s download --all                Download all datasets
  %(prog)s search "wind farm"            Search datasets by keyword
  %(prog)s --json search "wind"          Search with JSON output

Note: Global options (--json, --limit, etc.) go BEFORE the subcommand.
        """,
    )

    # Global options
    parser.add_argument(
        "--api-base",
        default=os.environ.get("DATA_API_BASE", DEFAULT_API_BASE),
        help=f"API base URL (default: {DEFAULT_API_BASE})",
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("DATA_OUTPUT_DIR", DEFAULT_DATA_DIR),
        help=f"Output directory for downloads (default: {DEFAULT_DATA_DIR})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Maximum datasets to fetch (default: {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--classification",
        type=int,
        default=DEFAULT_CLASSIFICATION,
        help=f"Classification filter (default: {DEFAULT_CLASSIFICATION}, use -1 for none)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format (for programmatic parsing)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List available datasets")
    list_parser.set_defaults(func=cmd_list)

    # Info command
    info_parser = subparsers.add_parser("info", help="Show dataset details")
    info_group = info_parser.add_mutually_exclusive_group(required=True)
    info_group.add_argument("--id", type=int, help="Dataset ID")
    info_group.add_argument("--index", type=int, help="Dataset index (1-based)")
    info_parser.set_defaults(func=cmd_info)

    # Download command
    dl_parser = subparsers.add_parser("download", help="Download datasets")
    dl_group = dl_parser.add_mutually_exclusive_group(required=True)
    dl_group.add_argument("--id", type=int, nargs="+", help="Dataset ID(s) to download")
    dl_group.add_argument("--index", type=int, nargs="+", help="Dataset index(es) to download (1-based)")
    dl_group.add_argument("--all", action="store_true", help="Download all datasets")
    dl_parser.add_argument("--no-azcopy", action="store_true", help="Use requests instead of azcopy")
    dl_parser.set_defaults(func=cmd_download)

    # Search command
    search_parser = subparsers.add_parser("search", help="Search datasets by keyword")
    search_parser.add_argument("keyword", help="Search keyword")
    search_parser.set_defaults(func=cmd_search)

    args = parser.parse_args()

    # Handle classification=-1 as None
    if args.classification == -1:
        args.classification = None

    # Show help if no command provided
    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
