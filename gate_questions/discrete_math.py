"""Discrete Mathematics GATE Question Bank."""

QUESTIONS = [
    {
        "id": "dm_graph_001",
        "subject": "Discrete Mathematics",
        "topic": "Graph Theory",
        "subtopic": "Planar Graphs & Euler's Formula",
        "concept": "Euler's planar formula and maximum edges in connected planar graphs",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Let G be a simple connected planar graph with 20 vertices and each face bounded by at least 4 edges. What is the MAXIMUM number of edges G can have?",
        "options": None,
        "answer": "36",
        "msq_answers": None,
        "explanation": "For any planar graph with V vertices, E edges, and F faces:\n1. Euler's formula: V - E + F = 2 ⟹ F = E - V + 2 = E - 20 + 2 = E - 18.\n2. Since each face is bounded by at least 4 edges, by handshaking on faces:\n   2 * E >= 4 * F\n   2 * E >= 4 * (E - 18)\n   2 * E >= 4 * E - 72\n   2 * E <= 72 ⟹ E <= 36.\nTherefore, the maximum number of edges is 36.",
        "gate_trap": "The standard formula E <= 3V - 6 applies only when faces can be triangles (girth = 3). When face length is at least 4, use 2E >= k*F to derive E <= 2V - 4.",
        "key_concept": "For a planar graph where each face degree >= k: 2E >= k*F. Combined with V - E + F = 2 gives E <= (k / (k-2)) * (V - 2).",
        "reference_url": "https://www.geeksforgeeks.org/euler-formula-for-planar-graphs/"
    },
    {
        "id": "dm_logic_001",
        "subject": "Discrete Mathematics",
        "topic": "Mathematical Logic",
        "subtopic": "Propositional Logic & Equivalence",
        "concept": "Tautology and logical implication validity",
        "type": "MSQ",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Let P, Q, and R be propositional logic variables. Which of the following formulas is/are TAUTOLOGIES?\n\nSelect all that apply:",
        "options": {
            "A": "((P -> Q) ∧ (Q -> R)) -> (P -> R)",
            "B": "(P ∧ (P -> Q)) -> Q",
            "C": "(P -> Q) <-> (~P ∨ Q)",
            "D": "(P -> (Q ∧ R)) <-> ((P -> Q) ∧ (P -> R))"
        },
        "answer": "A, B, C, D",
        "msq_answers": ["A", "B", "C", "D"],
        "explanation": "- A is Hypothetical Syllogism (transitivity of implication): Always true (Tautology).\n- B is Modus Ponens: Always true (Tautology).\n- C is Implication Definition / Equivalence: P -> Q is logically equivalent to ~P ∨ Q, so equivalence is a Tautology.\n- D is Distributivity of Implication over Conjunction: P -> (Q ∧ R) ≡ (~P ∨ (Q ∧ R)) ≡ (~P ∨ Q) ∧ (~P ∨ R) ≡ (P -> Q) ∧ (P -> R). Always true (Tautology).\nAll 4 options are valid tautologies.",
        "gate_trap": "In GATE MSQs, ALL options can be correct. Don't second-guess simply because all four are valid.",
        "key_concept": "Modus Ponens, Hypothetical Syllogism, and Implication Equivalences are fundamental classical tautologies.",
        "reference_url": "https://www.geeksforgeeks.org/proposition-logic/"
    },
    {
        "id": "dm_comb_001",
        "subject": "Discrete Mathematics",
        "topic": "Combinatorics",
        "subtopic": "Counting Principles & Pigeonhole Principle",
        "concept": "Pigeonhole Principle in subset sum divisibility",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "What is the MINIMUM number of integers that must be chosen from the set S = {1, 2, 3, ..., 100} to guarantee that at least one pair of chosen integers has a sum equal to 101?",
        "options": None,
        "answer": "51",
        "msq_answers": None,
        "explanation": "We can pair up the numbers from 1 to 100 such that each pair sums to 101:\nPairs: (1, 100), (2, 99), (3, 98), ..., (50, 51).\nTotal number of disjoint pairs (pigeonholes) = 50.\nIn the worst case, we can pick at most 1 element from each of the 50 pairs without having any pair complete (50 numbers chosen).\nBy the Pigeonhole Principle, choosing 50 + 1 = 51 numbers guarantees that at least two numbers must come from the same pair, making their sum 101.",
        "gate_trap": "Worst-case picking takes 1 element per hole. The guarantee requires 1 more than the total number of non-overlapping target pairs.",
        "key_concept": "Pigeonhole Principle: To guarantee a pair sum from k complementary pairs, choose k + 1 elements.",
        "reference_url": "https://www.geeksforgeeks.org/pigeonhole-principle/"
    }
]
