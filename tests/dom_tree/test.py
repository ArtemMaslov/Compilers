import sys
import os

thisDirPath = os.path.dirname(os.path.abspath(__file__))
codeDirPath = os.path.abspath(thisDirPath + "/../..")
sys.path.append(codeDirPath)

from jsoncomment import JsonComment

from CFG import CFG
from DomTree import DomTree
import ui as ui

files = ["dom_tree1.json", "dom_tree2.json", "dom_tree3.json"]

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
        dmtNode = dmt.FindNode(refNode["Name"])
        refNodeChilds = set(refNode["Dominates"])
        dmtNodeChilds = [node.Name for node in dmtNode.GetDominatingNodes()]
        if (refNodeChilds != dmtNodeChilds):
            ui.ColoredPrint(
                f"#rIncorrect list of dominating nodes for Node #c\"{dmtNode.Name}\"#rs.\n"
                f"    Ref  list = {refNodeChilds}\n"
                f"    Node list = {dmtNodeChilds}\n")
            passed = False

    if (passed):
        ui.ColoredPrint("#gTest passed!#rs")
    else:
        ui.ColoredPrint("#rTest FAILED.#rs")


    ui.ColoredPrint(f"\n#c**********************************************" + "*" * len(file) + "#rs\n")

for file in files:
    RunTest(file)