import sys
import os

thisDirPath = os.path.dirname(os.path.abspath(__file__))
codeDirPath = os.path.abspath(thisDirPath + "/../..")
sys.path.append(codeDirPath)

from jsoncomment import JsonComment

from CFG import CFG
from DomTree import DomTree
import ui as ui

files = ["dom_tree5.json"]

def RunTest(file):
    ui.ColoredPrint(f"#c********************   #y{file}#c   ********************#rs")
    cfg = CFG()
    filePath = os.path.join(thisDirPath, file)
    cfg.ConstructFromFile(filePath)
    cfg.BuildDFST()

    ui.ColoredPrint("#yCFG:#rs")
    cfg.Print()
    print("")

    ui.ColoredPrint("#yDominator tree:#rs")
    dmt = DomTree()
    dmt.BuildFromCFG(cfg)
    dmt.Print()
    print("")

    dmt.ComputeDominanceFrontier(cfg)

    ui.ColoredPrint(f"\n#c**********************************************" + "*" * len(file) + "#rs\n")

for file in files:
    RunTest(file)