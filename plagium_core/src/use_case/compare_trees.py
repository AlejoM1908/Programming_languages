from antlr4 import *
def compareTrees(tree1: ParserRuleContext, tree2: ParserRuleContext) -> float:
    """
    Compare two trees and return if they have any subtree in common

    Parameters
        tree1 (ParserRuleContext): First tree
        tree2 (ParserRuleContext): Second tree

    Returns
        float: Percentage of similarity
    """
    # Check if the tree is a terminal node
    if tree1.getChildCount() == 0:
        # If it is, return 0 if the other tree is not a terminal node
        if tree2.getChildCount() != 0:
            return 0

        # If it is, return 1 if the other tree is also a terminal node
        return 1
    
    # Check if the tree is a terminal node
    if tree2.getChildCount() == 0:
        # If it is, return 0 if the other tree is not a terminal node
        if tree1.getChildCount() != 0:
            return 0

        # If it is, return 1 if the other tree is also a terminal node
        return 1

    # Get the children of the trees
    children1 = tree1.children
    children2 = tree2.children

    # Get the number of children
    n1 = len(children1)
    n2 = len(children2)

    # If the number of children is different, return 0
    if n1 != n2:
        return 0

    # If the number of children is 0, return 1
    if n1 == 0:
        return 1

    # Compare the children
    similarity = 0
    for i in range(n1):
        similarity += compareTrees(children1[i], children2[i])

    # Return the similarity
    return similarity / n1