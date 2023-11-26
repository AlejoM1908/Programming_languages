from antlr4 import *
from antlr4.Token import CommonToken
from antlr4.tree.Tree import TerminalNodeImpl
from typing import List

def compareTrees(tree1: ParserRuleContext, tree2: ParserRuleContext) -> float:
    """
    Compare two trees and return if they have any subtree in common

    Parameters
        tree1 (ParserRuleContext): First tree
        tree2 (ParserRuleContext): Second tree

    Returns
        float: Percentage of similarity
    """
    matching_nodes = countMatchingNodes(tree1, tree2)
    total_nodes = max(len(flattenTree(tree1)), len(flattenTree(tree2)))

    if total_nodes == 0:
        return 0
    
    return matching_nodes / total_nodes


def checkTerminalNode(node1: ParserRuleContext, node2: ParserRuleContext) -> int: 
    """
    Checks if two nodes are terminal nodes of a subtree and if they are of
    the same type

    Parameters
        tree1 (ParserRuleContext): First tree
        tree2 (ParserRuleContext): Second tree

    Returns
        int: 1 if they are terminal nodes of the same type, 0 otherwise
    """


    
    # Get type of both terminal nodes
    typeTerminalNodeTree1 = getNodeType(node1)
    typeTerminalNodeTree2 = getNodeType(node2)

    # If it is, and are the same type return 1
    return 0 if typeTerminalNodeTree1 != typeTerminalNodeTree2 else 1

def getNodeType(node: ParserRuleContext) -> int:
    """
    Get the type of a node

    Parameters
        node (ParserRuleContext): Node

    Returns
        int: Type of the node
    """
    if isinstance (node, CommonToken):
        return node.type
    elif isinstance (node, TerminalNodeImpl):
        return node.symbol.type
    else:
        return node.start.type


def countMatchingNodes(tree1: ParserRuleContext, tree2: ParserRuleContext) -> int:
    """
    Count the number of matching nodes in two trees

    Parameters
        tree1 (ParserRuleContext): First tree
        tree2 (ParserRuleContext): Second tree

    Returns
        int: Number of matching 
    """

    matching_nodes = 0

    # Flatten the trees to lists
    # Compare each pair of child nodes in both trees
    for i in range(tree1.getChildCount()):
        for j in range(tree2.getChildCount()):
            matching_nodes += countMatchingNodes(tree1.getChild(i), tree2.getChild(j))

    return matching_nodes


def flattenTree(tree: ParserRuleContext) -> List[ParserRuleContext]:
    """
    Flatten a tree to a list of nodes

    Parameters
        tree (ParserRuleContext): Tree

    Returns
        List[ParserRuleContext]: List of nodes
    """
    nodes = [tree]

    for i in range(tree.getChildCount()):
        nodes.extend(flattenTree(tree.getChild(i)))

    return nodes