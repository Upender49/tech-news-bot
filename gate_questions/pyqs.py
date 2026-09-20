"""Verified GATE Previous Year Questions (PYQs) with strict official metadata."""

PYQS = [
    {
        "id": "pyq_gate2022_os_01",
        "subject": "Operating Systems",
        "topic": "Memory Management & Virtual Memory",
        "subtopic": "Demand Paging & Page Replacement (FIFO, LRU, Optimal, Clock)",
        "concept": "Page faults in FIFO page replacement with 3 frames",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE PYQ — 2022",
        "pyq_year": 2022,
        "q": "📌 GATE CSE 2022\nConsider a system with 3 page frames initially empty. The page reference string is:\n1, 2, 3, 4, 2, 1, 5, 6, 2, 1, 2, 3, 7, 6, 3, 2, 1, 2, 3, 6\nHow many PAGE FAULTS occur using the First-In First-Out (FIFO) page replacement algorithm?",
        "options": None,
        "answer": "16",
        "msq_answers": None,
        "explanation": "Let's trace 3 frames under FIFO:\n- Ref 1: Miss [1, -, -] (Fault 1)\n- Ref 2: Miss [1, 2, -] (Fault 2)\n- Ref 3: Miss [1, 2, 3] (Fault 3)\n- Ref 4: Miss, replace 1 [4, 2, 3] (Fault 4)\n- Ref 2: Hit [4, 2, 3]\n- Ref 1: Miss, replace 2 [4, 1, 3] (Fault 5)\n- Ref 5: Miss, replace 3 [4, 1, 5] (Fault 6)\n- Ref 6: Miss, replace 4 [6, 1, 5] (Fault 7)\n- Ref 2: Miss, replace 1 [6, 2, 5] (Fault 8)\n- Ref 1: Miss, replace 5 [6, 2, 1] (Fault 9)\n- Ref 2: Hit [6, 2, 1]\n- Ref 3: Miss, replace 6 [3, 2, 1] (Fault 10)\n- Ref 7: Miss, replace 2 [3, 7, 1] (Fault 11)\n- Ref 6: Miss, replace 1 [3, 7, 6] (Fault 12)\n- Ref 3: Hit [3, 7, 6]\n- Ref 2: Miss, replace 3 [2, 7, 6] (Fault 13)\n- Ref 1: Miss, replace 7 [2, 1, 6] (Fault 14)\n- Ref 2: Hit [2, 1, 6]\n- Ref 3: Miss, replace 6 [2, 1, 3] (Fault 15)\n- Ref 6: Miss, replace 2 [6, 1, 3] (Fault 16)\nTotal Page Faults = 16.",
        "gate_trap": "In FIFO, replacement order is governed strictly by the entry timestamp of the page frame, regardless of how recently it was accessed.",
        "key_concept": "FIFO tracks the oldest loaded frame in the circular queue and evicts it on a miss.",
        "reference_url": "https://www.geeksforgeeks.org/page-replacement-algorithms-in-operating-systems/"
    },
    {
        "id": "pyq_gate2021_dsa_01",
        "subject": "Programming & Data Structures",
        "topic": "Non-Linear Data Structures",
        "subtopic": "Binary Heaps & Priority Queues",
        "concept": "Minimum number of comparisons to find the minimum in a Max-Heap",
        "type": "NAT",
        "marks": 1,
        "difficulty": "gate",
        "source": "GATE PYQ — 2021",
        "pyq_year": 2021,
        "q": "📌 GATE CSE 2021\nIn a binary max-heap containing n = 1023 distinct elements, what is the MINIMUM number of comparisons required to find the minimum element?",
        "options": None,
        "answer": "511",
        "msq_answers": None,
        "explanation": "In a binary max-heap, the minimum element must reside in one of the leaf nodes.\n- For a complete binary tree with n = 1023 nodes:\n- Number of internal nodes = floor(n / 2) = floor(1023 / 2) = 511.\n- Number of leaf nodes = ceil(n / 2) = 1023 - 511 = 512 leaves (from index 512 to 1023).\n- Finding the minimum among 512 unordered elements requires (k - 1) comparisons:\n  Comparisons = 512 - 1 = 511 comparisons.",
        "gate_trap": "The minimum element in a Max-Heap is NOT at a specific leaf; it can be ANY leaf node, so finding it requires scanning all leaf nodes.",
        "key_concept": "In a max-heap of n elements, leaves occupy indices [floor(n/2)+1 ... n]. Finding the minimum takes ceil(n/2) - 1 comparisons.",
        "reference_url": "https://www.geeksforgeeks.org/binary-heap/"
    }
]
