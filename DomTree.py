from typing import Self, TypeVar

from CFG import CFG

import ui

###################################################################################################################
###################################################################################################################

class DomTree:
    class Node:
        Name   : str
        Childs : list[Self]
        Parent : Self

        Visited : bool
        """
        Flag for tree traversal algorithms. Indicates that node was already visited.
        """

        def __init__(self,
                     name   : str,
                     childs : list[Self]):
            self.Name    = name
            self.Childs  = []
            self.Parent  = None
            if (childs is not None):
                for child in childs:
                    self.AddChild(child)

        def AddChild(self, child : Self):
            if (child is not None):
                self.Childs.append(child)
                child.Parent = self

        def PrettyName(self, tabLevel : int):
            spaces = "    " * tabLevel
            if (self.Name == "Entry"):
                return f"{spaces}\"#g{self.Name}#rs\""
            elif (self.Name == "Exit"):
                return f"{spaces}\"#r{self.Name}#rs\""
            else:
                return f"{spaces}\"#c{self.Name}#rs\"#rs"
        
        def Print(self, tabLevel : int):
            self.Visited = True
            spaces = "    " * tabLevel
            ui.ColoredPrint(f"{self.PrettyName(tabLevel)}:")
            ui.ColoredPrint(f"#y#p{spaces}Childs#rs:")
            
            for childNode in self.Childs:
                if (not childNode.Visited):
                    childNode.Print(tabLevel + 1)
                else:
                    ui.ColoredPrint(f"{childNode.PrettyName(tabLevel + 1)} #palready printed.#rs")

###################################################################################################################
###################################################################################################################

    RootNode   : Node
    NodesArray : list[Node]

    def __init__(self):
        self.RootNode   = None
        self.NodesArray = []

    def BuildFromCFG(self, cfg : CFG):
        # First approximation.
        for node in cfg.NodesArray:
            node.In  = set()
            node.Out = set(cfg.NodesArray)

        # Boundary condition.
        entryNode = cfg.FindNode("Entry")
        entryNode.Out = set([entryNode])

        while (True):
            changed = False

            for node in cfg.NodesArray:
                if (node.Name == "Entry"):
                    continue

                prevNodeOut = node.Out
                # New In.
                node.In  = set()
                for parentNode in node.Parents:
                    node.In = node.In & parentNode.Out
                # New Out.
                node.Out = set([node]) | node.In
                # Check for changes.
                if (node.Out != prevNodeOut):
                    changed = True

            if (not changed):
                break

        # Building dominators tree.
        for node in cfg.NodesArray:
            domTreeNode = DomTree.Node(node.Name, None)
            self.NodesArray.append(domTreeNode)

        for st in range(0, len(cfg.NodesArray)):
            node = cfg.NodesArray[st]
            domTreeNode = self.NodesArray[st]
            for childNode in node.Out:
                domTreeNode.AddChild(self.FindNode(childNode.Name))
        
        self.RootNode = self.FindNode("Entry")

        # Clearing algorithm intermediate data.
        for node in cfg.NodesArray:
            del node.In
            del node.Out

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
            ui.ColoredPrint("#DomTree is None.#rs")
        else:
            self.RootNode.Print(tabLevel)

###################################################################################################################
###################################################################################################################