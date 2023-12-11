Naming scheme for MadGraph5 samples:
`<initialState>to<finalState>_<importantParameters>_<sqrts>_<generator><matchingScheme>-<shower>`

Correct way of unpacking the hepmc files:
`zcat tag_1_pythia8_events.hepmc.gz > tag_1_pythia8_events.hepmc`
This can take a few minutes as the hepmc files can be quite large

TODO: Add script that creates the dir structure in output
TODO: Add Delphes instructions

One can run Delphes during the MadGraph run or afterwards ("standalone").
To run standalone: 
`/net/software/cms/madgraph/MG5_aMC_v3_4_0/Delphes/DelphesHepMC ../../../../../cards/delphes_cards/common/delphes_card_CMS.tcl tag_1_pythia8_events_delphes_card_CMS.root tag_1_pythia8_events.hepmc`

`/net/software/cms/madgraph/MG5_aMC_v3_4_0/Delphes/DelphesHepMC ../../../../../cards/delphes_cards/custom/delphes_card_CMS_noSmear.tcl tag_1_pythia8_events_delphes_card_CMS_noSmear.root tag_1_pythia8_events.hepmc`