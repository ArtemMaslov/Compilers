import sys
import os

thisDirPath = os.path.dirname(os.path.abspath(__file__))
prevDirPath = os.path.dirname(thisDirPath)
prevPrevDirPath = os.path.dirname(prevDirPath)
sys.path.append(prevPrevDirPath)

from CFG import CFG

cfg = CFG()
cfg.ConstructFromFile(os.path.join(thisDirPath, "doms1.json"))
cfg.Print()