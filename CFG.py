# json parser with C-style comments.
from jsoncomment import JsonComment
import sys
print(sys.version)
from typing import Self

class CFG:
    class Node:
        Name   : str
        Left   : Self
        Right  : Self
        Parent : Self

        def __init__(self,
                     name   : str,
                     left   : Self = None,
                     right  : Self = None):
            self.Name   = name
            self.Parent = None
            self.AddLeftChild(left)
            self.AddRightChild(right)

        def AddLeftChild(self, left : Self):
            self.Left = left
            if (not self.Left is None):
                self.Left.Parent  = self

        def AddRightChild(self, right : Self):
            self.Right = right
            if (not self.Right is None):
                self.Right.Parent  = self

        def ConstructByName(name      : str,
                            leftName  : str,
                            rightName : str,
                            freeNodes : list[Self]) -> Self:
            leftNode  = None
            rightNode = None
            for st in range(len(freeNodes) - 1, -1, -1):
                node = freeNodes[st]
                if (node.Name == leftName):
                    leftNode = node
                    freeNodes.pop(st)
                elif (node.Name == rightName):
                    rightNode = node
                    freeNodes.pop(st)

            if (leftNode is None and leftName != ""):
                leftNode = CFG.Node(leftName)
            if (rightNode is None and rightName != ""):
                rightNode = CFG.Node(rightName)

            thisNode = CFG.Node(name, leftNode, rightNode)
            return thisNode

        def FindNodeByName(self, nodeName : str) -> Self:
            if (self.Name == nodeName):
                return self
            result = None
            if (not self.Left is None):
                result = self.Left.FindNodeByName(nodeName)
            if (result is None and (not self.Right is None)):
                result = self.Right.FindNodeByName(nodeName)
            return result
        
        def Print(self, level : int):
            spaces = "    " * level
            print(f"{spaces}\"{self.Name}\":")
            if (self.Left is None):
                print(f"{spaces}Left  is None.")
            else:
                print(f"{spaces}Left:")
                self.Left.Print(level + 1)

            if (self.Right is None):
                print(f"{spaces}Right is None.")
            else:
                print(f"{spaces}Right:")
                self.Right.Print(level + 1)
        
    RootNode : Node
    
    def __init__(self):
        self.RootNode = None

    def ConstructFromFile(self, filePath : str):
        data = JsonComment().loadf(filePath)

        freeNodes = []

        if (len(data["Nodes"]) > 0):
            dictNode = data["Nodes"][0]
            self.RootNode = CFG.Node.ConstructByName(dictNode["Name"], dictNode["Left"], dictNode["Right"], freeNodes)

        for st in range(1, len(data["Nodes"])):
            dictNode = data["Nodes"][st]

            cfgNode = CFG.Node.ConstructByName(dictNode["Name"], dictNode["Left"], dictNode["Right"], freeNodes)

            treeNode = self.RootNode.FindNodeByName(cfgNode.Name)
            if (not treeNode is None):
                parent = treeNode.Parent
                if (not parent.Left is None and parent.Left.Name == cfgNode.Name):
                    parent.AddLeftChild(cfgNode)
                elif (not parent.Right is None and parent.Right.Name == cfgNode.Name):
                    parent.AddRightChild(cfgNode)
                else:
                    raise Exception("CFG topology bug")
            else:
                freeNodes.append(cfgNode)

    def Print(self):
        if (self.RootNode is None):
            print("CFG is None")
        else:
            self.RootNode.Print(0)