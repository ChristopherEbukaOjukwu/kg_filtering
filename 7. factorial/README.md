# Pre-factorial sanity check. 

Before running 16 cells, verify that applying each filter individually gives sensible counts. 
This catches off-by-one threshold bugs and column-name typos, before they propagate across 16 cells.
source: prefactorial_sanity_check.py
