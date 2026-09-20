"""Compiler Design GATE Question Bank."""

QUESTIONS = [
    {
        "id": "cd_parse_001",
        "subject": "Compiler Design",
        "topic": "Syntax Analysis & Parsing",
        "subtopic": "FIRST & FOLLOW Set Calculations",
        "concept": "Computing FIRST and FOLLOW sets with epsilon productions",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Consider the following context-free grammar where S is the start symbol and ε denotes the empty string:\n\nS -> A B C\nA -> a | ε\nB -> b | ε\nC -> c | d\n\nHow many distinct terminal symbols are present in the set FIRST(S)?",
        "options": None,
        "answer": "4",
        "msq_answers": None,
        "explanation": "Let's compute FIRST sets:\n1. FIRST(A) = {a, ε}\n2. FIRST(B) = {b, ε}\n3. FIRST(C) = {c, d}\n\nFor S -> A B C:\n- FIRST(S) includes FIRST(A) \\ {ε} = {a}.\n- Since A can derive ε, FIRST(S) also includes FIRST(B) \\ {ε} = {b}.\n- Since both A and B can derive ε, FIRST(S) also includes FIRST(C) = {c, d}.\n- Since C cannot derive ε, S cannot derive ε.\nThus, FIRST(S) = {a, b, c, d}.\nThe number of distinct terminal symbols is 4.",
        "gate_trap": "Because A and B both have epsilon productions, FIRST(S) propagates through A and B to include symbols from C as well.",
        "key_concept": "FIRST(X1 X2 ... Xn) = FIRST(X1) \\ {ε} ∪ FIRST(X2) if ε ∈ FIRST(X1), and so on.",
        "reference_url": "https://www.geeksforgeeks.org/first-and-follow-in-compiler-design/"
    },
    {
        "id": "cd_lr_001",
        "subject": "Compiler Design",
        "topic": "Syntax Analysis & Parsing",
        "subtopic": "LR(0), SLR(1), LR(1), LALR(1) Item Sets",
        "concept": "Comparing parsing power of LR parser families (LR(0) vs SLR(1) vs LALR(1) vs CLR(1))",
        "type": "MSQ",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Which of the following statements regarding LR Parsers is/are TRUE?\n\nSelect all that apply:",
        "options": {
            "A": "Every SLR(1) grammar is also an LALR(1) grammar.",
            "B": "Every LALR(1) grammar is also a CLR(1) / LR(1) grammar.",
            "C": "LALR(1) parser has strictly fewer states than SLR(1) parser for the same grammar.",
            "D": "Merging states in CLR(1) to construct LALR(1) can never introduce Shift-Reduce (S-R) conflicts."
        },
        "answer": "A, B, D",
        "msq_answers": ["A", "B", "D"],
        "explanation": "- A is TRUE: Hierarchy of parsing power: LR(0) ⊂ SLR(1) ⊂ LALR(1) ⊂ CLR(1) ⊂ LL(k). Every SLR(1) grammar is LALR(1).\n- B is TRUE: Every LALR(1) grammar is CLR(1).\n- C is FALSE: LALR(1) has EXACTLY the SAME number of states as LR(0) and SLR(1) (states with same core items are merged).\n- D is TRUE: Merging states with identical cores can ONLY introduce Reduce-Reduce (R-R) conflicts, NEVER Shift-Reduce (S-R) conflicts.",
        "gate_trap": "LALR merging never produces Shift-Reduce conflicts (proven theorem in parsing theory); it can only introduce Reduce-Reduce conflicts.",
        "key_concept": "Parsing Power: LR(0) < SLR(1) < LALR(1) < CLR(1). Number of states: LR(0) = SLR(1) = LALR(1) < CLR(1).",
        "reference_url": "https://www.geeksforgeeks.org/classification-of-top-down-parsers/"
    }
]
