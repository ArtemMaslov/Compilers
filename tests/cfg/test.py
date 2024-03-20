import sys
import os

thisDirPath = os.path.dirname(os.path.abspath(__file__))
codeDirPath = os.path.abspath(thisDirPath + "/../..")
sys.path.append(codeDirPath)

from jsoncomment import JsonComment

from CFG import CFG

files = ["cfg1.json", "cfg2.json"]

def RunTest(file):
    print(f"####################   {file}   ####################")
    cfg = CFG()
    filePath = os.path.join(thisDirPath, file)
    cfg.ConstructFromFile(filePath)
    cfg.BuildDFST()
    print("Tree:")
    cfg.Print()
    print("")

    passed = True

    ref = JsonComment().loadf(filePath)
    if ("Reference" not in ref):
        print("There are no reference data for this test.")
        return

    for refNode in ref["Reference"]:
        cfgNode = cfg.FindNode(refNode["Name"])
        if (cfgNode.Index != refNode["Index"]):
            print("Node \"{}\" has index \"{}\", but the correct value is \"{}\".".format(cfgNode.Name, cfgNode.Index, refNode["Index"]))
            passed = False

    if (passed):
        print("Test passed!")
    else:
        print("Test FAILED.")


    print(f"\n##############################################" + "#" * len(file) + "\n")

for file in files:
    RunTest(file)