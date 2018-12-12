# Created by: Elias Mote, Ryan Moeller
import json
import sys
from typing import Dict, List, Optional, Set, Tuple


symbol = str
state = int
States = List[state]
Symbols = List[symbol]
txDomain = Tuple[state, symbol]
txRange = Optional[state]
Transfers = Dict[txDomain, txRange]
TransitionTable = List[List[txRange]]

# ω is the state reached if the walk terminates in a loop of any kind.
ω: state = -1


def tabulate(Q: States, Σ: Symbols, δ: Transfers) -> TransitionTable:
    """
    Turn a set of transfers Q × Σ -> Q into a table of transitions.
    The transition table has a row for each state and column for each symbol,
    with the destination state as the entry.
    """
    return [[δ.get((q,a)) for a in Σ] for q in Q]


def augment(s: state, a: symbol) -> state:
    print("FIXME")
    return s


def representative(s: state, l: int) -> state:
    print("FIXME")
    return s


def construct_dfa(k: int) -> dict:
    # The max length of the self-avoiding walk we are checking
    max_length: int = k

    symbols: Symbols = ["r", "u", "l", "d"] # right, up, left, down
    start_state: state = 0
    end_states: List[state] = [ω]

    #
    # Step 1
    #

    # Initialize a set of untreated states with state 0 as the only element
    untreated: Set[state] = {0}

    # Initialize an empty set of treated states
    treated: Set[state] = set()

    # Initialize an empty set of transfers
    transfers: Transfers = {}

    # The current walk length we are considering
    cur_length: int = 0

    # Repeat steps 2-4 until the set of untreated states is empty
    while untreated and cur_length < max_length:

        #
        # Step 2
        #

        # Choose any untreated state s, remove it from the set. This will be
        # accomplished by popping the last element.
        s: state = untreated.pop()

        r: state = representative(s, cur_length)

        #
        # Step 3
        #

        # Construct all possible successors of the state by iterating through
        # all 4 possible directions. In each iteration, augment r by a single
        # step in the corresponding direction, leading to an augmented walk a.
        for a in symbols:
            t: state = augment(r, a)

            # If t is a state we have not seen so far, put it in the set of
            # untreated states
            untreated.add(t)

            # Put the transfer from s to t in the set of transfers
            transfers[(s, a)] = t

        #
        # Step 4
        #

        # Put state s into the set of treated states.
        # If the set of untreated states is not empty, go to 2;
        # otherwise, continue to 5.
        treated.add(s)

        cur_length += 1

    #
    # Step 5
    #

    # We have now collected all necessary states in the set of treated states
    # and all transfers in the set of transfers, thus the automaton is built.
    # As a result, the DFA can now be sent for processing to have its length
    # counted.
    # Send a JSON-formatted DFA to stdout for further processing
    # Format:
    """
    {
        "transitions":  [
                            [1,1,1,1],
                            [2,2,2,2],
                            [3,3,3,3],
                            [4,4,4,4],
                            [4,4,4,4]
                        ],
        "states":[0,1,2,3,4],
        "final":[4],
        "symbols":["a","b","c","d"],
        "start":0
    }
    """

    states: States = sorted(treated)
    transitions: TransitionTable = tabulate(states, symbols, transfers)

    return {
        "states": states,
        "symbols": symbols,
        "transitions": transitions,
        "start": start_state,
        "final": end_states
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} K")
        return 1

    # k is the size of our "memory" and the upper bound on the length of
    # strings accepted by the DFA
    k = int(sys.argv[1])
    dfa = construct_dfa(k)
    print(json.dumps(dfa))

    return 0

if __name__ == '__main__':
    exit(main())
