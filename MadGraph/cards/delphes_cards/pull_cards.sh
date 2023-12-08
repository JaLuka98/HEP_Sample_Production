mkdir -p common/
# Alternative curl -O
wget -nc https://raw.githubusercontent.com/delphes/delphes/master/cards/delphes_card_CMS.tcl -P ./common/
wget -nc https://raw.githubusercontent.com/delphes/delphes/master/cards/CMS_PhaseII/CMS_PhaseII_0PU_v02.tcl -P ./common/