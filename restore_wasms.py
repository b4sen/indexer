import argparse
import sys
import os
import subprocess

def parse_wasm_filename(filename):
    # Filename format: <wasm-name>@<wasm-version>.wasm
    if not filename.endswith(".wasm"):
        return None, None
    
    base = filename[:-5]  # remove .wasm
    if "@" not in base:
        return None, None
    
    # Split from the right to handle names that might contain '@'
    name, version = base.rsplit("@", 1)
    return name, version

def run_publish(file_path, wasm_name, wasm_version, source_account):
    print(f"  Publishing {wasm_name}@{wasm_version}...")
    cmd = [
        "stellar", "registry", "publish",
        "--wasm", file_path,
        "--wasm-name", wasm_name,
        "--binver", wasm_version,
        "--source-account", source_account
    ]
    
    try:
        # Execute the publish command and capture output for logging
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"    Success.")
        else:
            print(f"    Error publishing: {result.stderr.strip()}")
    except Exception as e:
        print(f"    Failed to execute command: {e}")

def main():
    parser = argparse.ArgumentParser(
        description=(
            "utility to restore registry wasms after testnet reset. "
            "Pass --target-directory with directory created by save_wasms.py and optionally "
            "use env variable 'STELLAR_REGISTRY_CONTRACT_ID' to override registry contract id"
        )
    )
    
    parser.add_argument(
        "--target-directory", 
        help="Directory to be processed", 
        required=True
    )

    parser.add_argument(
        "--source-account",
        help="Source account for the publish transaction",
        required=True
    )

    args = parser.parse_args()
    target_dir = args.target_directory
    source_account = args.source_account

    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a directory.")
        sys.exit(1)

    # Check for Registry Contract ID override from environment
    registry_id = os.environ.get("STELLAR_REGISTRY_CONTRACT_ID", None)
    if registry_id:
        print(f"Using Registry Contract ID from env: {registry_id}")
    
    print(f"Target directory set to: {target_dir}")
    print(f"Source account set to: {source_account}")

    # 1. Process root directory WASMs (Main Channel)
    print("\nProcessing root directory WASMs...")
    root_files = [f for f in os.listdir(target_dir) if f.endswith(".wasm") and os.path.isfile(os.path.join(target_dir, f))]
    for filename in sorted(root_files):
        name, version = parse_wasm_filename(filename)
        if name and version:
            file_path = os.path.join(target_dir, filename)
            run_publish(file_path, name, version, source_account)
        else:
            print(f"  Skipping invalid filename: {filename}")

    # 2. Process 'unverified' directory WASMs (Unverified Channel)
    unverified_dir = os.path.join(target_dir, "unverified")
    if os.path.isdir(unverified_dir):
        print("\nProcessing 'unverified' directory WASMs...")
        unverified_files = [f for f in os.listdir(unverified_dir) if f.endswith(".wasm") and os.path.isfile(os.path.join(unverified_dir, f))]
        for filename in sorted(unverified_files):
            name, version = parse_wasm_filename(filename)
            if name and version:
                file_path = os.path.join(unverified_dir, filename)
                # Ensure the name is prepended with 'unverified/'
                full_name = f"unverified/{name}"
                run_publish(file_path, full_name, version, source_account)
            else:
                print(f"  Skipping invalid filename: {filename}")
    else:
        print("\n'unverified' directory not found, skipping.")

if __name__ == "__main__":
    main()
