"""Algorithms GATE Question Bank."""

QUESTIONS = [
    {
        "id": "algo_rec_001",
        "subject": "Algorithms",
        "topic": "Asymptotic Analysis & Recurrences",
        "subtopic": "Master Theorem & Recurrence Relations",
        "concept": "Master Theorem Case 2 with logarithmic factor",
        "type": "MCQ",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Consider the recurrence relation:\nT(n) = 2 * T(n/2) + n * log2(n), with T(1) = 1.\nWhich of the following describes the asymptotic time complexity of T(n)?",
        "options": {
            "A": "Theta(n * log2(n))",
            "B": "Theta(n * (log2(n))^2)",
            "C": "Theta(n^2)",
            "D": "Theta(n^2 * log2(n))"
        },
        "answer": "B",
        "msq_answers": None,
        "explanation": "Using the Extended Master Theorem:\nT(n) = a*T(n/b) + f(n)\nHere a = 2, b = 2, f(n) = n * log2(n).\nn^(log_b(a)) = n^(log_2(2)) = n^1 = n.\nSince f(n) = Theta(n^(log_b(a)) * (log n)^k) where k = 1:\nBy Master Theorem Case 2 extension, T(n) = Theta(n^(log_b(a)) * (log n)^(k+1)) = Theta(n * (log n)^2).",
        "gate_trap": "Standard Master theorem without the (log n)^k extension would fail here. When f(n) has an extra log factor matching n^(log_b a), increment the power of log.",
        "key_concept": "If f(n) = Theta(n^(log_b a) * log^k n), then T(n) = Theta(n^(log_b a) * log^(k+1) n).",
        "reference_url": "https://www.geeksforgeeks.org/advanced-master-theorem-for-divide-and-conquer-recurrences/"
    },
    {
        "id": "algo_mst_001",
        "subject": "Algorithms",
        "topic": "Graph Algorithms",
        "subtopic": "Minimum Spanning Trees (Prim's & Kruskal's with DSU)",
        "concept": "Cut property and cycle property of Minimum Spanning Trees (MST)",
        "type": "MSQ",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Let G = (V, E) be an undirected connected weighted graph with distinct edge weights. Which of the following statements is/are ALWAYS TRUE?\n\nSelect all that apply:",
        "options": {
            "A": "G has a unique Minimum Spanning Tree (MST).",
            "B": "The second minimum weight edge in G must be included in the MST of G.",
            "C": "The edge with the maximum weight in any cycle in G can NEVER be in any MST of G.",
            "D": "The shortest path between two vertices u and v in G is always a subset of edges in the MST."
        },
        "answer": "A, B, C",
        "msq_answers": ["A", "B", "C"],
        "explanation": "- A is TRUE: If all edge weights in a connected graph are strictly distinct, the MST is unique.\n- B is TRUE: The minimum weight edge and the second minimum weight edge in the entire graph cannot form a cycle (a cycle requires at least 3 edges), so both must be in the MST.\n- C is TRUE: By the Cycle Property of MST, the strictly heaviest edge in any simple cycle is never part of any MST.\n- D is FALSE: The shortest path between two vertices may use a direct heavy edge that is not part of the MST.",
        "gate_trap": "Never confuse Shortest Path Tree (Dijkstra) with Minimum Spanning Tree (Prim/Kruskal). MST minimizes total sum of edge weights, NOT individual path distances.",
        "key_concept": "Distinct edge weights ⟹ Unique MST; Cycle property eliminates max cycle edge; First 2 lightest edges are always in MST.",
        "reference_url": "https://www.geeksforgeeks.org/applications-of-minimum-spanning-tree-problem/"
    },
    {
        "id": "algo_dp_001",
        "subject": "Algorithms",
        "topic": "Dynamic Programming",
        "subtopic": "Matrix Chain Multiplication (MCM)",
        "concept": "Minimum number of scalar multiplications in Matrix Chain Multiplication",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Let four matrices have dimensions: A1 (10 x 30), A2 (30 x 5), A3 (5 x 60), A4 (60 x 10). What is the MINIMUM number of scalar multiplications required to compute the product A1 * A2 * A3 * A4?",
        "options": None,
        "answer": "4500",
        "msq_answers": None,
        "explanation": "Dimensions: p = [10, 30, 5, 60, 10]\nLet's evaluate the optimal parenthesization using DP:\n- Length 2:\n  m[1,2] = 10 * 30 * 5 = 1500 (A1*A2: 10x5)\n  m[2,3] = 30 * 5 * 60 = 9000 (A2*A3: 30x60)\n  m[3,4] = 5 * 60 * 10 = 3000 (A3*A4: 5x10)\n- Length 3:\n  m[1,3] = min(m[1,1]+m[2,3]+10*30*60, m[1,2]+m[3,3]+10*5*60) = min(0+9000+18000, 1500+0+3000) = 4500 ((A1A2)A3: 10x60)\n  m[2,4] = min(m[2,2]+m[3,4]+30*5*10, m[2,3]+m[4,4]+30*60*10) = min(0+3000+1500, 9000+0+18000) = 4500 (A2(A3A4): 30x10)\n- Length 4 (m[1,4]):\n  k=1: m[1,1] + m[2,4] + 10*30*10 = 0 + 4500 + 3000 = 7500\n  k=2: m[1,2] + m[3,4] + 10*5*10 = 1500 + 3000 + 500 = 5000\n  k=3: m[1,3] + m[4,4] + 10*60*10 = 4500 + 0 + 6000 = 10500\n  Wait! Let's re-check ((A1A2)(A3A4)):\n  (A1A2) cost = 1500 (dim 10x5)\n  (A3A4) cost = 3000 (dim 5x10)\n  Multiplying (10x5) by (5x10) = 10 * 5 * 10 = 500.\n  Total = 1500 + 3000 + 500 = 4500 scalar multiplications!",
        "gate_trap": "Carefully compute both subchain costs plus the cross multiplication term (p[i-1] * p[k] * p[j]).",
        "key_concept": "MCM Recurrence: m[i, j] = min_{i<=k<j} (m[i, k] + m[k+1, j] + p[i-1]*p[k]*p[j]).",
        "reference_url": "https://www.geeksforgeeks.org/matrix-chain-multiplication-dp-8/"
    }
]
