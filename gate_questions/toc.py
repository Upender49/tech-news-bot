"""Theory of Computation (TOC) GATE Question Bank."""

QUESTIONS = [
    {
        "id": "toc_dfa_001",
        "subject": "Theory of Computation",
        "topic": "Regular Languages & Finite Automata",
        "subtopic": "DFA Minimization & State Equivalence",
        "concept": "Minimum number of states in a DFA for divisibility conditions in binary",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "What is the MINIMUM number of states in a Deterministic Finite Automaton (DFA) that accepts the language L = { w in {0, 1}* | the binary value of w is divisible by 5 }? (Assume the empty string represents 0).",
        "options": None,
        "answer": "5",
        "msq_answers": None,
        "explanation": "To check if binary number is divisible by k=5:\n- When a new bit b in {0, 1} is appended to binary value V, the new value becomes V' = (2 * V + b) mod 5.\n- The possible remainders modulo 5 are {0, 1, 2, 3, 4} (5 distinct equivalence classes / states).\n- Start state = state 0 (remainder 0). Accepting state = state 0.\n- By Myhill-Nerode theorem, all 5 states are pairwise distinguishable. Thus, minimum states = 5.",
        "gate_trap": "For binary strings divisible by k, the minimum DFA has exactly k states (state 0 to k-1).",
        "key_concept": "Binary modulo k automaton requires exactly k states corresponding to remainders {0, 1, ..., k-1}.",
        "reference_url": "https://www.geeksforgeeks.org/dfa-accepting-binary-strings-divisible-by-number/"
    },
    {
        "id": "toc_cfl_001",
        "subject": "Theory of Computation",
        "topic": "Context-Free Languages & Pushdown Automata",
        "subtopic": "Closure & Decision Properties of CFLs",
        "concept": "Closure properties of Context-Free Languages vs Deterministic Context-Free Languages",
        "type": "MSQ",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Which of the following closure property statements is/are TRUE?\n\nSelect all that apply:",
        "options": {
            "A": "Context-Free Languages (CFL) are closed under Union and Concatenation.",
            "B": "Context-Free Languages (CFL) are closed under Intersection.",
            "C": "Deterministic Context-Free Languages (DCFL) are closed under Complement.",
            "D": "The intersection of a Context-Free Language (CFL) and a Regular Language is always Context-Free."
        },
        "answer": "A, C, D",
        "msq_answers": ["A", "C", "D"],
        "explanation": "- A is TRUE: CFLs are closed under Union, Concatenation, and Kleene Star.\n- B is FALSE: CFLs are NOT closed under Intersection (e.g. {a^n b^n c^m} ∩ {a^m b^n c^n} = {a^n b^n c^n} which is non-CFL).\n- C is TRUE: DCFLs are closed under Complement (by swapping accepting and non-accepting states in a DPDA with trap states).\n- D is TRUE: CFL ∩ Regular = CFL (construct product PDA x DFA).",
        "gate_trap": "CFL is NOT closed under complement or intersection, but DCFL IS closed under complement!",
        "key_concept": "CFLs are closed under Union, Concatenation, Kleene star, and Intersection with Regular languages. DCFLs are closed under Complement.",
        "reference_url": "https://www.geeksforgeeks.org/closure-properties-of-context-free-languages/"
    },
    {
        "id": "toc_undec_001",
        "subject": "Theory of Computation",
        "topic": "Turing Machines & Undecidability",
        "subtopic": "Rice's Theorem & Reductions",
        "concept": "Applying Rice's Theorem to non-trivial semantic properties of Turing Machine languages",
        "type": "MCQ",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Let <M> denote the encoding of a Turing Machine M. Which of the following decision problems is DECIDABLE?",
        "options": {
            "A": "Given <M>, is L(M) empty?",
            "B": "Given <M>, is L(M) regular?",
            "C": "Given <M>, does M have at most 10 states?",
            "D": "Given <M> and a string w, does M accept w?"
        },
        "answer": "C",
        "msq_answers": None,
        "explanation": "- A, B, D are semantic properties of the language recognized by Turing Machines L(M). By Rice's Theorem (Part 1), any non-trivial semantic property of Recursively Enumerable languages is Undecidable. (A is Emptiness, B is Regularity, D is Membership/Halting).\n- C is a SYNTACTIC property of the machine encoding itself (counting states in <M>), which is easily checked by parsing the string <M>. Hence C is Decidable.",
        "gate_trap": "Rice's Theorem applies strictly to SEMANTIC properties of the language L(M), NOT syntactic properties of the Turing machine's description/states.",
        "key_concept": "Semantic language properties of TM are Undecidable (Rice's Theorem); Structural/syntactic properties of TM encoding are Decidable.",
        "reference_url": "https://www.geeksforgeeks.org/rices-theorem-in-theory-of-computation/"
    }
]
