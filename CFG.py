# json parser with C-style comments.
from jsoncomment import JsonComment
import sys
from typing import Self, TypeVar

###################################################################################################################
###################################################################################################################

TCFG = TypeVar("TCFG", bound="CFG")

class CFG:
    class Node:
        Name   : str
        Left   : Self
        Right  : Self
        Parent : Self

        Index  : int
        """
        DFST (deep first spanning tree) index.
        """

        NonValidIndex = -1
        """
        Constant for non valid index.
        """

        Visited : bool
        """
        Flag for tree traversal algorithms. Indicates that node was already visited.
        """

        def __init__(self,
                     name  : str,
                     left  : Self = None,
                     right : Self = None):
            self.Name    = name
            self.Parent  = None
            self.Visited = False
            self.AddLeftChild(left)
            self.AddRightChild(right)
            self.SetIndex(CFG.Node.NonValidIndex)

        def AddLeftChild(self, left : Self):
            self.Left = left
            if (self.Left is not None):
                self.Left.Parent  = self

        def AddRightChild(self, right : Self):
            self.Right = right
            if (self.Right is not None):
                self.Right.Parent  = self

        def SetIndex(self, index : int):
            self.Index = index

        def FindNodeByName(self, nodeName : str) -> Self:
            if (self.Name == nodeName):
                return self
            result = None
            if (self.Left is not None):
                result = self.Left.FindNodeByName(nodeName)
            if (result is None and (self.Right is not None)):
                result = self.Right.FindNodeByName(nodeName)
            return result
        
        def PrettyName(self, tabLevel : int):
            spaces = "    " * tabLevel
            if (self.Name == "Exit" or self.Name == "Entry"):
                return f"{spaces}\"{self.Name}\""
            else:
                return f"{spaces}\"{self.Name}\" [{self.Index}]"
        
        def Print(self, tabLevel : int):
            self.Visited = True
            spaces = "    " * tabLevel
            print(f"{self.PrettyName(tabLevel)}:")
            if (self.Left is None):
                print(f"{spaces}Left  is None.")
            else:
                print(f"{spaces}Left:")

                if (not self.Left.Visited):
                    self.Left.Print(tabLevel + 1)
                else:
                    print(f"{self.Left.PrettyName(tabLevel + 1)} already printed.")

            if (self.Right is None):
                print(f"{spaces}Right is None.")
            else:
                print(f"{spaces}Right:")
                if (not self.Right.Visited):
                    self.Right.Print(tabLevel + 1)
                else:
                    print(f"{self.Right.PrettyName(tabLevel + 1)} already printed.")

###################################################################################################################
###################################################################################################################
        
    RootNode   : Node
    """
    Entry node of CFG.
    """

    NodesArray : list[Node]
    """
    Array of CFG nodes. After BuildDFST call, the nodes are arranged in ascending order.
    """
    
    def __init__(self):
        self.RootNode = None

    def ConstructFromFile(self, filePath : str):
        """
        Read json config file and build CFG tree.
        """
        data = JsonComment().loadf(filePath)

        self.NodesArray = []

        for dictNode in data["Nodes"]:
            cfgNode = CFG.Node(dictNode["Name"], None, None)
            self.NodesArray.append(cfgNode)

        for st in range(0, len(data["Nodes"])):
            dictNode = data["Nodes"][st]
            cfgNode  = self.NodesArray[st]

            if (dictNode["Left"] != ""):
                leftNode = self.FindNode(dictNode["Left"])
                if (leftNode == None):
                    raise Exception("Node \"{}\" not found".format(dictNode["Left"]))
                cfgNode.AddLeftChild(leftNode)                

            if (dictNode["Right"] != ""):
                rightNode = self.FindNode(dictNode["Right"])
                if (rightNode == None):
                    raise Exception("Node \"{}\" not found".format(dictNode["Right"]))
                cfgNode.AddRightChild(rightNode)

        self.RootNode = self.FindNode("Entry")

    def BuildDFST(self):
        """
        Algorithm for building deep first spanning tree (DFST) and numerating CFG nodes.
        """
        self.CheckNodesNotVisited()
        currentIndex = len(self.NodesArray) - 2 
        # -2, because NodesArray contains Entry and Exit nodes, which should not to be numerated.

        newNodesArray : list[CFG.Node] = [self.FindNode("Entry"), self.FindNode("Exit")]

        def helper(cfg : CFG, node : CFG.Node):
            nonlocal currentIndex

            node.Visited = True

            if (node.Name == "Exit"):
                return

            if (node.Left is not None and not node.Left.Visited):
                helper(cfg, node.Left)

            if (node.Right is not None and not node.Right.Visited):
                helper(cfg, node.Right)

            node.SetIndex(currentIndex)
            newNodesArray.insert(1, node)
            currentIndex -= 1

        assert(self.RootNode.Name == "Entry")
        assert(self.RootNode.Left is not None)
        assert(self.RootNode.Right is None)

        helper(self, self.RootNode.Left)

        self.NodesArray = newNodesArray

    def FindNode(self, nodeName : str):
        for node in self.NodesArray:
            if (node.Name == nodeName):
                return node
        return None

    def CheckNodesNotVisited(self):
        for node in self.NodesArray:
            node.Visited = False

    def Print(self, tabLevel : int = 0):
        self.CheckNodesNotVisited()
        if (self.RootNode is None):
            print("CFG is None")
        else:
            self.RootNode.Print(tabLevel)

###################################################################################################################
###################################################################################################################