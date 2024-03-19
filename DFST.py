from CFG import CFG

def ConstructDFST(cfg : CFG):
    currentIndex = cfg.NodesCount
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

    helper(cfg, cfg.RootNode.Left)