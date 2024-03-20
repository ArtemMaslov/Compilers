from typing import Self, TypeVar

class DomTree:
    class Node:
        Name   : str
        Childs : list[Self]
        Parent : Self

        def __init__(self,
                     name  : str,
                     childs : list[Self]):
            self.Name    = name
            self.Childs  = []
            self.Parent  = None
            for child in childs:
                self.AddChild(child)


        def AddChild(self, child : Self):
            if (child is not None):
                self.Childs.append(child)
                child.Parent = self

    RootNode : Node

    def __init__(self):
        RootNode = None
