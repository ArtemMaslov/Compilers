import sys
import os

thisDirPath = os.path.dirname(os.path.abspath(__file__))
codeDirPath = os.path.abspath(thisDirPath + "/../..")
sys.path.append(codeDirPath)

from jsoncomment import JsonComment

from CFG import CFG
from DomTree import DomTree
import ui

files = ["dom_tree1.json", "dom_tree2.json"]

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

    passed = True

    ref = JsonComment().loadf(filePath)
    if ("Reference" not in ref):
        ui.ColoredPrint("#yThere are no reference data for this test.#rs")
        return

    return

    for refNode in ref["Reference"]:
        cfgNode = cfg.FindNode(refNode["Name"])
        if (cfgNode.Index != refNode["Index"]):
            ui.ColoredPrint("#rNode #c\"{}\"#rs has index #y\"{}\"#r, but the correct value is #y\"{}\"#rs.".format(cfgNode.Name, cfgNode.Index, refNode["Index"]))
            passed = False

    if (passed):
        ui.ColoredPrint("#gTest passed!#rs")
    else:
        ui.ColoredPrint("#rTest FAILED.#rs")


    ui.ColoredPrint(f"\n#c**********************************************" + "*" * len(file) + "#rs\n")

for file in files:
    RunTest(file)