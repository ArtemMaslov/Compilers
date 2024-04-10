from typing import Self, TypeVar

from Tree import Tree

import ui as ui

###################################################################################################################
###################################################################################################################

TCNodeInfo = TypeVar("TCNodeInfo", bound = "CNodeInfo")
TCNode     = TypeVar("TCNode", bound = "CNode")

class CNodeInfo:
    Index  : int
    """
    DFST (deep first spanning tree) index.
    """

    NonValidIndex = -1
    """
    Constant for non valid index.
    """
    
    Doms : list[TCNode]
    """
    A set of dominators of this node.
    """

    IDom : TCNode
    """
    Direct dominator.
    """

    def __init__(self):
        self.Index = CNodeInfo.NonValidIndex
        self.Doms = []
        self.IDom = None

    def Sort(nodes):
        nodes.sort(key = lambda node: node.Index)

class CNode(Tree.Node):
    CNodeInfo : TCNodeInfo
    
    def __init__(self,
                 name     : str,
                 CNodeInfo : TCNodeInfo,
                 childs : list[Self] = None):
        Tree.Node.__init__(self, name, childs)
        self.CNodeInfo = CNodeInfo

    def Sort(nodes):
        nodes.sort(key = lambda node: node.CNodeInfo.Index)

    def PrintValue(self, tabLevel : int):
        pass
    
    def PrettyName(self, printIndex = True):
        if (self.Name == "Entry"):
            return f"\"#g{self.Name}#rs\""
        elif (self.Name == "Exit"):
            return f"\"#r{self.Name}#rs\""
        else:
            if (printIndex):
                return f"\"#c{self.Name}#rs\" #g[{self.CNodeInfo.Index}]#rs"
            else:
                return f"\"#c{self.Name}#rs\""
            
###################################################################################################################
###################################################################################################################