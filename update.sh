###########################
# Place in home directory #
###########################

# Update Knife Edge Finite Difference Pages
cd ~/public_html/resultsWebsite/knifeEdgeFD2D
source gen_monitors.sh
source gen_movies.sh
## Update Knife Edge Spectral 3D Pages
cd ~/public_html/resultsWebsite/knifeEdgeSpectral3D
python gen_monitors.py
source gen_movies.sh
# Update Knife Edge Spectral Axisymmetric Pages
cd ~/public_html/resultsWebsite/knifeEdgeSpectral3DAxisym
python gen_monitors.py
source gen_movies.sh
# Update Free Surf Finite Difference Pages
cd ~/public_html/resultsWebsite/freeSurfFD2D
python gen_monitors.py
source gen_movies.sh

# Could be done more elegantly,
# find public_html/Website/ -type f -iname "gen*" -exec bash {} \;
