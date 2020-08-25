# Update Finite Difference Pages
#cd public_html/resultsWebsite/knifeEdge2DFD
#source gen_monitors.sh
#source gen_movies.sh
cd ~
# Update Spectral Axisymmetric Pages
cd public_html/resultsWebsite/spectral3DAxisym/
cd public_html/resultsWebsite/knifeEdgeSpectral3DAxisym
python gen_monitors.py
source gen_movies.sh
cd ~
## Update Spectral 3D Pages
cd public_html/resultsWebsite/spectral3D/
cd public_html/resultsWebsite/knifeEdgeSpectral3D
python gen_monitors.py
source gen_movies.sh
cd ~

# Could be done more elegantly,
# find public_html/Website/ -type f -iname "gen*" -exec bash {} \;
