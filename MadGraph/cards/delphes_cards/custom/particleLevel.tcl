#######################################
# Order of execution of various modules
#######################################

set ExecutionPath {
  PhotonFilter
  ElectronFilter
  MuonFilter

  NeutrinoFilter
  
  GenJetFinder

  GenMissingET

  UniqueObjectFinder

  InterestingParticlesFilter

  TreeWriter
}

#################
# Photon filter
#################

module PdgCodeFilter PhotonFilter {
  set InputArray Delphes/stableParticles
  set OutputArray photons
  set Invert true
  add PdgCode {22}
}

#################
# Electron filter
#################

module PdgCodeFilter ElectronFilter {
  set InputArray Delphes/stableParticles
  set OutputArray electrons
  set Invert true
  add PdgCode {11}
  add PdgCode {-11}
}

#################
# Muon filter
#################

module PdgCodeFilter MuonFilter {
  set InputArray Delphes/stableParticles
  set OutputArray muons
  set Invert true
  add PdgCode {13}
  add PdgCode {-13}
}

#####################
# Neutrino Filter
#####################

module PdgCodeFilter NeutrinoFilter {
  set InputArray Delphes/stableParticles
  set OutputArray filteredParticles

  set PTMin 0.0

  add PdgCode {12}
  add PdgCode {14}
  add PdgCode {16}
  add PdgCode {-12}
  add PdgCode {-14}
  add PdgCode {-16}
}

#####################
# MC truth jet finder
#####################

module FastJetFinder GenJetFinder {
    set InputArray NeutrinoFilter/filteredParticles
    set OutputArray GenJets
    
    # algorithm: 1 CDFJetClu, 2 MidPoint, 3 SIScone, 4 kt, 5 Cambridge/Aachen, 6 antikt
    
    set JetAlgorithm 6
    set ParameterR 0.4
    set JetPTMin 20.0
}

#########################
# Gen Missing ET merger
########################

module Merger GenMissingET {
# add InputArray InputArray
  add InputArray NeutrinoFilter/filteredParticles
  set MomentumOutputArray momentum
}

#####################################################
# Find uniquely identified photons/electrons/muons/jets
#####################################################

module UniqueObjectFinder UniqueObjectFinder {
# earlier arrays take precedence over later ones
# add InputArray InputArray OutputArray
  add InputArray PhotonFilter/photons photons
  add InputArray ElectronFilter/electrons electrons
  add InputArray MuonFilter/muons muons
  add InputArray FastJetFinder/GenJets jets
}

######################################
# Filter out VIP Particles
######################################

module PdgCodeFilter InterestingParticlesFilter {
    set InputArray Delphes/allParticles
    set OutputArray interestingParticles
    set Invert true
    # 5=bottom, 6=top, 11=electron, 13=muon, 15=tau (also antiparticles), 22=photon, 23=Z0, 24=W+, 25=SM Higgs boson
    # status=1 means particleLevel stable (do not add them for now because electrons, muons, photons, genjets are separate, see above)
    # status=22 means LHE intermediate
    # status=23 means LHE outgoing
    add PdgCode {5}
    add PdgCode {-5}
    add PdgCode {6}
    add PdgCode {-6}
    add PdgCode {11}
    add PdgCode {-11}
    add PdgCode {13}
    add PdgCode {-13}
    add PdgCode {15}
    add PdgCode {-15}
    add PdgCode {22}
    add PdgCode {23}
    add PdgCode {24}
    add PdgCode {-24}
    add PdgCode {25}
    #add status {1}
    add status {22}
    add status {23}
}

##################
# ROOT tree writer
##################

# If needed , (un)comment the relevant "add Branch ..." lines.

module TreeWriter TreeWriter {
    # add Branch InputArray BranchName BranchClass
    add Branch InterestingParticlesFilter/interestingParticles InterestingParticles GenParticle 
    add Branch UniqueObjectFinder/photons GenPhoton Photon
    add Branch UniqueObjectFinder/electrons GenElectron Electron
    add Branch UniqueObjectFinder/muons GenMuon Muon
    add Branch GenJetFinder/jets GenJet Jet
    add Branch GenMissingET/momentum GenMissingET MissingET
}