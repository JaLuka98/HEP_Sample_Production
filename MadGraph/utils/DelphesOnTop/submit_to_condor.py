import os
import subprocess
from pathlib import Path

def extract_process_name(directory):
    # Extract the last component of the directory path
    return Path(directory).parts[-2]

def create_condor_submit_script(index, hepmc_gz_file, process_directory):
    hepmc_stem = Path(hepmc_gz_file).stem
    condor_submit_script_content = f"""
executable = ./condor_run.sh
arguments = {hepmc_gz_file}
output = {process_directory}/{hepmc_stem}_{index}.out
error = {process_directory}/{hepmc_stem}_{index}.err
log = {process_directory}/{hepmc_stem}_{index}.log
request_memory = 12GB
queue
"""
# The typical 50k zcat Delphes run only takes max 9GB memory, but just to stay safe, we request 12GB to avoid that our jobs get killed
    condor_submit_script_path = f"{process_directory}/condor_submit_{hepmc_stem}_{index}.submit"
    with open(condor_submit_script_path, 'w') as script_file:
        script_file.write(condor_submit_script_content)
    return condor_submit_script_path

def create_condor_run_script(hepmc_gz_file):
    hepmc_stem = Path(hepmc_gz_file).stem
    condor_run_script_content = f"""
#!/bin/bash

# Set up the environment
source /net/scratch_cms3a/spaeh/private/Software/MadGraph_v3_AL9/setup_MG5.sh

# Run the Python script
python ./run_delphes_on_top.py $1
"""

    condor_run_script_path = f"./condor_run.sh"
    with open(condor_run_script_path, 'w') as script_file:
        script_file.write(condor_run_script_content)
    
    # Ensure the script is executable
    os.chmod(condor_run_script_path, 0o755)

    return condor_run_script_path

def submit_condor_job(condor_submit_script):
    subprocess.run(f"condor_submit {condor_submit_script}", shell=True)

def process_directory(directory):
    # Find all HepMC.gz files in the specified directory and its subdirectories
    hepmc_files = [str(file) for file in Path(directory).rglob('*.hepmc.gz')]

    # Extract the process name from the directory path
    process_name = extract_process_name(directory)

    # Create a dedicated directory for HTCondor files
    condor_files_directory = f"./condor_files_{process_name}"
    os.makedirs(condor_files_directory, exist_ok=True)

    # Create a common bash script for running Delphes
    condor_run_script = create_condor_run_script(hepmc_files[0])

    # Process each HepMC.gz file
    for index, hepmc_gz_file in enumerate(hepmc_files, start=1):
        # Create a unique HTCondor submit script for each file
        condor_submit_script = create_condor_submit_script(index, hepmc_gz_file, condor_files_directory)

        # Submit the HTCondor job
        submit_condor_job(condor_submit_script)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Submit HTCondor jobs to process HepMC.gz files in multiple directories.")
    parser.add_argument("directories", nargs='+', help="Directories containing HepMC.gz files.")
    args = parser.parse_args()

    for directory in args.directories:
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist.")
        else:
            process_directory(directory)