"""Digital Logic GATE Question Bank."""

QUESTIONS = [
    {
        "id": "dl_kmap_001",
        "subject": "Digital Logic",
        "topic": "Boolean Algebra & Minimization",
        "subtopic": "K-Maps Minimization (Up to 5 variables)",
        "concept": "Essential Prime Implicants determination in 4-variable K-map",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Consider the Boolean function F(A, B, C, D) given by the sum of minterms:\nF(A, B, C, D) = Σm(0, 2, 5, 7, 8, 10, 13, 15)\nHow many ESSENTIAL PRIME IMPLICANTS (EPI) does function F have?",
        "options": None,
        "answer": "2",
        "msq_answers": None,
        "explanation": "Let's group the minterms in 4-variable K-Map (A, B, C, D):\n1. Group 1 (Four corners): m(0, 2, 8, 10) ⟹ B' D'.\n   - Covers minterms 0, 2, 8, 10.\n   - Minterm 0 is only covered by this group. Hence B'D' is an ESSENTIAL Prime Implicant.\n2. Group 2 (Center quad): m(5, 7, 13, 15) ⟹ B D.\n   - Covers minterms 5, 7, 13, 15.\n   - Minterm 5 is only covered by this group. Hence BD is an ESSENTIAL Prime Implicant.\nAll minterms are covered by these two groups.\nTotal Essential Prime Implicants (EPI) = 2.",
        "gate_trap": "A Prime Implicant is ESSENTIAL if and only if it covers at least one minterm that is not covered by any other prime implicant.",
        "key_concept": "EPI Identification: Every minterm uniquely covered by a single prime implicant establishes that PI as Essential.",
        "reference_url": "https://www.geeksforgeeks.org/prime-implicant-and-essential-prime-implicants/"
    },
    {
        "id": "dl_float_001",
        "subject": "Digital Logic",
        "topic": "Number Representations",
        "subtopic": "IEEE 754 Floating-Point Standard (Single & Double Precision)",
        "concept": "IEEE 754 single precision floating point representation decoding",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "The 32-bit IEEE 754 single-precision representation of a floating-point number is given in hexadecimal as 0xC1480000. What is the decimal value represented by this number?",
        "options": None,
        "answer": "-12.5",
        "msq_answers": None,
        "explanation": "Hexadecimal: 0xC1480000\nBinary:\n1100 0001 0100 1000 0000 0000 0000 0000\n\n1. Sign bit (1 bit): 1 ⟹ Negative number.\n2. Exponent (8 bits): 1000 0010_2 = 130_10.\n   Actual exponent E = Exponent - Bias = 130 - 127 = 3.\n3. Mantissa / Fraction (23 bits): 100 1000 0000... = 2^(-1) + 2^(-4) = 0.5 + 0.0625 = 0.5625.\n4. Normalized Significand = 1 + Fraction = 1.5625.\n5. Value = (-1)^Sign * (1.Fraction) * 2^E\n   Value = -1 * 1.5625 * 2^3 = -1 * 1.5625 * 8 = -12.5.",
        "gate_trap": "Remember the implicit leading 1 for normalized IEEE 754 floats: Significand is (1 + Mantissa), and Bias for single precision is 127.",
        "key_concept": "IEEE 754 Single Precision: Value = (-1)^S * (1.M) * 2^(E - 127).",
        "reference_url": "https://www.geeksforgeeks.org/ieee-standard-754-floating-point-numbers/"
    }
]
