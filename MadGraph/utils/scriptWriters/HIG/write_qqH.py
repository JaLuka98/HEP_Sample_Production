import argparse
import sys

def generate_madgraph_script(quark, sqrts):
    if quark == 'up':
        q = 'u' 
    elif quark == 'down':
        q = 'd'
    elif quark == 'strange':
        q = 's'
    else:
        print(f'Problem: Selected {quark} but this is not supported.')
        sys.exit(1)

    ebeam = sqrts / 2 * 1000 # unit conversion from TeV to GeV

    template = f"""
import model SMEFTsim_U35_MwScheme_UFO-lightQuarkYukawas
set gauge unitary

# Use QCD==2 to avoid VBF-like diagrams and {q}{q}-> {q}{q}H Higgs-fusion diagrams
generate {q} {q}~ > h QCD==0 SMHLOOP==0
add process {q} {q}~ > h j QCD==1 SMHLOOP==0
add process {q} g > h j QCD==1 SMHLOOP==0
add process {q}~ g > h j QCD==1 SMHLOOP==0
# Do not take other q(~) g > h j into account as they do not contribute at yup-level
add process {q} {q}~ > h j j QCD==2 SMHLOOP==0
add process {q} g > h j j QCD==2 SMHLOOP==0
add process {q}~ g > h j j QCD==2 SMHLOOP==0
# Restrict final states to {quark} quarks because we are interested in {q}{q}H coupling
# Initial state radiation still contributes but will be zero as we set the couplings to zero
add process d d~ > h {q} {q}~ QCD==2 SMHLOOP==0
add process s s~ > h {q} {q}~ QCD==2 SMHLOOP==0
add process c c~ > h {q} {q}~ QCD==2 SMHLOOP==0
add process g g > h {q} {q}~ QCD==2 SMHLOOP==0
# Due to baryon conservation, stuff like d g > h j j cannot lead to diagrams with {q}{q}H coupling, so neglect them
# This is now the kappa approach, using cuH would also be possible, maybe later

output /user/scratch/spaeh/MG5_temp/HIG/{q}{q}HtoGG_M-125_{sqrts}TeV_MG5MLM-pythia8
launch /user/scratch/spaeh/MG5_temp/HIG/{q}{q}HtoGG_M-125_{sqrts}TeV_MG5MLM-pythia8
shower=PY8
detector=ON # use Delphes
done
# Give external cards
../../cards/pythia8_cards/pythia8_card_Hgamgam.dat
../../cards/delphes_cards/custom/particleLevel.tcl
set ebeam {ebeam}
set ymup {'4.18' if quark == 'up' else '0.0'}
set ymdo {'4.18' if quark == 'down' else '0.0'}
set yms {'4.18' if quark == 'strange' else '0.0'}
set ymc 0.0
set use_syst False
set ickkw 1
set xqcut 30
set auto_ptj_mjj T
set drjj 0
set scale 125
set dsqrt_q2fact1 31.25
set dsqrt_q2fact2 31.25
set nevents 250k
done
"""
    
    # Save to a file
    filename = f"../../../scripts/HIG/{q}{q}HtoGG_M-125_{sqrts}TeV_MG5MLM-pythia8.mg5"
    with open(filename, 'w') as file:
        file.write(template)
    print(f"Generated MadGraph script saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate MadGraph5 scripts for studies for single Higgs production from diagrams with qqH coupling for different light-quark species.")
    parser.add_argument('quark', type=str, choices=['up', 'down', 'strange'],
                        help='Specify the light-quark species to consider (up, down, strange).')
    parser.add_argument('--sqrts', type=int, default=14,
                        help='Specify the center-of-mass energy in TeV (default is 14).')
    args = parser.parse_args()
    generate_madgraph_script(args.quark, args.sqrts)

if __name__ == "__main__":
    main()
