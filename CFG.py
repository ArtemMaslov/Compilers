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

        Visited : bool

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
        
        def PrettyName(self, level : int):
            spaces = "    " * level
            if (self.Name == "Exit" or self.Name == "Entry"):
                return f"{spaces}\"{self.Name}\""
            else:
                return f"{spaces}\"{self.Name}\" [{self.Index}]"
        
        def Print(self, level : int):
            self.Visited = True
            spaces = "    " * level
            print(f"{self.PrettyName(level)}:")
            if (self.Left is None):
                print(f"{spaces}Left  is None.")
            else:
                print(f"{spaces}Left:")

                if (not self.Left.Visited):
                    self.Left.Print(level + 1)
                else:
                    print(f"{self.Left.PrettyName(level + 1)} already printed.")

            if (self.Right is None):
                print(f"{spaces}Right is None.")
            else:
                print(f"{spaces}Right:")
                if (not self.Right.Visited):
                    self.Right.Print(level + 1)
                else:
                    print(f"{self.Right.PrettyName(level + 1)} already printed.")

###################################################################################################################
###################################################################################################################
        
    RootNode   : Node
    NodesArray : list[Node]
    
    def __init__(self):
        self.RootNode = None

    def ConstructFromFile(self, filePath : str):
        data = JsonComment().loadf(filePath)

        cfgNodes : list[CFG.Node] = []

        def FindNodeInList(nodeName : str, nodesList : list[CFG.Node]):
            for node in nodesList:
                if (node.Name == nodeName):
                    return node
            return None

        for dictNode in data["Nodes"]:
            cfgNode = CFG.Node(dictNode["Name"], None, None)
            cfgNodes.append(cfgNode)

        for st in range(0, len(data["Nodes"])):
            dictNode = data["Nodes"][st]
            cfgNode  = cfgNodes[st]

            if (dictNode["Left"] != ""):
                leftNode = FindNodeInList(dictNode["Left"], cfgNodes)
                if (leftNode == None):
                    raise Exception("Node \"{}\" not found".format(dictNode["Left"]))
                cfgNode.AddLeftChild(leftNode)                

            if (dictNode["Right"] != ""):
                rightNode = FindNodeInList(dictNode["Right"], cfgNodes)
                if (rightNode == None):
                    raise Exception("Node \"{}\" not found".format(dictNode["Right"]))
                cfgNode.AddRightChild(rightNode)

        entryNode = FindNodeInList("Entry", cfgNodes)
        self.RootNode   = entryNode
        self.NodesArray = cfgNodes

    def CheckNodesNotVisited(self):
        for node in self.NodesArray:
            node.Visited = False

    def Print(self):
        self.CheckNodesNotVisited()
        if (self.RootNode is None):
            print("CFG is None")
        else:
            self.RootNode.Print(0)

###################################################################################################################
###################################################################################################################