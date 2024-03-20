from CFG import CFG

###################################################################################################################
###################################################################################################################

def ConstructDFST(cfg : CFG):
    cfg.CheckNodesNotVisited()
    currentIndex = len(cfg.NodesArray) - 2 
    # -2, because NodesArray contains Entry and Exit nodes, which should not to be numerated.

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
        currentIndex -= 1

    assert(cfg.RootNode.Name == "Entry")
    assert(cfg.RootNode.Left is not None)
    assert(cfg.RootNode.Right is None)

    helper(cfg, cfg.RootNode.Left)

###################################################################################################################
###################################################################################################################