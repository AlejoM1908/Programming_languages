from antlr4 import *

def getSubtrees(tree: ParserRuleContext) -> list[ParserRuleContext]:
    """
    Get all subtrees of a tree

    Parameters:
        tree (ParserRuleContext): Tree to get the subtrees from

    Returns:
        List[ParserRuleContext]: List of subtrees
    """
    subtrees = [tree]

    for i in range(tree.getChildCount()):
        subtrees.extend(getSubtrees(tree.getChild(i)))

    return subtrees

def hashSubtree(subtree: ParserRuleContext) -> int:
    """
    Generate a hash for a subtree.

    Parameters:
        subtree (ParserRuleContext): Subtree to hash

    Returns:
        int: Hash value
    """
    # Implementación simple: usa una combinación de tipos de nodos y su estructura.
    # Nota: Esta es una implementación básica y puede necesitar ser más sofisticada.
    hash_value = 7
    node_type = type(subtree).__name__
    hash_value = 31 * hash_value + hash(node_type)

    for i in range(subtree.getChildCount()):
        child = subtree.getChild(i)
        hash_value = 31 * hash_value + hashSubtree(child)

    return hash_value

def compareTreesUseCase(tree1: ParserRuleContext, tree2: ParserRuleContext) -> float:
    """
    Compare two trees and return if they have any subtree in common

    Parameters
        tree1 (ParserRuleContext): First tree
        tree2 (ParserRuleContext): Second tree

    Returns
        float: Percentage of similarity
    """
    first_subtrees = getSubtrees(tree1)
    second_subtrees = getSubtrees(tree2)

    first_hashes = {hashSubtree(subtree) for subtree in first_subtrees}
    second_hashes = {hashSubtree(subtree) for subtree in second_subtrees}

    # Calcula las coincidencias y el total de subárboles únicos
    matches = first_hashes.intersection(second_hashes)
    total_unique_subtrees = len(first_hashes) + len(second_hashes) - len(matches)

    if total_unique_subtrees == 0:
        return 0  # Evita la división por cero

    similarity_percentage = (len(matches) / total_unique_subtrees) * 100
    return similarity_percentage
