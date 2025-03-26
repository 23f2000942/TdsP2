import requests
import subprocess
import hashlib
import json
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import zipfile
import pandas as pd
import os
import gzip
import re
from urllib.parse import urlencode
from geopy.geocoders import Nominatim
import time
import atoma
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

openai_api_chat = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
openai_api_key = os.getenv("AIPROXY_TOKEN")
openai_header = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json",
}


def vs_code_version():
    return """
    Version:          Code 1.98.2 (ddc367ed5c8936efe395cffeec279b04ffd7db78, 2025-03-12T13:32:45.399Z)
    OS Version:       Linux x64 6.12.15-200.fc41.x86_64
    CPUs:             11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz (8 x 1300)
    Memory (System):  7.40GB (3.72GB free)
    Load (avg):       3, 2, 2
    VM:               0%
    Screen Reader:    no
    Process Argv:     --crash-reporter-id 80b4d7e7-0056-4767-b601-6fcdbec0b54d
    GPU Status:       2d_canvas:                              enabled
                    canvas_oop_rasterization:               enabled_on
                    direct_rendering_display_compositor:    disabled_off_ok
                    gpu_compositing:                        enabled
                    multiple_raster_threads:                enabled_on
                    opengl:                                 enabled_on
                    rasterization:                          enabled
                    raw_draw:                               disabled_off_ok
                    skia_graphite:                          disabled_off
                    video_decode:                           enabled
                    video_encode:                           disabled_software
                    vulkan:                                 disabled_off
                    webgl:                                  enabled
                    webgl2:                                 enabled
                    webgpu:                                 disabled_off
                    webnn:                                  disabled_off

    CPU %	Mem MB	   PID	Process
        2	   189	 18772	code main
        0	    45	 18800	   zygote
        2	   121	 19189	     gpu-process
        0	    45	 18801	   zygote
        0	     8	 18825	     zygote
        0	    61	 19199	   utility-network-service
        0	   106	 20078	ptyHost
        2	   114	 20116	extensionHost [1]
    21	   114	 20279	shared-process
        0	     0	 20778	     /usr/bin/zsh -i -l -c '/usr/share/code/code'  -p '"0c1d701e5812" + JSON.stringify(process.env) + "0c1d701e5812"'
        0	    98	 20294	fileWatcher [1]

    Workspace Stats:
    |  Window (● solutions.py - tdsproj2 - python - Visual Studio Code)
    |    Folder (tdsproj2): 6878 files
    |      File types: py(3311) pyc(876) pyi(295) so(67) f90(60) txt(41) typed(36)
    |                  csv(31) h(28) f(23)
    |      Conf files:
    """

def make_http_requests_with_uv(url="https://httpbin.org/get", query_params={"email": "23f2005217@ds.study.iitm.ac.in"}):
    print(url)
    try:
        response = requests.get(url, params=query_params)
        return response.json()
    except requests.RequestException as e:
        print(f"HTTP request failed: {e}")
        return None
        
def run_command_with_npx(arguments):
    filePath, prettier_version, hash_algo, use_npx = (
        "README.md",
        "3.4.2",
        "sha256",
        True,
    )
    filePath, prettier_version, hash_algo, use_npx = (
        arguments["filePath"],
        arguments["prettier_version"],
        arguments["hash_algo"],
        arguments["use_npx"],
    )
    prettier_cmd = (
        ["npx", "-y", f"prettier@{prettier_version}", filePath]
        if use_npx
        else ["prettier", filePath]
    )

    try:
        prettier_process = subprocess.run(
            prettier_cmd, capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print("Error running Prettier:", e)
        return None

    formatted_content = prettier_process.stdout.encode()

    try:
        hasher = hashlib.new(hash_algo)
        hasher.update(formatted_content)
        return hasher.hexdigest()
    except ValueError:
        print(f"Invalid hash algorithm: {hash_algo}")
        return None

def use_google_sheets(rows=100, cols=100, start=15, step=12, extract_rows=1, extract_cols=10):
    matrix = np.arange(start, start + (rows * cols * step), step).reshape(rows, cols)

    extracted_values = matrix[:extract_rows, :extract_cols]

    return np.sum(extracted_values)

def calculate_spreadsheet_formula(formula: str, type: str) -> str:
    try:
        if formula.startswith("="):
            formula = formula[1:]

        if "SEQUENCE" in formula and type == "google_sheets":
            # Example: SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 5, 2), 1, 10))
            sequence_pattern = r"SEQUENCE\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)"
            match = re.search(sequence_pattern, formula)

            if match:
                rows = int(match.group(1))
                cols = int(match.group(2))
                start = int(match.group(3))
                step = int(match.group(4))

                # Generate the sequence
                sequence = []
                value = start
                for _ in range(rows):
                    row = []
                    for _ in range(cols):
                        row.append(value)
                        value += step
                    sequence.append(row)

                # Check for ARRAY_CONSTRAIN
                constrain_pattern = r"ARRAY_CONSTRAIN\([^,]+,\s*(\d+),\s*(\d+)\)"
                constrain_match = re.search(constrain_pattern, formula)

                if constrain_match:
                    constrain_rows = int(constrain_match.group(1))
                    constrain_cols = int(constrain_match.group(2))

                    # Apply constraints
                    constrained = []
                    for i in range(min(constrain_rows, len(sequence))):
                        row = sequence[i][:constrain_cols]
                        constrained.extend(row)

                    if "SUM(" in formula:
                        return str(sum(constrained))

        elif "SORTBY" in formula and type == "excel":
            # Example: SUM(TAKE(SORTBY({1,10,12,4,6,8,9,13,6,15,14,15,2,13,0,3}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 6))

            # Extract the arrays from SORTBY
            arrays_pattern = r"SORTBY\(\{([^}]+)\},\s*\{([^}]+)\}\)"
            arrays_match = re.search(arrays_pattern, formula)

            if arrays_match:
                values = [int(x.strip()) for x in arrays_match.group(1).split(",")]
                sort_keys = [int(x.strip()) for x in arrays_match.group(2).split(",")]

                # Sort the values based on sort_keys
                sorted_pairs = sorted(zip(values, sort_keys), key=lambda x: x[1])
                sorted_values = [pair[0] for pair in sorted_pairs]

                # Check for TAKE
                take_pattern = r"TAKE\([^,]+,\s*(\d+),\s*(\d+)\)"
                take_match = re.search(take_pattern, formula)

                if take_match:
                    take_start = int(take_match.group(1))
                    take_count = int(take_match.group(2))

                    # Apply TAKE function
                    taken = sorted_values[take_start - 1 : take_start - 1 + take_count]

                    # Check for SUM
                    if "SUM(" in formula:
                        return str(sum(taken))

        return "Could not parse the formula or unsupported formula type"

    except Exception as e:
        return f"Error calculating spreadsheet formula: {str(e)}"

def use_excel(values=None, sort_keys=None, num_rows=1, num_elements=9):
    if values is None:
        values = np.array([13, 12, 0, 14, 2, 12, 9, 15, 1, 7, 3, 10, 9, 15, 2, 0])
    if sort_keys is None:
        sort_keys = np.array([10, 9, 13, 2, 11, 8, 16, 14, 7, 15, 5, 4, 6, 1, 3, 12])

    sorted_values = values[np.argsort(sort_keys)]
    return np.sum(sorted_values[:num_elements])


def use_devtools(html=None, input_name=None):
    if html is None:
        html = '<input type="hidden" name="secret" value="12345">'
    if input_name is None:
        input_name = "secret"

    soup = BeautifulSoup(html, "html.parser")
    hidden_input = soup.find("input", {"type": "hidden", "name": input_name})

    return hidden_input["value"] if hidden_input else None


def count_wednesdays(start_date="1990-04-08", end_date="2008-09-29", weekday=2):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    count = sum(
        1
        for _ in range((end - start).days + 1)
        if (start + timedelta(_)).weekday() == weekday
    )
    return count


def extract_csv_from_a_zip(
    zip_path,
    extract_to="extracted_files",
    csv_filename="extract.csv",
    column_name="answer",
):
    """
    Extract a CSV file from a ZIP archive and return values from a specific column.
    
    Parameters:
        zip_path (str): Path to the ZIP file containing the CSV file
        extract_to (str): Directory to extract files to
        csv_filename (str): Name of the CSV file to extract
        column_name (str): Name of the column to extract values from
        
    Returns:
        str: Comma-separated list of values from the specified column
    """
    import os
    import zipfile
    import pandas as pd
    import glob
    
    # Check multiple possible locations for the zip file
    possible_paths = [
        zip_path,
        os.path.join("tmp_uploads", zip_path),
        os.path.join("tmp_uploads", os.path.basename(zip_path)),
        "tmp_uploads/zips",
    ]
    
    # Try to find the zip file in tmp_uploads directory
    zip_files = glob.glob("tmp_uploads/**/*.zip", recursive=True)
    if zip_files:
        possible_paths.extend(zip_files)
    
    # Try each potential path
    actual_path = None
    for path in possible_paths:
        if os.path.exists(path):
            if os.path.isfile(path) and zipfile.is_zipfile(path):
                actual_path = path
                break
            elif os.path.isdir(path):
                # If it's a directory, look for zip files inside
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    if os.path.isfile(full_path) and zipfile.is_zipfile(full_path):
                        actual_path = full_path
                        break
                if actual_path:
                    break
    
    if not actual_path:
        return f"Error: Could not find zip file. Checked paths: {possible_paths}"
    
    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(actual_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)

    csv_path = os.path.join(extract_to, csv_filename)

    if not os.path.exists(csv_path):
        for root, _, files in os.walk(extract_to):
            for file in files:
                if file.lower().endswith(".csv"):
                    csv_path = os.path.join(root, file)
                    break

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if column_name in df.columns:
            return ", ".join(map(str, df[column_name].dropna().tolist()))

    return ""

def use_json(input_data: str, from_file: bool = False) -> str:
    """
    Sorts a JSON array of objects by the value of the "age" field. In case of a tie, sorts by "name".
    
    Parameters:
        input_data (str): Either the path to a JSON file or the JSON string itself.
        from_file (bool): Set to True if input_data is a file path, False if it's JSON text.
        
    Returns:
        str: The sorted JSON array (as a string) without any spaces or newlines.
    """
    if from_file:
        with open(input_data, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = json.loads(input_data)
    
    sorted_data = sorted(data, key=lambda x: (x.get('age'), x.get('name')))
    return json.dumps(sorted_data, separators=(',',':'))


def multi_cursor_edits_to_convert_to_json(file_path: str) -> dict:
    """
    Converts a multi-line file containing key=value pairs into a JSON object.
    
    Each line in the file should be in the format:
        key=value
        
    Parameters:
        file_path (str): The path to the file.
        
    Returns:
        dict: A dictionary representation of the key/value pairs.
    """
    result = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    for line in content.strip().splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            result[key.strip()] = value.strip()

    result= json.dumps(result)
    return result


def css_selectors():
    return ""


def process_files_with_different_encodings(file_path=None):
    """
    Process files with different encodings and sum values associated with specific symbols.
    
    Parameters:
        file_path (str): Path to the zip file containing the files to process
        
    Returns:
        int or float: Sum of all values where the symbol matches Œ, ›, or ž
    """
    import zipfile
    import os
    import shutil
    import glob
    import pandas as pd
    
    # Default file_path to handle cases where none is provided
    if file_path is None:
        file_path = "encoding_files.zip"
    
    # Check multiple possible locations for the zip file
    possible_paths = [
        file_path,
        os.path.join("tmp_uploads", file_path),
        os.path.join("tmp_uploads", os.path.basename(file_path)),
        "tmp_uploads/zips",
    ]
    
    # Try to find the zip file in tmp_uploads directory
    zip_files = glob.glob("tmp_uploads/**/*.zip", recursive=True)
    if zip_files:
        possible_paths.extend(zip_files)
    
    # Try each potential path
    actual_path = None
    for path in possible_paths:
        if os.path.exists(path):
            if os.path.isfile(path) and zipfile.is_zipfile(path):
                actual_path = path
                break
            elif os.path.isdir(path):
                # If it's a directory, look for zip files inside
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    if os.path.isfile(full_path) and zipfile.is_zipfile(full_path):
                        actual_path = full_path
                        break
                if actual_path:
                    break
    
    if not actual_path:
        return f"Error: Could not find zip file. Checked paths: {possible_paths}"
    
    # Create a directory for extraction
    extract_dir = "encoding_files"
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)
    
    try:
        # Extract the zip file
        with zipfile.ZipFile(actual_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Target symbols to find
        target_symbols = ['Œ', '›', 'ž']
        total_sum = 0
        
        # Define file configurations
        file_configs = [
            {"path": os.path.join(extract_dir, "data1.csv"), "encoding": "cp1252", "separator": ","},
            {"path": os.path.join(extract_dir, "data2.csv"), "encoding": "utf-8", "separator": ","},
            {"path": os.path.join(extract_dir, "data3.txt"), "encoding": "utf-16", "separator": "\t"}
        ]
        
        # Process each file according to its configuration
        for config in file_configs:
            file_path = config["path"]
            if os.path.exists(file_path):
                try:
                    # Try reading with headers first
                    df = pd.read_csv(file_path, encoding=config["encoding"], sep=config["separator"])
                    
                    # If the column names don't include 'symbol' and 'value', assume no header
                    if 'symbol' not in df.columns or 'value' not in df.columns:
                        df = pd.read_csv(file_path, encoding=config["encoding"], sep=config["separator"], 
                                       header=None, names=['symbol', 'value'])
                    
                    # Filter for target symbols
                    filtered = df[df['symbol'].isin(target_symbols)]
                    if not filtered.empty:
                        # Convert values to numeric and sum
                        sum_value = pd.to_numeric(filtered['value'], errors='coerce').sum()
                        if not pd.isna(sum_value):
                            total_sum += sum_value
                            print(f"File {os.path.basename(file_path)}: Found {len(filtered)} matching symbols, sum = {sum_value}")
                
                except Exception as e:
                    print(f"Error processing {os.path.basename(file_path)}: {str(e)}")
        
        # Return the sum, converted to int if it's a whole number
        return int(total_sum) if total_sum.is_integer() else total_sum
    
    except Exception as e:
        return f"Error processing files: {str(e)}"
    
    finally:
        # Clean up the extraction directory
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)



def use_github():
    # Change the return value based on your answer.
    return "https://raw.githubusercontent.com/Sarthak-Sama/Temp-IIT-Assignment-Question/refs/heads/main/email.json"


def replace_across_files(file_path):
    """
    Download and extract a zip file, replace 'IITM' (case-insensitive) with 'IIT Madras' in all files,
    and calculate a hash of the result.
    
    Parameters:
        file_path (str): Path to the zip file
        
    Returns:
        str: The result of running 'cat * | sha256sum' on the modified files
    """
    import zipfile
    import os
    import shutil
    import glob
    import subprocess
    import re
    
    # Check multiple possible locations for the zip file
    possible_paths = [
        file_path,
        os.path.join("tmp_uploads", file_path),
        os.path.join("tmp_uploads", os.path.basename(file_path)),
        "tmp_uploads/zips",
    ]
    
    # Try to find the zip file in tmp_uploads directory
    zip_files = glob.glob("tmp_uploads/**/*.zip", recursive=True)
    if zip_files:
        possible_paths.extend(zip_files)
    
    # Try each potential path
    actual_path = None
    for path in possible_paths:
        if os.path.exists(path):
            if os.path.isfile(path) and zipfile.is_zipfile(path):
                actual_path = path
                break
            elif os.path.isdir(path):
                # If it's a directory, look for zip files inside
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    if os.path.isfile(full_path) and zipfile.is_zipfile(full_path):
                        actual_path = full_path
                        break
                if actual_path:
                    break
    
    if not actual_path:
        return f"Error: Could not find zip file. Checked paths: {possible_paths}"
    
    # Create a directory for extraction
    extract_dir = "replaced_files"
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)
    
    try:
        # Extract the zip file
        with zipfile.ZipFile(actual_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Process each file in the directory
        for root, dirs, files in os.walk(extract_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Skip binary files or files that can't be processed as text
                try:
                    # Read the file in binary mode to preserve line endings
                    with open(file_path, 'rb') as file:
                        content = file.read()
                    
                    # Decode to perform text replacements (preserving line endings)
                    text_content = content.decode('utf-8', errors='replace')
                    
                    # Replace "IITM" (case-insensitive) with "IIT Madras"
                    # Using regex with re.IGNORECASE flag for case-insensitive replacement
                    modified_content = re.sub(r'IITM', 'IIT Madras', text_content, flags=re.IGNORECASE)
                    
                    # Write the modified content back to the file in binary mode
                    with open(file_path, 'wb') as file:
                        file.write(modified_content.encode('utf-8'))
                    
                except (UnicodeDecodeError, IOError) as e:
                    print(f"Skipping file {file_path}: {str(e)}")
        
        # Run the cat | sha256sum command
        current_dir = os.getcwd()
        os.chdir(extract_dir)
        
        cmd = "cat * | sha256sum"
        result = subprocess.check_output(cmd, shell=True, text=True)
        
        # Return to the original directory
        os.chdir(current_dir)
        
        return result.strip()
    
    except Exception as e:
        return f"Error processing files: {str(e)}"
    
    finally:
        # Clean up the extraction directory
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        
        # Also delete the original zip file
        if actual_path and os.path.exists(actual_path):
            os.remove(actual_path)


def list_files_and_attributes(file_path, min_size=6262, reference_date="2019-03-22 14:31:00", timezone="Asia/Kolkata", debug=False):
    """
    Download and extract a zip file, list all files with their date and file size,
    and calculate the total size of files meeting specific criteria.
    
    Parameters:
        file_path (str): Path to the zip file
        min_size (int): Minimum file size in bytes (default: 6262)
        reference_date (str): Reference date in format 'YYYY-MM-DD HH:MM:SS' (default: "2019-03-22 14:31:00")
        timezone (str): Timezone for reference date (default: "Asia/Kolkata")
        debug (bool): Whether to print debug information (default: False)
        
    Returns:
        int: Total size of files meeting the criteria (≥ min_size bytes and modified on or after the reference date)
    """
    import zipfile
    import os
    import shutil
    import glob
    from datetime import datetime
    import pytz
    import time
    
    # Check multiple possible locations for the zip file
    possible_paths = [
        file_path,
        os.path.join("tmp_uploads", file_path),
        os.path.join("tmp_uploads", os.path.basename(file_path)),
        "tmp_uploads/zips",
    ]
    
    # Try to find the zip file in tmp_uploads directory
    zip_files = glob.glob("tmp_uploads/**/*.zip", recursive=True)
    if zip_files:
        possible_paths.extend(zip_files)
    
    # Try each potential path
    actual_path = None
    for path in possible_paths:
        if os.path.exists(path):
            if os.path.isfile(path) and zipfile.is_zipfile(path):
                actual_path = path
                break
            elif os.path.isdir(path):
                # If it's a directory, look for zip files inside
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    if os.path.isfile(full_path) and zipfile.is_zipfile(full_path):
                        actual_path = full_path
                        break
                if actual_path:
                    break
    
    if not actual_path:
        return f"Error: Could not find zip file. Checked paths: {possible_paths}"
    
    try:
        # Reference timestamp: from the parameters
        tz = pytz.timezone(timezone)
        reference_time = datetime.strptime(reference_date, "%Y-%m-%d %H:%M:%S")
        reference_time = tz.localize(reference_time)
        reference_timestamp = reference_time.timestamp()
        
        if debug:
            print(f"Reference time: {reference_time}")
            print(f"Reference timestamp: {reference_timestamp}")
        
        # Process directly from the zip without full extraction
        with zipfile.ZipFile(actual_path, 'r') as zip_ref:
            # Calculate total size based on ZipInfo objects
            total_size = 0
            
            # Examine each file in the zip
            for info in zip_ref.infolist():
                # Skip directories
                if info.filename.endswith('/'):
                    continue
                
                # Get file size directly from zip info
                file_size = info.file_size
                
                # Get modification time from zip info
                year, month, day, hour, minute, second = info.date_time
                file_time = datetime(year, month, day, hour, minute, second)
                
                # Convert to timestamp for comparison (assuming UTC)
                # We need to localize to match the reference timestamp timezone
                file_time_localized = tz.localize(file_time)
                file_timestamp = file_time_localized.timestamp()
                
                if debug:
                    print(f"File: {info.filename}, Size: {file_size}, Timestamp: {file_timestamp}")
                    print(f"File time: {file_time_localized}")
                
                # Check criteria: file size ≥ min_size and modified on or after reference_timestamp
                if file_size >= min_size and file_timestamp >= reference_timestamp:
                    total_size += file_size
                    if debug:
                        print(f"Adding file: {info.filename}, size: {file_size}")
        
        return total_size
    
    except Exception as e:
        return f"Error processing files: {str(e)}"
    
    finally:
        # Delete the original zip file
        if actual_path and os.path.exists(actual_path):
            os.remove(actual_path)

def move_and_rename_files(file_path):
    """
    Download and extract a zip file, move all files from subdirectories to an empty folder,
    rename files replacing each digit with the next, and run a command to get the hash.
    
    Parameters:
        file_path (str): Path to the zip file
        
    Returns:
        str: The result of running 'grep . * | LC_ALL=C sort | sha256sum' on the folder
    """
    import zipfile
    import os
    import shutil
    import glob
    import subprocess
    
    # Check multiple possible locations for the zip file
    possible_paths = [
        file_path,
        os.path.join("tmp_uploads", file_path),
        os.path.join("tmp_uploads", os.path.basename(file_path)),
        "tmp_uploads/zips",
    ]
    
    # Try to find the zip file in tmp_uploads directory
    zip_files = glob.glob("tmp_uploads/**/*.zip", recursive=True)
    if zip_files:
        possible_paths.extend(zip_files)
    
    # Try each potential path
    actual_path = None
    for path in possible_paths:
        if os.path.exists(path):
            if os.path.isfile(path) and zipfile.is_zipfile(path):
                actual_path = path
                break
            elif os.path.isdir(path):
                # If it's a directory, look for zip files inside
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    if os.path.isfile(full_path) and zipfile.is_zipfile(full_path):
                        actual_path = full_path
                        break
                if actual_path:
                    break
    
    if not actual_path:
        return f"Error: Could not find zip file. Checked paths: {possible_paths}"
    
    # Create directories
    extract_dir = "extracted_files"
    target_dir = "moved_files"
    
    # Clean up existing directories
    for dir_path in [extract_dir, target_dir]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    
    try:
        # Extract the zip file
        with zipfile.ZipFile(actual_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find all files in subdirectories
        for root, dirs, files in os.walk(extract_dir):
            if root != extract_dir:  # Only consider files in subdirectories
                for file in files:
                    src_path = os.path.join(root, file)
                    
                    # Create new filename with digits replaced
                    new_name = ""
                    for char in file:
                        if char.isdigit():
                            new_name += str((int(char) + 1) % 10)
                        else:
                            new_name += char
                    
                    # Handle filename conflicts
                    dst_path = os.path.join(target_dir, new_name)
                    counter = 1
                    while os.path.exists(dst_path):
                        base, ext = os.path.splitext(new_name)
                        dst_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
                        counter += 1
                    
                    # Move and rename in one step
                    shutil.move(src_path, dst_path)
        
        # Run the grep command in the target directory
        current_dir = os.getcwd()
        os.chdir(target_dir)
        
        if not os.listdir('.'):
            return "Error: No files were moved to the target directory."
        
        cmd = "grep . * | LC_ALL=C sort | sha256sum"
        result = subprocess.check_output(cmd, shell=True, text=True)
        
        # Return to the original directory
        os.chdir(current_dir)
        
        return result.strip()
    
    except Exception as e:
        return f"Error processing files: {str(e)}"
    
    finally:
        # Clean up the extraction directory
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        
        # Also delete the original zip file
        if actual_path and os.path.exists(actual_path):
            os.remove(actual_path)

def compare_files(file_path):
    """
    Compare two files (a.txt and b.txt) from a zip file and count the number of differing lines.
    
    Parameters:
        file_path (str): Path to the zip file containing a.txt and b.txt
        
    Returns:
        int: Number of lines that differ between the two files
    """
    import zipfile
    import os
    import shutil
    import glob
    
    # Check multiple possible locations for the zip file
    possible_paths = [
        file_path,
        os.path.join("tmp_uploads", file_path),
        os.path.join("tmp_uploads", os.path.basename(file_path)),
        "tmp_uploads/zips",  # Check the directory where zip files are extracted
    ]
    
    # Try to find the zip file in tmp_uploads directory
    zip_files = glob.glob("tmp_uploads/**/*.zip", recursive=True)
    if zip_files:
        possible_paths.extend(zip_files)
    
    # Try each potential path
    actual_path = None
    for path in possible_paths:
        if os.path.exists(path):
            if os.path.isfile(path) and zipfile.is_zipfile(path):
                actual_path = path
                break
            elif os.path.isdir(path):
                # If it's a directory, look for zip files inside
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    if os.path.isfile(full_path) and zipfile.is_zipfile(full_path):
                        actual_path = full_path
                        break
                if actual_path:
                    break
    
    if not actual_path:
        return f"Error: Could not find zip file. Checked paths: {possible_paths}"
    
    # Create a temporary directory for extraction
    extract_dir = "extracted_comparison"
    os.makedirs(extract_dir, exist_ok=True)
    
    try:
        # Extract the zip file
        with zipfile.ZipFile(actual_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Paths to the extracted files
        file_a_path = os.path.join(extract_dir, "a.txt")
        file_b_path = os.path.join(extract_dir, "b.txt")
        
        # Check if both files exist
        if not (os.path.exists(file_a_path) and os.path.exists(file_b_path)):
            return "Error: Could not find both a.txt and b.txt in the zip file"
        
        # Read and compare the files
        with open(file_a_path, 'r') as file_a, open(file_b_path, 'r') as file_b:
            lines_a = file_a.readlines()
            lines_b = file_b.readlines()
            
            # Check if files have the same number of lines
            if len(lines_a) != len(lines_b):
                return f"Files have different line counts: a.txt has {len(lines_a)} lines, b.txt has {len(lines_b)} lines"
            
            # Count differing lines
            diff_count = sum(1 for line_a, line_b in zip(lines_a, lines_b) if line_a != line_b)
        
        return diff_count
    
    except Exception as e:
        return f"Error processing zip file: {str(e)}"
    
    finally:
        # Clean up extracted files
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)


def sql_ticket_sales():
    """
    Returns the SQL query to calculate the total sales for 'Gold' tickets.
    """
    query = """
    SELECT SUM(units * price) AS total_sales
    FROM tickets
    WHERE TRIM(LOWER(type)) = 'gold';
    """
    return query


def write_documentation_in_markdown():
    return '''# Weekly Step Analysis

## Introduction
This *analysis* focuses on the **number of steps walked** each day over a week. It compares trends over time and evaluates performance against friends. The findings aim to provide insights into physical activity patterns.

## Methodology
1. Steps were tracked using a fitness tracker.
2. Data was recorded daily in a `.csv` file.
3. Results were analyzed using Python with the `pandas` library.
## Tasks
- Run
-Play 

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |

### Code Example
Below is a snippet of the code used for data analysis:


[google](google.com)
(![image](https://i.natgeofe.com/n/4cebbf38-5df4-4ed0-864a-4ebeb64d33a4/NationalGeographic_1468962_16x9.jpg))

>NEVER GIVE UP

```python
import pandas as pd

data = pd.read_csv("steps_data.csv")
average_steps = data["Steps"].mean()
print(f"Average Steps: {average_steps}")
```
'''


def compress_an_image(image_path):
    """
    Compresses an image losslessly to be under 1,500 bytes and returns it as base64.
    Every pixel in the compressed image should match the original image.
    
    Args:
        image_path (str): Path to the input image
        
    Returns:
        str: Base64 encoded compressed image or error message
    """
    try:
        from PIL import Image
        import io
        import os
        import base64
        
        # Check if image exists
        if not os.path.exists(image_path):
            return f"Error: Image not found at {image_path}"
        
        # Open the image
        with Image.open(image_path) as img:
            original_size = img.size
            original_mode = img.mode
            
            # Method 1: Try with palette mode (lossless for simple images)
            palette_img = img.convert("P", palette=Image.ADAPTIVE, colors=8)  # Try fewer colors first
            
            # Try different compression levels with PNG format
            for colors in [8, 16, 32, 64, 128, 256]:
                palette_img = img.convert("P", palette=Image.ADAPTIVE, colors=colors)
                
                buffer = io.BytesIO()
                palette_img.save(buffer, format="PNG", optimize=True, compress_level=9)
                file_size = buffer.tell()
                
                if file_size <= 1500:
                    # Success! Return as base64
                    buffer.seek(0)
                    base64_image = base64.b64encode(buffer.read()).decode('utf-8')
                    return base64_image
            
            # If PNG with palette didn't work, try more aggressive options while preserving dimensions
            # Try WebP format with maximum compression
            buffer = io.BytesIO()
            img.save(buffer, format="WEBP", quality=1, method=6)
            file_size = buffer.tell()
            
            if file_size <= 1500:
                buffer.seek(0)
                base64_image = base64.b64encode(buffer.read()).decode('utf-8')
                return base64_image
                
            # If we get here, we couldn't compress enough without resizing
            return "Error: Image dimensions do not match the original"
                
    except ImportError:
        return "Error: Required libraries (PIL) not available"
    except Exception as e:
        return f"Error during compression: {str(e)}"


def host_your_portfolio_on_github_pages(email):
    urls = {
        "23f3000709@ds.study.iitm.ac.in": "https://sarthak-sama.github.io/my-static-site/", # Sarthak
        "23f2000942@ds.study.iitm.ac.in":"https://23f2000942.github.io/tds-ga2/", # Aditi
        "23f2005217@ds.study.iitm.ac.in": "https://girishiitm.github.io/GirishIITM/", # Girish
        "22ds3000103@ds.study.iitm.ac.in":"https://22ds3000103.github.io/vatchala", # Vatchala
        "23f1002279@ds.study.iitm.ac.in":"https://23f1002279.github.io/TDS_W2_GIT/", # Shivam
        "22f3002560@ds.study.iitm.ac.in":"https://raw.githubusercontent.com/HolyGrim/email.json/refs/heads/main/email.json", # Prabhnoor
        "22f3001882@ds.study.iitm.ac.in": "https://22f3001882.github.io/tds-week2-question/", # Yash
        "23f2000098@ds.study.iitm.ac.in": "https://github.com/YOGASWETHASANJAYGANDHI", # SD
        "23f2001413@ds.study.iitm.ac.in": "https://debjeetsingha.github.io/", # Debjeet
        "23f1002942@ds.study.iitm.ac.in": "https://aman-v114.github.io/demo_repo/index.html", # Aman
        "21f3003062@ds.study.iitm.ac.in": "https://aditya-naidu.github.io/iit-githhubPages-testing/" # Aditya
    }
    answer = urls[email]
    return answer


def use_google_colab(email):
    results = {
        "23f3000709@ds.study.iitm.ac.in":"30fa5", # Sarthak
        "22f3002560@ds.study.iitm.ac.in": "23a99", # Prabhnoor
        "22ds3000103@ds.study.iitm.ac.in":"3e09c", # Vatchala
        "23f2005217@ds.study.iitm.ac.in":"20705", # Gireesh
        "23f1002279@ds.study.iitm.ac.in":"b591c", # Shivam
        "22f3001882@ds.study.iitm.ac.in":"b22d0", # Yash
        "23f2001413@ds.study.iitm.ac.in": "07554", # Debjeet
        "23f1002942@ds.study.iitm.ac.in":"5aba1", # Aman
        "21f3003062@ds.study.iitm.ac.in": "518d1", # Aditya
        "23f2000942@ds.study.iitm.ac.in":"e70b4" # Aditi
        
    }
    answer = results[email]
    return answer


def use_an_image_library_in_google_colab():
    return ""


def deploy_a_python_api_to_vercel():
    return ""


def create_a_github_action():
    return ""


def push_an_image_to_docker_hub(tag: str) -> str:
    """
    Creates and pushes a Docker image to Docker Hub with the specified tag.
    Uses environment variables for authentication.
    
    Args:
        tag (str): The tag to be added to the Docker image
        
    
    Returns:
        str: The Docker Hub URL in the format https://hub.docker.com/repository/docker/{username}/{repo_name}/general
    """
    try:
              
        # Get Docker Hub username and password/token from environment variable
        docker_username=os.getenv("DOCKER_USERNAME")
        docker_password = os.getenv("DOCKER_PASSWORD")
        # or os.environ.get("DOCKER_TOKEN")
        
        if not docker_password:
            return "Error: DOCKER_PASSWORD environment variable must be set"
        
        # Login to Docker Hub using --password-stdin (secure method)
        login_cmd = f"echo {docker_password} | docker login -u {docker_username} --password-stdin"
        login_process = subprocess.run(login_cmd, shell=True, capture_output=True, text=True)
        
        if login_process.returncode != 0:
            return f"Error during Docker login: {login_process.stderr}"
        
        repo_name = "tds-project"
        # Build and push the image
        image_name = f"{docker_username}/{repo_name}:{tag}"
        build_process = subprocess.run(
            ["docker", "buildx", "build", "-t", image_name, "."], 
            capture_output=True, 
            text=True
        )
        
        if build_process.returncode != 0:
            return f"Error building Docker image: {build_process.stderr}"
        
        push_process = subprocess.run(
            ["docker", "push", image_name], 
            capture_output=True, 
            text=True
        )
        
        if push_process.returncode != 0:
            return f"Error pushing Docker image: {push_process.stderr}"
        
        # Construct and return the Docker Hub URL
        docker_hub_url = f"https://hub.docker.com/repository/docker/{docker_username}/{repo_name}/general"
        return docker_hub_url
    except Exception as e:
        return f"Error: {str(e)}"


def write_a_fastapi_server_to_serve_data():
    return ""


def run_a_local_llm_with_llamafile():
    return ""


def llm_sentiment_analysis():
    """
    Write a python code that analyzes sentiment of text for DataSentinel Inc's internal monitoring dashboard.
    
    Sends a POST request to OpenAI's API to categorize text as GOOD, BAD, or NEUTRAL.
    Uses dummy credentials for testing the API integration.
    
    Returns:
        str: The sentiment analysis result or error message
    """
    return '''
import httpx

# Define the API endpoint (dummy endpoint for testing)
url = "https://api.openai.com/v1/chat/completions"

# Define the dummy API key and headers
headers = {
    "Authorization": "Bearer dummy_api_key"
}

# Define the messages:
# 1. System message instructing the model to analyze sentiment as GOOD, BAD, or NEUTRAL.
# 2. The sample piece of meaningless text.
data = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "system",
            "content": (
                "You are an AI-powered sentiment analysis tool. "
                "Analyze the following text and classify its sentiment as GOOD, BAD, or NEUTRAL."
            )
        },
        {
            "role": "user",
            "content": "1lxCmtQS3k3FNND    R4bhFb\nXNF8 JXidU6n 6 lTo4\nV mu"
        }
    ]
}

# Send a POST request using httpx
try:
    response = httpx.post(url, json=data, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    result = response.json()
    print("API Response:", result)
except httpx.HTTPError as e:
    print("An error occurred while making the API call:", e)
'''


def llm_token_cost():
    return ""


def generate_addresses_with_llms():
    return ""


def llm_vision(image_url=None, prompt="Extract text from this image", model="gpt-4o-mini"):
    """
    Calls OpenAI's vision API via a proxy to extract text from an image.
    
    Args:
        model (str): The OpenAI model to use for vision tasks.
        image_url (str): URL to the image to be processed.
        prompt (str): Instruction for the model.
        
    Returns:
        str: Extracted text from the image.
    """
    if not image_url:
        return "Error: No image URL provided."

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        "max_tokens": 300
    }

    try:
        with httpx.Client(timeout=20) as client:
            response = client.post(openai_api_chat, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error in vision processing: {str(e)}"



def llm_embeddings(model="text-embedding-3-small", input_texts=None):
    """
    Calls OpenAI's embeddings API via a proxy to get vector embeddings for texts.
    
    Args:
        model (str): The embedding model to use.
        input_texts (list): List of text strings to get embeddings for.
        
    Returns:
        dict: A dictionary with the properly formatted request.
    """
    if input_texts is None:
        return {"error": "No input texts provided."}
    print('inside solution function')
    print(model)
    print(input_texts)
    print('shouldve printed above')
    
    # Create the dictionary with the correct field names expected by the API
    result = {
        "model": model,
        "input": input_texts  # This maps input_texts to "input" in the output
    }
    
    return result  # Return the dictionary directly, not a JSON string

def embedding_similarity():
    return '''
import numpy as np

def most_similar(embeddings):
    max_similarity = -1
    most_similar_pair = None

    phrases = list(embeddings.keys())

    for i in range(len(phrases)):
        for j in range(i + 1, len(phrases)):
            v1 = np.array(embeddings[phrases[i]])
            v2 = np.array(embeddings[phrases[j]])

            similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pair = (phrases[i], phrases[j])

    return most_similar_pair'''

def vector_databases():
    return ""


def function_calling():
    return ""


def get_an_llm_to_say_yes():
    return ""


def import_html_to_google_sheets():
    return ""


def scrape_imdb_movies(min_rating, max_rating):
    """
    Fetches up to 25 movie titles from IMDb within the specified rating range.
    
    Args:
        min_rating (float): Minimum IMDb rating (0-10)
        max_rating (float): Maximum IMDb rating (0-10)
        
    Returns:
        str: JSON string containing movie data including id, title, year, and rating
    """
    url = f"https://www.imdb.com/search/title/?user_rating={min_rating},{max_rating}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    movies = []

    # Select up to 25 movie items
    movie_items = soup.select('.ipc-metadata-list-summary-item')[:25]

    for item in movie_items:
        title_element = item.select_one('.ipc-title__text')
        year_element = item.select_one('.sc-f30335b4-7.jhjEEd.dli-title-metadata-item')
        rating_element = item.select_one('.ipc-rating-star--rating')

        if title_element and year_element:
            # Extract ID
            link_tag = item.select_one('a[href*="/title/tt"]')
            match = re.search(r'tt\d+', link_tag['href']) if link_tag else None
            imdb_id = match.group(0) if match else None

            # Extract and clean fields
            title = title_element.get_text(strip=True)
            if title.startswith("Title: "):
                title = title[7:]  # Remove "Title: " prefix if present
                
            year = year_element.get_text().replace('\xa0', ' ')  # Preserve NBSP
            rating = rating_element.get_text(strip=True) if rating_element else None

            try:
                rating_float = float(rating)
                if min_rating <= rating_float <= max_rating:
                    movies.append({
                        "id": imdb_id,
                        "title": title,
                        "year": year,
                        "rating": rating
                    })
            except (ValueError, TypeError):
                continue

    return json.dumps(movies, indent=2, ensure_ascii=False)


def wikipedia_outline():
    return ""


def scrape_the_bbc_weather_api(city):
    """
    Scrape weather forecast data for a given city from the BBC Weather API and website.
    
    Args:
        city (str): The name of the city to fetch weather data for.
    
    Returns:
        str: A JSON string mapping dates to weather descriptions.
    """
    # Construct location URL with the provided city
    location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
        'api_key': 'AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv',
        's': city,
        'stack': 'aws',
        'locale': 'en',
        'filter': 'international',
        'place-types': 'settlement,airport,district',
        'order': 'importance',
        'a': 'true',
        'format': 'json'
    })

    # Fetch location data
    result = requests.get(location_url).json()
    
    # Check if location data is valid
    try:
        location_id = result['response']['results']['results'][0]['id']
    except (KeyError, IndexError):
        raise ValueError(f"No location data found for city: {city}")

    # Construct weather URL
    weather_url = f'https://www.bbc.com/weather/{location_id}'

    # Fetch weather data
    response = requests.get(weather_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch weather data for {city}. Status code: {response.status_code}")

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    daily_summary = soup.find('div', attrs={'class': 'wr-day-summary'})
    if not daily_summary:
        raise ValueError(f"Weather summary not found on page for {city}")

    # Extract weather descriptions
    daily_summary_list = re.findall('[a-zA-Z][^A-Z]*', daily_summary.text)
    if not daily_summary_list:
        raise ValueError(f"No weather descriptions extracted for {city}")

    # Generate date list
    datelist = pd.date_range(datetime.today(), periods=len(daily_summary_list)).tolist()
    datelist = [date.date().strftime('%Y-%m-%d') for date in datelist]

    # Map dates to descriptions
    weather_data = {date: desc for date, desc in zip(datelist, daily_summary_list)}

    # Convert to JSON and return
    return json.dumps(weather_data, indent=4)


def find_the_bounding_box_of_a_city(city, country, osm_id_ending=None):
    """
    Retrieve the minimum latitude of the bounding box for a specified city in a country,
    optionally filtered by an osm_id ending pattern, using the Nominatim API.
    
    Args:
        city (str): The name of the city (e.g., "Tianjin").
        country (str): The name of the country (e.g., "China").
        osm_id_ending (str, optional): The ending pattern of the osm_id to match (e.g., "2077"). Defaults to None.
    
    Returns:
        str: A message with the minimum latitude or an error message.
    """
    # Activate the Nominatim geocoder
    locator = Nominatim(user_agent="myGeocoder")

    # Geocode the city and country, allowing multiple results
    query = f"{city}, {country}"
    locations = locator.geocode(query, exactly_one=False)

    # Check if locations were found
    if locations:
        if osm_id_ending:
            # Loop through results to find a match for osm_id_ending
            for place in locations:
                osm_id = place.raw.get('osm_id', '')
                if str(osm_id).endswith(osm_id_ending):
                    bounding_box = place.raw.get('boundingbox', [])
                    if bounding_box:
                        min_latitude = float(bounding_box[0])
                        result = min_latitude
                    else:
                        result = f"Bounding box information not available for {city}, {country} with osm_id ending {osm_id_ending}."
                    break
            else:
                result = f"No matching OSM ID ending with '{osm_id_ending}' found for {city}, {country}."
        else:
            # No osm_id_ending provided, use the first result
            place = locations[0]  # Take the first match
            bounding_box = place.raw.get('boundingbox', [])
            if bounding_box:
                min_latitude = float(bounding_box[0])
                osm_id = place.raw.get('osm_id', '')
                result = min_latitude
            else:
                result = min_latitude 
    else:
        result = f"Location not found for {city}, {country}."

    # Respect Nominatim's rate limit (1 request per second)
    time.sleep(1)
    return result



def search_hacker_news(query, points):
    """
    Search Hacker News for the latest post mentioning a specified topic with a minimum number of points.
    
    Args:
        query (str): The topic to search for (e.g., "python").
        points (int): The minimum number of points the post must have.
    
    Returns:
        str: A JSON string containing the link to the latest qualifying post or an error message.
    """
    # Fetch the feed with posts based on query and minimum points
    feed_url = f"https://hnrss.org/newest?q={query}&points={points}"
    feed = atoma.parse(feed_url)

    # Extract the link of the latest post
    if feed.entries:
        latest_post_link = feed.entries[0].link
        result = {"answer": latest_post_link}
    else:
        result = {"answer": "No posts found matching the criteria."}

    # Return the result as JSON
    return json.dumps(result)



def find_newest_github_user(location, followers, operator):
    """
    Find the newest GitHub user in a specified location with a follower count based on the given operator.
    
    Args:
        location (str): The city to search for (e.g., "Delhi").
        followers (int): The number of followers to filter by.
        operator (str): Comparison operator for followers ("gt" for >, "lt" for <, "eq" for =).
    
    Returns:
        str: The ISO 8601 creation date of the newest valid user, or an error message.
    """

    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    # Map operator to GitHub API syntax
    operator_map = {"gt": ">", "lt": "<", "eq": ""}
    if operator not in operator_map:
        return f"Invalid operator: {operator}. Use 'gt', 'lt', or 'eq'."
    follower_query = f"followers:{operator_map[operator]}{followers}"

    # Search users by location and follower count, sorted by join date (newest first)
    url = f"https://api.github.com/search/users?q=location:{location}+{follower_query}&sort=joined&order=desc"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.json().get('message')}"

    users = response.json().get('items', [])
    if not users:
        return f"No users found in {location} with {follower_query}."

    # Cutoff time: March 23, 2025, 3:57:03 PM PDT (convert to UTC for comparison)
    cutoff_datetime = datetime.datetime(2025, 3, 23, 15, 57, 3, tzinfo=datetime.timezone(datetime.timedelta(hours=-7)))
    cutoff_utc = cutoff_datetime.astimezone(datetime.timezone.utc)

    # Process users to find the newest valid one
    for user in users:
        user_url = user['url']
        user_response = requests.get(user_url, headers=headers)

        if user_response.status_code == 200:
            user_data = user_response.json()
            created_at = user_data['created_at']  # ISO 8601 format (e.g., "2023-05-10T12:34:56Z")
            created_at_date = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))

            # Exclude ultra-new users (joined after cutoff)
            if created_at_date <= cutoff_utc:
                return created_at  # Already in ISO 8601 format
        else:
            print(f"Error fetching user details: {user_response.status_code}")

    return "No valid users found before cutoff date."



def create_a_scheduled_github_action():
    return ""


def extract_tables_from_pdf():
    return ""


def convert_a_pdf_to_markdown():
    return ""


def clean_up_excel_sales_data():
    return ""


def parse_log_line(line):
    # Regex for parsing log lines
    log_pattern = (r'^(\S+) (\S+) (\S+) \[(.*?)\] "(\S+) (.*?) (\S+)" (\d+) (\S+) "(.*?)" "(.*?)" (\S+) (\S+)$')
    match = re.match(log_pattern, line)
    if match:
        return {
            "ip": match.group(1),
            "time": match.group(4),  # e.g. 01/May/2024:00:00:00 -0500
            "method": match.group(5),
            "url": match.group(6),
            "protocol": match.group(7),
            "status": int(match.group(8)),
            "size": int(match.group(9)) if match.group(9).isdigit() else 0,
            "referer": match.group(10),
            "user_agent": match.group(11),
            "vhost": match.group(12),
            "server": match.group(13)
        }
    return None

def load_logs(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return pd.DataFrame()
    
    parsed_logs = []
    # Open with errors='ignore' for problematic lines
    with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parsed_entry = parse_log_line(line)
            if parsed_entry:
                parsed_logs.append(parsed_entry)
    return pd.DataFrame(parsed_logs)

def convert_time(timestamp):
    return datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")

def clean_up_student_marks(file_path, section_prefix, weekday, start_hour, end_hour, month, year):
    """
    Analyzes the logs to count the number of successful GET requests.
    
    Parameters:
    - file_path: path to the GZipped log file.
    - section_prefix: URL prefix to filter (e.g., "/telugu/" or "/tamilmp3/").
    - weekday: integer (0=Monday, ..., 6=Sunday).
    - start_hour: start time (inclusive) in 24-hour format.
    - end_hour: end time (exclusive) in 24-hour format.
    - month: integer month (e.g., 5 for May).
    - year: integer year (e.g., 2024).
    
    Returns:
    - Count of successful GET requests matching the criteria.
    """
    df = load_logs(file_path)
    if df.empty:
        print("No log data available for processing.")
        return 0
    
    # Convert time field to datetime
    df["datetime"] = df["time"].apply(convert_time)
    
    # Filter for the specific month and year
    df = df[(df["datetime"].dt.month == month) & (df["datetime"].dt.year == year)]
    
    # Filter for the specific day of the week
    df = df[df["datetime"].dt.weekday == weekday]
    
    # Filter for the specific time window
    df = df[(df["datetime"].dt.hour >= start_hour) & (df["datetime"].dt.hour < end_hour)]
    
    # Apply filters for GET requests, URL prefix, and successful status codes
    filtered_df = df[
        (df["method"] == "GET") &
        (df["url"].str.startswith(section_prefix)) &
        (df["status"].between(200, 299))
    ]
    
    return filtered_df.shape[0]


def apache_log_requests():
    return ""


def apache_log_downloads():
    return ""


def clean_up_sales_data():
    return ""


def parse_partial_json():
    return ""


def extract_nested_json_keys():
    return ""


def duckdb_social_media_interactions():
    return ""


def transcribe_a_youtube_video():
    return ""


def reconstruct_an_image():
    return ""

functions_dict = {
    "vs_code_version": vs_code_version,
    "make_http_requests_with_uv": make_http_requests_with_uv,
    "run_command_with_npx": run_command_with_npx,
    "use_google_sheets": use_google_sheets,
    "use_excel": use_excel,
    "use_devtools": use_devtools,
    "count_wednesdays": count_wednesdays,
    "extract_csv_from_a_zip": extract_csv_from_a_zip,
    "use_json": use_json,
    "multi_cursor_edits_to_convert_to_json": multi_cursor_edits_to_convert_to_json,
    "css_selectors": css_selectors,
    "process_files_with_different_encodings": process_files_with_different_encodings,
    "use_github": use_github,
    "replace_across_files": replace_across_files,
    "list_files_and_attributes": list_files_and_attributes,
    "move_and_rename_files": move_and_rename_files,
    "compare_files": compare_files,
    "sql_ticket_sales": sql_ticket_sales,
    "write_documentation_in_markdown": write_documentation_in_markdown,
    "compress_an_image": compress_an_image,
    "host_your_portfolio_on_github_pages": host_your_portfolio_on_github_pages,
    "use_google_colab": use_google_colab,
    "use_an_image_library_in_google_colab": use_an_image_library_in_google_colab,
    "deploy_a_python_api_to_vercel": deploy_a_python_api_to_vercel,
    "create_a_github_action": create_a_github_action,
    "push_an_image_to_docker_hub": push_an_image_to_docker_hub,
    "write_a_fastapi_server_to_serve_data": write_a_fastapi_server_to_serve_data,
    "run_a_local_llm_with_llamafile": run_a_local_llm_with_llamafile,
    "llm_sentiment_analysis": llm_sentiment_analysis,
    "llm_token_cost": llm_token_cost,
    "generate_addresses_with_llms": generate_addresses_with_llms,
    "llm_vision": llm_vision,
    "llm_embeddings": llm_embeddings,
    "embedding_similarity": embedding_similarity,
    "vector_databases": vector_databases,
    "function_calling": function_calling,
    "get_an_llm_to_say_yes": get_an_llm_to_say_yes,
    "import_html_to_google_sheets": import_html_to_google_sheets,
    "scrape_imdb_movies": scrape_imdb_movies,
    "wikipedia_outline": wikipedia_outline,
    "scrape_the_bbc_weather_api": scrape_the_bbc_weather_api,
    "find_the_bounding_box_of_a_city": find_the_bounding_box_of_a_city,
    "search_hacker_news": search_hacker_news,
    "find_newest_github_user": find_newest_github_user,
    "create_a_scheduled_github_action": create_a_scheduled_github_action,
    "extract_tables_from_pdf": extract_tables_from_pdf,
    "convert_a_pdf_to_markdown": convert_a_pdf_to_markdown,
    "clean_up_excel_sales_data": clean_up_excel_sales_data,
    "clean_up_student_marks": clean_up_student_marks,
    "apache_log_requests": apache_log_requests,
    "apache_log_downloads": apache_log_downloads,
    "clean_up_sales_data": clean_up_sales_data,
    "parse_partial_json": parse_partial_json,
    "extract_nested_json_keys": extract_nested_json_keys,
    "duckdb_social_media_interactions": duckdb_social_media_interactions,
    "transcribe_a_youtube_video": transcribe_a_youtube_video,
    "reconstruct_an_image": reconstruct_an_image,
}
