#!/usr/bin/env python

import argparse
import subprocess
import os

def unpack_hepmc(hepmc_gz_file):
    hepmc_file = hepmc_gz_file.replace(".gz", "")
    subprocess.run(f"zcat {hepmc_gz_file} > {hepmc_file}", shell=True)
    print(f"Unpacked: {hepmc_gz_file} -> {hepmc_file}")
    return hepmc_file

def run_delphes(hepmc_file):
    delphes_dir = "/net/scratch_cms3a/spaeh/private/Software/MadGraph_v3_AL9/MG5_aMC_v3_5_2/Delphes"
    delphes_tcl = "cards/CMS_PhaseII/CMS_PhaseII_0PU_v02.tcl"
    delphes_output = hepmc_file.replace("tag_1_pythia8_events.hepmc", "tag_1_delphes_events.root")

    # Get the current working directory
    current_dir = os.getcwd()

    try:
        # Change to the Delphes directory
        os.chdir(delphes_dir)
        print(os.getcwd())
        # Run the Delphes command
        subprocess.run(f"./DelphesHepMC {delphes_tcl} {delphes_output} {hepmc_file}", shell=True, executable='/bin/bash')
        print(f"Delphes run complete: {hepmc_file} -> {delphes_output}")
    finally:
        # Return to the original directory
        os.chdir(current_dir)

    return delphes_output

def remove_hepmc(hepmc_file):
    os.remove(hepmc_file)
    print(f"HepMC file removed: {hepmc_file}")

def process_single_hepmc_file(hepmc_gz_file):
    # Unpack HepMC.gz
    hepmc_file = unpack_hepmc(hepmc_gz_file)

    # We want to "source" MadGraph so we can use its delphes installation
    subprocess.run('source /net/scratch_cms3a/spaeh/private/Software/MadGraph_v3_AL9/setup_MG5.sh', shell=True, executable='/bin/bash')

    # Run Delphes on the HepMC file
    delphes_output = run_delphes(hepmc_file)

    # Optionally, remove the HepMC file
    remove_hepmc(hepmc_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a single HepMC.gz file.")
    parser.add_argument("hepmc_gz_file", help="Path to the HepMC.gz file.")
    args = parser.parse_args()

    if not os.path.exists(args.hepmc_gz_file):
        print(f"Error: File '{args.hepmc_gz_file}' does not exist.")
    else:
        process_single_hepmc_file(args.hepmc_gz_file)
