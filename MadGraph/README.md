Naming scheme for MadGraph5 samples:
`<initialState>to<finalState>_<importantParameters>_<sqrts>_<generator><matchingScheme>-<shower>`

Correct way of unpacking the hepmc files:
`zcat tag_1_pythia8_events.hepmc.gz > tag_1_pythia8_events.hepmc`

TODO: Add script that creates the dir structure in output
TODO: Add Delphes instructions

One can run Delphes during the MadGraph run or afterwards ("standalone").
To run standalone: 
`./DelphesHepMC cards/delphes_card_custom_CMS_Hgg_stripped.tcl output.root ../../../../PhD/Studies/light_quark_couplings/first_simulations/uubar_to_Hjets_scripts/uubar_to_Hjets/Events/run_01/tag_1_pythia8_events.hepmc`