from typing import Self, TypeVar

from Tree import Tree
from CFG import CFG

import ui as ui

###################################################################################################################
###################################################################################################################

class DomTree(Tree):
    class Node(Tree.Node):
        def __init__(self,
                     name   : str,
                     childs : list[Self] = None):
            Tree.Node.__init__(self, name, childs)

        def PrintValue(self, tabLevel : int):
            pass

        def PrettyName(self):
            if (self.Name == "Entry"):
                return f"\"#g{self.Name}#rs\""
            elif (self.Name == "Exit"):
                return f"\"#r{self.Name}#rs\""
            else:
                return f"\"#c{self.Name}#rs\"#rs"
            
        def GetDominatingNodes(self):
            res = {self}
            for child in self.Childs:
                if (child is not None):
                    res.add(child.GetDominatingNodes())
            return res
            
###################################################################################################################
###################################################################################################################

    def BuildFromCFG(self, cfg : CFG):
        print_flag = True

        spaces = ui.GetSpacePadding(1)

        ui.DebugPrint("#yBuilding dominator tree...#rs\n", print_flag)

        ui.DebugPrint("#yFirst approximation:#rs\n", print_flag)

        # First approximation.
        # In and Out is temporary nodes variables.
        for node in cfg.NodesArray:
            node.In  = set()
            node.Out = set(cfg.NodesArray)

            ui.DebugPrint(f"{spaces}{node.PrettyName()}:\n", print_flag)
            ui.DebugPrint(f"{spaces}In  = {node.In}\n", print_flag)
            ui.DebugPrint(f"{spaces}Out = {node.Out}\n", print_flag)

        ui.DebugPrint("#yBoundary condition:#rs\n", print_flag)
        
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
            domTreeNode = DomTree.Node(node.Name)
            self.NodesArray.append(domTreeNode)

        for st in range(0, len(cfg.NodesArray)):
            node = cfg.NodesArray[st]
            domTreeNode = self.NodesArray[st]
            for childNode in node.Out:
                domTreeNode.AddChildToEnd(self.FindNode(childNode.Name))
        
        self.RootNode = self.FindNode("Entry")

        # Clearing algorithm temporary data.
        for node in cfg.NodesArray:
            del node.In
            del node.Out

###################################################################################################################
###################################################################################################################