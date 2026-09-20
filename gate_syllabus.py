"""Official GATE CSE & IT Syllabus Tree and Topic Weights.

Source of Truth: GATE Official Syllabus & 2018-2025 Historical Weightage Analysis.
"""

GATE_SYLLABUS = {
    "General Aptitude": {
        "weight": 15.0,
        "tier": 0,  # Compulsory in every single session
        "topics": {
            "Verbal Aptitude": [
                "Basic English Grammar", "Tenses & Articles", "Subject-Verb Agreement",
                "Vocabulary & Words in Context", "Idioms & Phrases", "Reading Comprehension",
                "Narrative Sequencing"
            ],
            "Quantitative Aptitude": [
                "Ratios & Percentages", "Powers, Exponents & Logarithms",
                "Permutations & Combinations", "Series & Progressions",
                "Mensuration & Geometry", "Elementary Statistics & Probability",
                "Data Interpretation (Tables & Graphs)"
            ],
            "Analytical Aptitude": [
                "Logic & Syllogisms", "Deductive & Inductive Reasoning",
                "Word & Concept Analogies", "Numerical Relations & Reasoning",
                "Seating Arrangements & Blood Relations"
            ],
            "Spatial Aptitude": [
                "Translation & Rotation of Shapes", "Scaling & Mirroring",
                "Assembling & Grouping 2D/3D Shapes", "Paper Folding & Paper Cutting",
                "2D & 3D Pattern Spotting"
            ]
        }
    },
    "Programming & Data Structures": {
        "weight": 9.75,
        "tier": 1,
        "topics": {
            "Programming in C": [
                "Data Types & Operators Precedence", "Control Structures & Loops",
                "Functions & Parameter Passing", "Pointers & Pointer Arithmetic",
                "Dynamic Memory Allocation", "Structures, Unions & Enums", "Recursion"
            ],
            "Linear Data Structures": [
                "Arrays & Address Calculation", "Stacks & Applications (Infix/Postfix)",
                "Queues (Circular, Priority, Deque)", "Linked Lists (Singly, Doubly, Circular)"
            ],
            "Non-Linear Data Structures": [
                "Binary Trees & Traversals", "Binary Search Trees (BST)",
                "AVL Trees & Tree Balance", "Binary Heaps & Priority Queues",
                "Graph Representations & Traversals (BFS/DFS)"
            ]
        }
    },
    "Computer Organization & Architecture": {
        "weight": 9.4,
        "tier": 1,
        "topics": {
            "Machine Instructions & Addressing": [
                "Instruction Formats & Opcode Encoding", "Addressing Modes",
                "RISC vs CISC Architecture"
            ],
            "ALU, Data-Path & Control Unit": [
                "Data-Path Design", "Hardwired vs Microprogrammed Control",
                "Control Hazards & Branch Handling"
            ],
            "Instruction Pipelining": [
                "Pipeline Stages & Throughput Calculation", "Structural, Data & Control Hazards",
                "Branch Penalty & Forwarding Speedup"
            ],
            "Memory Hierarchy": [
                "Cache Mapping (Direct, Associative, Set-Associative)",
                "Cache Write Policies & Hit/Miss Latency", "Multi-Level Cache Calculations",
                "Main Memory Interleaving & DRAM/SRAM", "Secondary Storage & Disk Scheduling"
            ],
            "I/O Interface": [
                "Programmed I/O vs Interrupt-Driven I/O", "Direct Memory Access (DMA)"
            ]
        }
    },
    "Operating Systems": {
        "weight": 8.75,
        "tier": 1,
        "topics": {
            "Processes & Threads": [
                "Process States & PCB", "Context Switching Overhead",
                "User-Level vs Kernel-Level Threads", "System Calls (fork, exec, wait, exit)"
            ],
            "CPU Scheduling": [
                "FCFS, SJF, SRTF Scheduling", "Round Robin & Multilevel Queue",
                "Waiting Time & Turnaround Time Calculations"
            ],
            "Concurrency & Synchronization": [
                "Critical Section Problem & Peterson's Solution",
                "Counting & Binary Semaphores", "Mutexes & Monitors",
                "Classic Problems (Producer-Consumer, Readers-Writers)"
            ],
            "Deadlocks": [
                "4 Coffman Conditions", "Resource Allocation Graph (RAG)",
                "Deadlock Avoidance & Banker's Algorithm", "Deadlock Prevention & Detection"
            ],
            "Memory Management & Virtual Memory": [
                "Contiguous Allocation & Fragmentation", "Paging & Multi-Level Page Tables",
                "TLB & Effective Memory Access Time", "Segmentation",
                "Demand Paging & Page Replacement (FIFO, LRU, Optimal, Clock)",
                "Belady's Anomaly & Thrashing"
            ],
            "File Systems & Disk Scheduling": [
                "File Allocation (Contiguous, Linked, Inode)",
                "Disk Scheduling (FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK)"
            ]
        }
    },
    "Discrete Mathematics": {
        "weight": 8.4,
        "tier": 1,
        "topics": {
            "Mathematical Logic": [
                "Propositional Logic & Equivalence", "First-Order Predicate Logic & Quantifiers",
                "Inference Rules & Tautologies"
            ],
            "Set Theory & Algebra": [
                "Sets, Subsets & Power Sets", "Relations & Equivalence Classes",
                "Functions (Injective, Surjective, Bijective)",
                "Partial Orders, Hasse Diagrams & Lattices", "Groups, Subgroups & Abelian Groups"
            ],
            "Combinatorics": [
                "Counting Principles & Pigeonhole Principle",
                "Permutations, Combinations & Binomial Coefficients",
                "Generating Functions & Recurrence Relations"
            ],
            "Graph Theory": [
                "Degrees & Handshaking Lemma", "Paths, Cycles, Eulerian & Hamiltonian Graphs",
                "Planar Graphs & Euler's Formula", "Graph Coloring & Chromatic Number",
                "Trees, Spanning Trees & Tree Properties"
            ]
        }
    },
    "Computer Networks": {
        "weight": 8.25,
        "tier": 2,
        "topics": {
            "Layering & Physical Layer": [
                "OSI & TCP/IP Reference Models", "Transmission, Propagation & Queuing Delays",
                "Bandwidth-Delay Product & Packet Switching"
            ],
            "Data Link Layer": [
                "Framing & CRC Error Detection", "Stop-and-Wait, Go-Back-N, Selective Repeat",
                "Flow & Error Control Efficiency", "CSMA/CD & Minimum Frame Size Calculation",
                "Binary Exponential Backoff & Pure/Slotted ALOHA"
            ],
            "Network Layer & IP Addressing": [
                "IPv4 Addressing & CIDR Subnetting", "Subnet Masking & Usable Hosts",
                "IPv4 Header Fields & Fragmentation Calculations",
                "Routing Protocols (Distance Vector, Link State, BGP)",
                "ARP, DHCP, ICMP, NAT"
            ],
            "Transport Layer": [
                "TCP vs UDP Comparison", "TCP 3-Way Handshake & Connection Teardown",
                "TCP Congestion Control (Slow Start, AIMD, Fast Retransmit)",
                "Flow Control & Sliding Window"
            ],
            "Application Layer & Security": [
                "DNS, HTTP, SMTP, FTP Protocols",
                "RSA Cryptography & Digital Signatures Basics"
            ]
        }
    },
    "Theory of Computation": {
        "weight": 8.0,
        "tier": 2,
        "topics": {
            "Regular Languages & Finite Automata": [
                "DFA & NFA Design", "DFA Minimization & State Equivalence",
                "Regular Expressions & Arden's Theorem", "Pumping Lemma for Regular Languages",
                "Closure & Decision Properties of Regular Languages"
            ],
            "Context-Free Languages & Pushdown Automata": [
                "Context-Free Grammars (CFG) & Ambiguity", "Chomsky Normal Form (CNF)",
                "Pushdown Automata (DPDA vs NPDA)", "Pumping Lemma for CFLs",
                "Closure & Decision Properties of CFLs"
            ],
            "Turing Machines & Undecidability": [
                "Turing Machines (TM) & Halting Problem",
                "Recursive (REC) vs Recursively Enumerable (RE)",
                "Rice's Theorem & Reductions", "Post Correspondence Problem (PCP)"
            ]
        }
    },
    "Algorithms": {
        "weight": 8.0,
        "tier": 2,
        "topics": {
            "Asymptotic Analysis & Recurrences": [
                "Big-O, Omega, Theta Notations", "Master Theorem & Recurrence Relations",
                "Complexity Comparison of Functions"
            ],
            "Searching, Sorting & Hashing": [
                "Sorting Algorithms (Merge, Quick, Heap, Counting)",
                "Time & Space Bounds, Stability & In-Place Analysis",
                "Hash Tables, Open Addressing & Collision Resolution"
            ],
            "Divide-and-Conquer & Greedy": [
                "Divide-and-Conquer Recurrences & Applications",
                "Activity Selection & Fractional Knapsack", "Huffman Coding & Tree Construction"
            ],
            "Dynamic Programming": [
                "0/1 Knapsack & Subset Sum", "Longest Common Subsequence (LCS)",
                "Matrix Chain Multiplication (MCM)", "Optimal Binary Search Trees"
            ],
            "Graph Algorithms": [
                "BFS & DFS Applications & Topological Sort",
                "Minimum Spanning Trees (Prim's & Kruskal's with DSU)",
                "Single-Source Shortest Paths (Dijkstra, Bellman-Ford)",
                "All-Pairs Shortest Path (Floyd-Warshall)"
            ]
        }
    },
    "Databases (DBMS)": {
        "weight": 7.25,
        "tier": 2,
        "topics": {
            "ER Model & Relational Model": [
                "ER Diagram to Relational Schema Conversion", "Relational Integrity Constraints",
                "Relational Algebra Operations & Queries", "Tuple & Domain Relational Calculus"
            ],
            "SQL Querying": [
                "Nested Subqueries & Correlated Queries", "Joins & Aggregate Functions",
                "GROUP BY & HAVING Clauses"
            ],
            "Normalization & Functional Dependencies": [
                "Attribute Closure & Candidate Keys", "Minimal Cover & Superkeys",
                "1NF, 2NF, 3NF, BCNF Decomposition", "Lossless Join & Dependency Preservation"
            ],
            "Transactions & Concurrency Control": [
                "ACID Properties & Transaction States",
                "Conflict Serializability & Precedence Graphs",
                "View Serializability & Recoverability",
                "Two-Phase Locking (2PL, Strict, Rigorous)",
                "Timestamp Ordering Protocol & WAL (Write-Ahead Logging)"
            ],
            "File Organization & Indexing": [
                "Primary, Secondary & Clustering Index",
                "B-Trees & B+ Trees (Order, Height, Node Calculations)"
            ]
        }
    },
    "Engineering Mathematics": {
        "weight": 5.75,
        "tier": 3,
        "topics": {
            "Linear Algebra": [
                "Matrices, Determinants & Rank", "Systems of Linear Equations (Ax = b)",
                "Eigenvalues & Eigenvectors", "Cayley-Hamilton Theorem & Matrix Powers",
                "LU Decomposition"
            ],
            "Calculus": [
                "Limits, Continuity & Differentiability", "Mean Value Theorems (Rolle's, Lagrange's)",
                "Maxima, Minima & Saddle Points", "Definite & Indefinite Integrals"
            ],
            "Probability & Statistics": [
                "Conditional Probability & Bayes' Theorem", "Independent & Mutually Exclusive Events",
                "Random Variables (PMF, PDF, CDF)",
                "Uniform, Exponential, Poisson, Normal, Binomial Distributions",
                "Expectation, Variance & Standard Deviation"
            ]
        }
    },
    "Compiler Design": {
        "weight": 5.5,
        "tier": 3,
        "topics": {
            "Lexical Analysis": [
                "Tokens, Lexemes, Patterns & Regular Expressions", "Input Buffering & Lexical Errors"
            ],
            "Syntax Analysis & Parsing": [
                "FIRST & FOLLOW Set Calculations", "LL(1) Parsing Table & Conflict Detection",
                "LR(0), SLR(1), LR(1), LALR(1) Item Sets", "Shift-Reduce & Reduce-Reduce Conflicts",
                "Operator Precedence Parsing"
            ],
            "Syntax-Directed Translation (SDT)": [
                "S-Attributed vs L-Attributed Definitions", "Evaluation Orders & Parse Tree Annotation"
            ],
            "Intermediate Code & Optimization": [
                "Three-Address Code & Control Flow Translation",
                "Basic Blocks & Control Flow Graphs (CFG)",
                "Data Flow Analysis (Liveness, Constant Propagation)",
                "Common Subexpression & Dead Code Elimination"
            ],
            "Runtime Environments": [
                "Activation Records & Stack Allocation", "Parameter Passing Mechanisms"
            ]
        }
    },
    "Digital Logic": {
        "weight": 5.0,
        "tier": 3,
        "topics": {
            "Boolean Algebra & Minimization": [
                "Logic Gates & Boolean Laws", "Canonical SOP & POS Forms",
                "K-Maps Minimization (Up to 5 variables)", "Prime Implicants & Essential Prime Implicants"
            ],
            "Combinational Circuits": [
                "Half / Full Adders & Lookahead Carry", "Multiplexers (MUX) & Demultiplexers",
                "Encoders, Decoders & Code Converters"
            ],
            "Sequential Circuits": [
                "Latches & Flip-Flops (SR, JK, D, T)", "Flip-Flop Conversions & Timing",
                "Synchronous & Asynchronous Counters", "Shift Registers & State Diagrams"
            ],
            "Number Representations": [
                "1's Complement & 2's Complement Arithmetic", "Overflow Detection in Binary Additions",
                "IEEE 754 Floating-Point Standard (Single & Double Precision)"
            ]
        }
    }
}
