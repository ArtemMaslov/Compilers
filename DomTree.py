from typing import Self, TypeVar

from Tree import Tree
from CFG import CFG
from CNodes import CNode, CNodeInfo

import ui as ui

###################################################################################################################
###################################################################################################################

class DomTree(Tree):
    RootNode   : CNode
    NodesArray : list[CNode]

    def BuildFromCFG(self, cfg : CFG):
        print_flag = True
        spaces1 = ui.GetSpacePadding(1)
        spaces2 = ui.GetSpacePadding(2)

        ui.DebugPrint("#yBuilding dominator tree...#rs\n", print_flag)

        ui.DebugPrint("#yFirst approximation:#rs\n", print_flag)

        # First approximation.
        # In and Out is temporary nodes variables.
        for node in cfg.NodesArray:
            node.In  = set()
            node.Out = set(cfg.NodesArray)
            ui.DebugPrint(f"{spaces1}{node.PrettyName()}:", print_flag)
            ui.DebugPrint(f"{spaces1}In  = {Tree.NodesNamesToStr(node.In)}", print_flag)
            ui.DebugPrint(f"{spaces1}Out = {Tree.NodesNamesToStr(node.Out)}\n", print_flag)
        
        # Boundary condition.
        entryNode = cfg.FindNode("Entry")
        entryNode.Out = set([entryNode])

        ui.DebugPrint("#yBoundary condition:#rs\n", print_flag)
        ui.DebugPrint(f"{spaces1}{entryNode.PrettyName()}:", print_flag)
        ui.DebugPrint(f"{spaces1}In  = {Tree.NodesNamesToStr(entryNode.In)}", print_flag)
        ui.DebugPrint(f"{spaces1}Out = {Tree.NodesNamesToStr(entryNode.Out)}\n", print_flag)

        while (True):
            changed = False

            for node in cfg.NodesArray:
                if (node.Name == "Entry"):
                    ui.DebugPrint(f"Skipping entry node\n", print_flag)
                    continue
                
                ui.DebugPrint(f"{spaces1}{node.PrettyName()}:", print_flag)
                ui.DebugPrint(f"{spaces1}CurrentIn  = {Tree.NodesNamesToStr(node.In)}", print_flag)
                ui.DebugPrint(f"{spaces1}CurrentOut = {Tree.NodesNamesToStr(node.Out)}\n", print_flag)

                prevNodeOut = node.Out
                # New In.t
                node.In = set()
                if (len(node.Parents) > 0):
                    node.In = node.Parents[0].Out
                for parentNode in node.Parents:
                    ui.DebugPrint(f"{spaces2}Parent    = {parentNode.PrettyName(False)}", print_flag)
                    ui.DebugPrint(f"{spaces2}ParentOut = {Tree.NodesNamesToStr(parentNode.Out)}", print_flag)
                    node.In = node.In & parentNode.Out
                    ui.DebugPrint(f"{spaces2}NewIn = {Tree.NodesNamesToStr(node.In)}\n", print_flag)
                # New Out.
                node.Out = set([node]) | node.In
                ui.DebugPrint(f"{spaces1}NewOut = {Tree.NodesNamesToStr(node.Out)}\n", print_flag)

                # Check for changes.
                if (node.Out != prevNodeOut):
                    ui.DebugPrint(f"Node {node.PrettyName(False)} has changed.\n", print_flag)
                    changed = True

            if (not changed):
                break

        ui.DebugPrint(f"#yConstructing tree...#rs\n", print_flag)
    
        for node in cfg.NodesArray:
            dmtNode = CNode(node.Name, node.CNodeInfo)
            self.NodesArray.append(dmtNode)

        # Building dominators tree.
        printTreeDebug = True

        for st in range(0, len(cfg.NodesArray)):
            cfgNode = cfg.NodesArray[st]
            dmtNode = self.NodesArray[st]

            ui.DebugPrint(f"Node = {cfgNode.PrettyName(False)}", printTreeDebug)
            
            doms = []
            for _cfgNode in cfgNode.Out:
                _dmtNode = self.FindNode(_cfgNode.Name)
                doms.append(_dmtNode)
            CNode.Sort(doms)

            dmtNode.CNodeInfo.Doms = doms

            ui.DebugPrint(f"Doms = {Tree.NodesNamesToStr(doms)}", printTreeDebug)

            if (dmtNode.Name != "Entry"):
                dmtNode.CNodeInfo.IDom = dmtNode.CNodeInfo.Doms[-2]
                ui.DebugPrint(f"IDom = {dmtNode.CNodeInfo.IDom.PrettyName(False)}", printTreeDebug)

                parentNode = self.FindNode(dmtNode.CNodeInfo.IDom.Name)
                parentNode.AddChildToEnd(dmtNode)
                ui.DebugPrint(f"Parent = {parentNode.PrettyName(False)}", printTreeDebug)
            print("")
        
        self.RootNode = self.FindNode("Entry")

        # Clearing algorithm temporary data.
        for node in cfg.NodesArray:
            del node.In
            del node.Out

###################################################################################################################
###################################################################################################################