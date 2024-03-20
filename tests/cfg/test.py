import sys
import os

thisDirPath = os.path.dirname(os.path.abspath(__file__))
prevDirPath = os.path.dirname(thisDirPath)
prevPrevDirPath = os.path.dirname(prevDirPath)
sys.path.append(prevPrevDirPath)

from CFG import CFG
import DFST

print("##########   cfg1.json   ##########")
cfg = CFG()
cfg.ConstructFromFile(os.path.join(thisDirPath, "cfg1.json"))
DFST.ConstructDFST(cfg)
cfg.Print()

print("\n\n")

print("##########   cfg2.json   ##########")
cfg = CFG()
cfg.ConstructFromFile(os.path.join(thisDirPath, "cfg2.json"))
DFST.ConstructDFST(cfg)
cfg.Print()