"""Graph utilities for choosing controls (ECON 5200 Lab 10).

"Which variables should I adjust for?" is a question about a graph, and once the
graph is stated the answer is computable. The graph itself is not computable:
it is an argument you have to make and defend.
"""
from __future__ import annotations

import itertools

import networkx as nx


def backdoor_paths(G: nx.DiGraph, treatment: str, outcome: str) -> list[list[str]]:
    """Every path from treatment to outcome that starts with an arrow INTO
    the treatment. These are the paths adjustment has to block."""
    undirected = G.to_undirected()
    out = []
    for path in nx.all_simple_paths(undirected, treatment, outcome):
        if len(path) > 1 and G.has_edge(path[1], treatment):
            out.append(path)
    return out


def is_collider(G: nx.DiGraph, path: list[str], i: int) -> bool:
    """Node i on the path has both neighbours pointing INTO it."""
    return G.has_edge(path[i - 1], path[i]) and G.has_edge(path[i + 1], path[i])


def path_blocked(G: nx.DiGraph, path: list[str], S: set[str]) -> bool:
    """Is this path blocked by conditioning on S?

    A non-collider in S blocks. A collider blocks BY DEFAULT and is opened
    by conditioning on it or on any of its descendants: the opposite of the
    rule for chains and forks.
    """
    for i in range(1, len(path) - 1):
        node = path[i]
        if is_collider(G, path, i):
            opened = node in S or any(d in S for d in nx.descendants(G, node))
            if not opened:
                return True          # collider left closed, so the path is blocked
        elif node in S:
            return True              # non-collider conditioned on, so blocked
    return False


def is_valid_adjustment_set(G: nx.DiGraph, treatment: str, outcome: str,
                            S: set[str]) -> bool:
    """Backdoor criterion: S blocks every backdoor path and contains no
    descendant of the treatment."""
    if any(v in nx.descendants(G, treatment) for v in S):
        return False
    return all(path_blocked(G, p, S)
               for p in backdoor_paths(G, treatment, outcome))


def minimal_adjustment_sets(G: nx.DiGraph, treatment: str, outcome: str,
                            observed: set[str] | None = None) -> list[set[str]]:
    """Every smallest valid adjustment set drawn from the observed variables.

    Returns [] when no set works: the effect is then not identified by
    adjustment on what you measured, and you need a different design
    (Chapters 11-13).
    """
    pool = sorted((observed if observed is not None
                   else set(G.nodes)) - {treatment, outcome})
    for size in range(len(pool) + 1):
        found = [set(c) for c in itertools.combinations(pool, size)
                 if is_valid_adjustment_set(G, treatment, outcome, set(c))]
        if found:
            return found
    return []
