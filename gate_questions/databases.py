"""Databases (DBMS) GATE Question Bank."""

QUESTIONS = [
    {
        "id": "db_norm_001",
        "subject": "Databases (DBMS)",
        "topic": "Normalization & Functional Dependencies",
        "subtopic": "Attribute Closure & Candidate Keys",
        "concept": "Finding all candidate keys of a relational schema",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Consider a relation schema R(A, B, C, D, E) with the following set of functional dependencies:\nF = { A -> BC, CD -> E, B -> D, E -> A }\nHow many CANDIDATE KEYS does relation R have?",
        "options": None,
        "answer": "4",
        "msq_answers": None,
        "explanation": "Let's find the attribute closures:\n1. Check attributes that never appear on the RHS: None (all A, B, C, D, E appear on RHS).\n2. (A)+ = {A, B, C, D, E} ⟹ A is a candidate key.\n3. Since E -> A: (E)+ = {E, A, B, C, D} ⟹ E is a candidate key.\n4. Since CD -> E: (CD)+ = {C, D, E, A, B} ⟹ CD is a candidate key. (Neither C+ nor D+ is a key).\n5. Since B -> D: (BC)+ = (B, C, D, E, A) ⟹ BC is a candidate key. (Neither B+ nor C+ is a key).\nCandidate keys = { A, E, CD, BC }.\nTotal candidate keys = 4.",
        "gate_trap": "Don't forget composite candidate keys like BC and CD that derive the full attribute set via transitivity.",
        "key_concept": "A candidate key is a minimal superkey whose attribute closure determines all attributes in the relation.",
        "reference_url": "https://www.geeksforgeeks.org/finding-attribute-closure-and-candidate-keys-using-functional-dependencies/"
    },
    {
        "id": "db_serial_001",
        "subject": "Databases (DBMS)",
        "topic": "Transactions & Concurrency Control",
        "subtopic": "Conflict Serializability & Precedence Graphs",
        "concept": "Testing conflict serializability using precedence/serialization graphs",
        "type": "MCQ",
        "marks": 1,
        "difficulty": "medium",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Consider the schedule S with transactions T1, T2, T3:\nS: r1(X); r2(Y); r3(X); w1(X); r2(X); w2(Y); w3(X);\nWhich of the following is the correct serialization order equivalent to S?",
        "options": {
            "A": "T1 -> T2 -> T3",
            "B": "T3 -> T1 -> T2",
            "C": "Schedule S is NOT conflict serializable",
            "D": "T2 -> T1 -> T3"
        },
        "answer": "C",
        "msq_answers": None,
        "explanation": "Let's construct the Precedence Graph (conflicting operations on same item by different transactions):\n1. r3(X) is before w1(X) ⟹ Edge T3 -> T1.\n2. w1(X) is before w3(X) ⟹ Edge T1 -> T3.\n3. Edges T3 -> T1 and T1 -> T3 form a cycle of length 2 between T1 and T3!\nSince the precedence graph contains a cycle, schedule S is NOT conflict serializable.",
        "gate_trap": "r3(X) precedes w1(X), creating T3 -> T1, and w1(X) precedes w3(X), creating T1 -> T3. The cycle immediately rules out conflict serializability.",
        "key_concept": "A schedule is conflict serializable iff its precedence (serialization) graph has NO cycles.",
        "reference_url": "https://www.geeksforgeeks.org/conflict-serializability-in-dbms/"
    },
    {
        "id": "db_btree_001",
        "subject": "Databases (DBMS)",
        "topic": "File Organization & Indexing",
        "subtopic": "B-Trees & B+ Trees (Order, Height, Node Calculations)",
        "concept": "Order calculation of a B+ tree node to fit in a disk block",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "A B+ tree index is to be constructed on a relation. The disk block size is 512 bytes. Each search key is 8 bytes long and each block pointer is 6 bytes long. What is the MAXIMUM order (maximum number of block pointers) of an INTERNAL node in this B+ tree?",
        "options": None,
        "answer": "37",
        "msq_answers": None,
        "explanation": "Let 'p' be the order (number of block pointers) of an internal node.\nAn internal node of order p contains:\n- p block pointers (each of size P = 6 bytes)\n- (p - 1) search keys (each of size K = 8 bytes)\n\nThe node must fit inside a single disk block of 512 bytes:\np * P + (p - 1) * K <= Block Size\np * 6 + (p - 1) * 8 <= 512\n6p + 8p - 8 <= 512\n14p <= 520\np <= 520 / 14 = 37.1428...\nSince order p must be an integer, p_max = 37.",
        "gate_trap": "An internal node has (p - 1) keys for p pointers. Don't use p keys for p pointers.",
        "key_concept": "Internal B+ Tree Node Constraint: p * (Pointer_Size) + (p - 1) * (Key_Size) <= Block_Size.",
        "reference_url": "https://www.geeksforgeeks.org/b-tree-set-1-introduction-2/"
    }
]
