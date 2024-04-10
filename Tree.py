from typing import Self

import ui as ui

###################################################################################################################
###################################################################################################################

class Tree:
    class Node:
        Name    : str
        Childs  : list[Self]
        """
        Child node can be None. For example, it is used in CFG, when there is right successor and there is no left one.
        """
        Parents : list[Self]

        Visited : bool
        """
        Flag for tree traversal algorithms. Indicates that node was already visited.
        """

        def __init__(self,
                     name   : str,
                     childs : list[Self] = None):
            self.Name    = name
            self.Parents = []
            self.Childs  = []
            self.Visited = False
            if (childs is not None):
                for child in childs:
                    self.AddChildToEnd(child)

        def InsertChildByIndex(self, 
                            child : Self, 
                            index : int):
            """
            Add child to node by index.

            Child is placed before element with index.

            Examples (let nodes be integer numbers for simplicity):
                Childs = []
                Result of node.AddChildByIndex(1, index = 0) is:
                    Childs == [1]

                Childs = [1, 2]
                Result of node.AddChildByIndex(3, index = 1) is:
                    Childs == [1, 3, 2]

                Childs = [1, 2]
                Result of node.AddChildByIndex(3, index = 2) is:
                    Childs == [1, 2, 3]

                Childs = [1, 2]
                Result of node.AddChildByIndex(3, index = 4) is:
                    Childs == [1, 2, None, None, 3]
            """
            if (index < 0):
                raise Exception(f"Index cannot be negative. index = {index}. If you want to add child at the top of the list use index = 0.")
            
            if (index <= self.GetChildrenCount()):
                self.Childs.insert(index, child)
            else:
                for st in range(self.GetChildrenCount(), index):
                    self.Childs.append(None)
                self.Childs.append(child)

        def SetChildByIndex(self, 
                            child : Self, 
                            index : int):
            """
            Set child to node by index.

            If len(self.Childs) is less, than index, then Childs will be expanded to size = index with None nodes.

            Examples (let nodes be integer numbers for simplicity):
                Childs = []
                Result of node.AddChildByIndex(1, index = 0) is:
                    Childs == [1]

                Childs = [1, 2]
                Result of node.AddChildByIndex(3, index = 1) is:
                    Childs == [1, 3]

                Childs = [1, 2]
                Result of node.AddChildByIndex(3, index = 4) is:
                    Childs == [1, 2, None, None, 3]
            """
            if (index < 0):
                raise Exception(f"Index cannot be negative. index = {index}.")
            
            if (index < self.GetChildrenCount()):
                self.Childs[st] = child
            else:
                for st in range(self.GetChildrenCount(), index):
                    self.Childs.append(None)
                self.Childs.append(child)

        def AddChildToTop(self, child : Self):
            self.Childs.insert(0, child)
            
        def AddChildToEnd(self, child : Self):
            self.Childs.append(child)

        def GetChildrenCount(self):
            return len(self.Childs)

        def PrettyName(self):
            return f"\"#c{self.Name}#rs\""
            
        def PrintValue(self, tabLevel : int):
            """
            Print the value of node.
            """
            raise NotImplementedError()
                
        def Print(self, tabLevel : int):
            self.Visited = True
            spaces = ui.GetSpacePadding(tabLevel)

            # Print name and value.
            ui.ColoredPrint(f"{spaces}{self.PrettyName()}:")
            self.PrintValue(tabLevel)

            if (len(self.Childs) == 0):
                ui.ColoredPrint(f"{spaces}#p_No children.#rs")
                return

            for st in range(len(self.Childs)):
                childNumberName = f"#y#p{spaces}Child{st}#rs"

                if (len(self.Childs) == 2):
                    if (st == 0):
                        childNumberName = f"#y#p{spaces}Left#rs"
                    else:
                        childNumberName = f"#y#p{spaces}Right#rs"

                if (self.Childs[st] is None):
                    ui.ColoredPrint(f"{childNumberName}#p  is None#rs.")
                else:
                    ui.ColoredPrint(f"{childNumberName}:")
                        
                    if (not self.Childs[st].Visited):
                        self.Childs[st].Print(tabLevel + 1)
                    else:
                        ui.ColoredPrint(f"{ui.GetSpacePadding(tabLevel + 1)}{self.Childs[st].PrettyName()} #p_already printed.#rs")

###################################################################################################################
###################################################################################################################
        
    RootNode   : Node
    """
    Entry node of CFG.
    """

    NodesArray : list[Node]
    """
    Array of nodes.
    """
    
    def __init__(self):
        self.RootNode   = None
        self.NodesArray = []

    def FindNode(self, nodeName : str) -> Self:
        for node in self.NodesArray:
            if (node.Name == nodeName):
                return node
        raise Exception(f"Node \"{nodeName}\" not found")
    
    def CheckNodesNotVisited(self):
        for node in self.NodesArray:
            node.Visited = False

    def Print(self, tabLevel : int = 0):
        self.CheckNodesNotVisited()
        if (self.RootNode is None):
            ui.ColoredPrint("#rCFG is None.#rs")
        else:
            self.RootNode.Print(tabLevel)

###################################################################################################################
###################################################################################################################