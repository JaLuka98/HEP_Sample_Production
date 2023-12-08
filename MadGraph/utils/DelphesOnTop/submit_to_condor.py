import os
import subprocess
from pathlib import Path

def create_condor_submit_script(index, hepmc_gz_file):
    hepmc_stem = Path(hepmc_gz_file).stem
    condor_submit_script_content = f"""
executable = ./run_delphes_on_top.py
arguments = {hepmc_gz_file}
output = {hepmc_stem}_{index}_out.log
error = {hepmc_stem}_{index}_err.log
log = {hepmc_stem}_{index}_condor.log
queue
"""
    condor_submit_script_path = f"condor_submit_{hepmc_stem}_{index}.submit"
    with open(condor_submit_script_path, 'w') as script_file:
        script_file.write(condor_submit_script_content)
    return condor_submit_script_path

def submit_condor_job(condor_submit_script):
    subprocess.run(f"condor_submit {condor_submit_script}", shell=True)

def main(directory):
    # Find all HepMC.gz files in the specified directory and its subdirectories
    hepmc_files = [str(file) for file in Path(directory).rglob('*.hepmc.gz')]

    # Process each HepMC.gz file
    for index, hepmc_gz_file in enumerate(hepmc_files, start=1):
        # Create a unique HTCondor submit script for each file
        condor_submit_script = create_condor_submit_script(index, hepmc_gz_file)

        # Submit the HTCondor job
        submit_condor_job(condor_submit_script)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Submit HTCondor jobs to process HepMC.gz files.")
    parser.add_argument("directory", help="Directory containing HepMC.gz files.")
    args = parser.parse_args()

    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
    else:
        main(args.directory)