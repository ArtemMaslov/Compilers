# json parser with C-style comments.
from jsoncomment import JsonComment
import sys
from typing import Self, TypeVar

from Tree import Tree
from CNodes import CNode, CNodeInfo

import ui as ui

###################################################################################################################
###################################################################################################################

TCFG = TypeVar("TCFG", bound="CFG")

class CFG(Tree):
    RootNode   : CNode
    NodesArray : list[CNode]

    def ConstructFromFile(self, filePath : str):
        """
        Read json config file and build CFG tree.
        """
        data = JsonComment().loadf(filePath)

        self.NodesArray = []

        for dictNode in data["Nodes"]:
            cfgNode = CNode(dictNode["Name"], CNodeInfo())
            self.NodesArray.append(cfgNode)

        for st in range(0, len(data["Nodes"])):
            dictNode = data["Nodes"][st]
            cfgNode  = self.NodesArray[st]

            def AddNode(recordNode, index):
                if (recordNode == ""):
                    return
                
                node = self.FindNode(recordNode)
                cfgNode.SetChildByIndex(node, index)
                
            for record in dictNode:
                if (record == "Left"):
                    AddNode(dictNode[record], 0)

                if (record == "Right"):
                    AddNode(dictNode[record], 1)

                if (record.startswith("Child")):
                    index = int(record[len("Child") : ])
                    AddNode(dictNode[record], index)

        self.RootNode = self.FindNode("Entry")

    def BuildDFST(self):
        """
        Algorithm for building deep first spanning tree (DFST) and numerating CFG nodes.
        """
        self.CheckNodesNotVisited()
        currentIndex = len(self.NodesArray) - 2 
        # -2, because NodesArray contains Entry and Exit nodes, which should not to be numerated.

        newNodesArray : list[CNode] = [self.FindNode("Entry"), self.FindNode("Exit")]
        newNodesArray[0].CNodeInfo.Index = CNodeInfo.NonValidIndex
        newNodesArray[1].CNodeInfo.Index = len(self.NodesArray) - 1

        def helper(cfg : CFG, node : CNode):
            nonlocal currentIndex

            node.Visited = True

            if (node.Name == "Exit"):
                return
            
            for child in node.Childs:
                if (child is None):
                    continue
                
                if (not child.Visited):
                    helper(cfg, child)

            node.CNodeInfo.Index = currentIndex
            newNodesArray.insert(1, node)
            currentIndex -= 1

        assert(self.RootNode.Name == "Entry")
        assert(self.RootNode.Childs[0] is not None)

        helper(self, self.RootNode.Childs[0])

        self.NodesArray = newNodesArray

###################################################################################################################
###################################################################################################################