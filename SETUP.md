# Windows Setup Guide

Instructions for setting up the required tools on Windows.

---

## 1. Python

### Option A: Microsoft Store (Recommended for beginners)

1. Open Microsoft Store
2. Search for "Python 3.12" (or latest version)
3. Click **Get** to install
4. Verify installation:
   ```
   py --version
   ```

### Option B: Official Installer

1. Download from https://www.python.org/downloads/windows/
2. Run installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```
   python --version
   ```

### Install Required Packages

```
py -3 -m pip install fiona geopandas matplotlib folium flask
```

---

## 2. 7-Zip

### Installation

1. Download from https://www.7-zip.org/download.html
2. Choose the 64-bit Windows x64 installer (.exe)
3. Run installer (default path: `C:\Program Files\7-Zip\`)

### Add to PATH (Optional)

1. Open **Settings** > **System** > **About** > **Advanced system settings**
2. Click **Environment Variables**
3. Under **System variables**, find **Path** and click **Edit**
4. Click **New** and add: `C:\Program Files\7-Zip`
5. Click **OK** to save

### Usage

If added to PATH:
```
7z x archive.zip -o./output/
```

If not added to PATH:
```
"C:\Program Files\7-Zip\7z.exe" x archive.zip -o./output/
```

### Common Commands

| Command | Description |
|---------|-------------|
| `7z x archive.zip` | Extract with full paths |
| `7z e archive.zip` | Extract flat (no folders) |
| `7z l archive.zip` | List contents |
| `-o./output/` | Specify output directory |
| `-y` | Assume yes to all prompts |

---

## 3. AzCopy

### Installation

1. Download from https://aka.ms/downloadazcopy-v10-windows
2. Extract the ZIP file
3. Move `azcopy.exe` to a permanent location (e.g., `C:\Tools\azcopy\`)

### Add to PATH

1. Open **Settings** > **System** > **About** > **Advanced system settings**
2. Click **Environment Variables**
3. Under **System variables**, find **Path** and click **Edit**
4. Click **New** and add: `C:\Tools\azcopy` (or your chosen location)
5. Click **OK** to save
6. Restart terminal

### Verify Installation

```
azcopy --version
```

### Usage

```
azcopy copy "<SOURCE_URL>" "<DESTINATION>"
```

### Common Commands

| Command | Description |
|---------|-------------|
| `azcopy copy "url" .` | Download to current directory |
| `azcopy copy "url" ./folder/` | Download to specific folder |
| `azcopy jobs list` | List active/recent jobs |
| `azcopy jobs resume <job-id>` | Resume failed download |

### Troubleshooting

- **Firewall issues**: Ensure outbound HTTPS (443) is allowed
- **Token expired**: SAS tokens are time-limited; fetch a fresh URL
- **Resume failed transfer**: Use `azcopy jobs resume <job-id>`

---

## Verification Checklist

Run these commands to verify all tools are installed:

```
py --version
```
Expected: `Python 3.x.x`

```
"C:\Program Files\7-Zip\7z.exe" --help
```
Expected: 7-Zip help text

```
azcopy --version
```
Expected: `azcopy version 10.x.x`

---

## Quick Start

After setup, run the workflow:

```bash
# 1. Download dataset list
curl -H "Accept: application/json" "https://datahub.pleio.nl/api/v1/files/?limit=25&classification=4" -o datasets.json

# 2. Get download URL for a specific file (replace <ID>)
curl -s "https://datahub.pleio.nl/api/v1/files/<ID>/download/"

# 3. Download using azcopy (paste URL from step 2)
azcopy copy "<URL>" .

# 4. Extract archive
"C:\Program Files\7-Zip\7z.exe" x archive.zip -o./data-extracted/ -y

# 5. Run inventory script
py -3 gdb_inventory.py

# 6. Start dashboard
py -3 infrastructure_dashboard.py
```

---

## Optional: Windows Terminal

For a better command-line experience:

1. Install from Microsoft Store: search "Windows Terminal"
2. Supports tabs, split panes, and better font rendering
3. Works with PowerShell, CMD, and WSL
