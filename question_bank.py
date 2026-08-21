"""
question_bank.py — Static bank of CS Fundamentals quiz questions.

Each question is a dict with:
  id         — unique string identifier
  topic      — topic category
  difficulty — easy | medium | hard | interview | tricky
  q          — question text (can include a code block)
  options    — dict {A: ..., B: ..., C: ..., D: ...}
  answer     — correct option key (A/B/C/D)
  explanation— detailed explanation of why the answer is correct
               and why alternatives are wrong
  tip        — optional interview tip string (or empty "")
"""

QUESTIONS: list[dict] = [

    # ─────────────────────────── DATA STRUCTURES ──────────────────────────────

    {
        "id": "ds_001",
        "topic": "Data Structures",
        "difficulty": "medium",
        "q": "Which data structure provides average-case O(1) insertion, deletion, and lookup by key?",
        "options": {
            "A": "Binary Search Tree",
            "B": "Hash Table",
            "C": "Skip List",
            "D": "Balanced AVL Tree",
        },
        "answer": "B",
        "explanation": (
            "B — Hash Table. A well-implemented hash table uses a hash function to map keys directly to "
            "array indices, giving O(1) average-case for all three operations. "
            "A) BST offers O(log n) for all operations on average. "
            "C) Skip Lists also provide O(log n) average-case. "
            "D) AVL Tree guarantees O(log n) due to rebalancing overhead. "
            "Key caveat: worst-case for a hash table is O(n) due to collisions — a classic interview trap!"
        ),
        "tip": "Interviewers love asking about HashMap worst-case. Always mention O(n) worst-case and why (all keys hash to the same bucket).",
    },
    {
        "id": "ds_002",
        "topic": "Data Structures",
        "difficulty": "tricky",
        "q": (
            "Consider this Python code:\n"
            "```\n"
            "stack = []\n"
            "stack.append(1)\n"
            "stack.append(2)\n"
            "stack.append(3)\n"
            "print(stack.pop())\n"
            "print(stack.pop())\n"
            "```\n"
            "What is the output?"
        ),
        "options": {
            "A": "1\n2",
            "B": "3\n2",
            "C": "1\n3",
            "D": "2\n3",
        },
        "answer": "B",
        "explanation": (
            "B — 3, then 2. A stack follows LIFO (Last In, First Out). "
            "Items are pushed in order 1→2→3. pop() removes the LAST inserted item first. "
            "So first pop() returns 3, second returns 2. "
            "A) Would be FIFO (queue) behaviour. C and D are incorrect orderings."
        ),
        "tip": "Python list used as a stack: append() = push, pop() = pop from top. Never use pop(0) for a stack — that is O(n).",
    },
    {
        "id": "ds_003",
        "topic": "Data Structures",
        "difficulty": "interview",
        "q": "You need to find the k-th largest element in a stream of numbers efficiently. Which data structure is MOST appropriate?",
        "options": {
            "A": "Max-Heap of size n",
            "B": "Min-Heap of size k",
            "C": "Sorted array",
            "D": "Hash Table",
        },
        "answer": "B",
        "explanation": (
            "B — Min-Heap of size k. Maintain a min-heap of exactly k elements. "
            "For each new number: if the heap has <k elements, insert it. "
            "If the new number is larger than the heap's minimum, pop the min and insert the new number. "
            "The heap's root is always the k-th largest. "
            "A) Max-Heap of size n gives the largest but does not efficiently give k-th largest. "
            "C) Sorted array insertion is O(n) per element. "
            "D) Hash Table cannot maintain ordering."
        ),
        "tip": "This is a very common Google/Amazon interview question. The min-heap of size k pattern is essential to memorize.",
    },
    {
        "id": "ds_004",
        "topic": "Data Structures",
        "difficulty": "easy",
        "q": "What is the time complexity of searching for an element in an unsorted array?",
        "options": {
            "A": "O(1)",
            "B": "O(log n)",
            "C": "O(n)",
            "D": "O(n log n)",
        },
        "answer": "C",
        "explanation": (
            "C — O(n). In the worst case, you must check every element before finding it or confirming it is absent. "
            "A) O(1) is only possible with direct indexing by position. "
            "B) O(log n) requires the array to be sorted (binary search). "
            "D) O(n log n) is typically sorting complexity."
        ),
        "tip": "",
    },
    {
        "id": "ds_005",
        "topic": "Data Structures",
        "difficulty": "medium",
        "q": "Which property distinguishes a Binary Search Tree (BST) from a general Binary Tree?",
        "options": {
            "A": "A BST always has exactly two children per node",
            "B": "For every node, all left subtree values are smaller and all right subtree values are larger",
            "C": "A BST is always balanced",
            "D": "A BST stores only integers",
        },
        "answer": "B",
        "explanation": (
            "B — The BST property: for any node N, every key in N's left subtree < N's key, "
            "and every key in N's right subtree > N's key. This enables O(log n) search on average. "
            "A) Nodes can have 0, 1, or 2 children. "
            "C) A BST is NOT necessarily balanced — a degenerate BST (all nodes on one side) degrades to O(n). "
            "D) BSTs work for any comparable data type."
        ),
        "tip": "A common interview follow-up: 'What is the time complexity of BST operations?' — Always say O(h) where h is height, not O(log n), because the tree might be unbalanced.",
    },
    {
        "id": "ds_006",
        "topic": "Data Structures",
        "difficulty": "tricky",
        "q": "What is the worst-case time complexity of inserting an element into a Hash Table?",
        "options": {
            "A": "O(1)",
            "B": "O(log n)",
            "C": "O(n)",
            "D": "O(n log n)",
        },
        "answer": "C",
        "explanation": (
            "C — O(n) worst case. If every key hashes to the same bucket (worst-case collision), "
            "the hash table degrades to a linked list and insertion requires traversing all n elements. "
            "A) O(1) is the AVERAGE case with a good hash function. "
            "B) O(log n) is not applicable to hash tables. "
            "D) O(n log n) is a sorting complexity."
        ),
        "tip": "This is the classic HashMap interview trap. Always distinguish average O(1) from worst-case O(n). Java's HashMap uses tree bins (red-black tree) after 8 collisions, making worst-case O(log n) in modern implementations.",
    },
    {
        "id": "ds_007",
        "topic": "Data Structures",
        "difficulty": "medium",
        "q": "Which traversal of a BST produces elements in sorted (ascending) order?",
        "options": {
            "A": "Pre-order",
            "B": "Post-order",
            "C": "In-order",
            "D": "Level-order",
        },
        "answer": "C",
        "explanation": (
            "C — In-order traversal (Left → Root → Right) visits nodes in ascending order in a BST. "
            "A) Pre-order (Root → Left → Right) is used for tree copying. "
            "B) Post-order (Left → Right → Root) is used for tree deletion. "
            "D) Level-order uses a queue and visits nodes level by level."
        ),
        "tip": "",
    },

    # ────────────────────────────── ALGORITHMS ────────────────────────────────

    {
        "id": "algo_001",
        "topic": "Algorithms",
        "difficulty": "medium",
        "q": (
            "What is the time complexity of the following code?\n"
            "```\n"
            "for i in range(n):\n"
            "    for j in range(i, n):\n"
            "        print(i, j)\n"
            "```"
        ),
        "options": {
            "A": "O(n)",
            "B": "O(n log n)",
            "C": "O(n²)",
            "D": "O(2ⁿ)",
        },
        "answer": "C",
        "explanation": (
            "C — O(n²). The outer loop runs n times. The inner loop runs n-i times for each i, "
            "giving n + (n-1) + (n-2) + ... + 1 = n(n+1)/2 total iterations = O(n²). "
            "Note: even though the inner loop doesn't always start from 0, "
            "it still executes a quadratic number of total operations."
        ),
        "tip": "",
    },
    {
        "id": "algo_002",
        "topic": "Algorithms",
        "difficulty": "interview",
        "q": "Why does QuickSort have O(n²) worst-case but is still preferred over MergeSort in practice?",
        "options": {
            "A": "QuickSort uses less code",
            "B": "QuickSort has better cache locality and O(log n) average space vs O(n) for MergeSort",
            "C": "QuickSort is always faster regardless of input",
            "D": "QuickSort does not require recursion",
        },
        "answer": "B",
        "explanation": (
            "B — Despite O(n²) worst-case, QuickSort is preferred because: "
            "(1) It sorts IN-PLACE (O(log n) stack space) vs MergeSort's O(n) auxiliary space. "
            "(2) Better cache performance — it accesses memory sequentially during partition. "
            "(3) Average-case O(n log n) with a good pivot selection strategy (random pivot). "
            "A) Code length is irrelevant to performance preference. "
            "C) MergeSort guarantees O(n log n) — it IS faster in worst case. "
            "D) QuickSort uses recursion."
        ),
        "tip": "For linked lists, MergeSort is preferred over QuickSort because random access is O(n) and cache locality advantage disappears.",
    },
    {
        "id": "algo_003",
        "topic": "Algorithms",
        "difficulty": "medium",
        "q": "Binary Search requires the input to be:",
        "options": {
            "A": "Stored in a linked list",
            "B": "Sorted and in a random-access structure",
            "C": "Unique elements only",
            "D": "Stored in a hash table",
        },
        "answer": "B",
        "explanation": (
            "B — Binary Search requires the data to be SORTED (to decide which half to eliminate) "
            "and in a structure that supports O(1) random access (like an array). "
            "A) Linked lists do not support O(1) random access, making binary search O(n). "
            "C) Duplicates are allowed; binary search still works. "
            "D) Hash tables do not maintain sorted order."
        ),
        "tip": "",
    },
    {
        "id": "algo_004",
        "topic": "Algorithms",
        "difficulty": "tricky",
        "q": "What does it mean for an algorithm to be 'greedy'? Which of the following problems CANNOT be solved optimally with a greedy approach?",
        "options": {
            "A": "Activity Selection Problem",
            "B": "Fractional Knapsack Problem",
            "C": "0/1 Knapsack Problem",
            "D": "Minimum Spanning Tree (Kruskal's algorithm)",
        },
        "answer": "C",
        "explanation": (
            "C — The 0/1 Knapsack Problem cannot be solved optimally with greedy. "
            "Greedy algorithms make the locally optimal choice at each step, hoping it leads to the global optimum. "
            "This works for: Activity Selection (A), Fractional Knapsack (B — items are divisible), "
            "and MST algorithms like Kruskal's (D). "
            "For 0/1 Knapsack, items are indivisible, so greedy (picking highest value/weight ratio) "
            "can miss the optimal solution — Dynamic Programming is required."
        ),
        "tip": "Remember: Greedy works when the problem has the 'greedy-choice property'. Always justify WHY greedy works for a specific problem in interviews.",
    },
    {
        "id": "algo_005",
        "topic": "Algorithms",
        "difficulty": "medium",
        "q": "What is the time complexity of Merge Sort in all cases (best, average, worst)?",
        "options": {
            "A": "O(n) best, O(n log n) average, O(n²) worst",
            "B": "O(n log n) for all cases",
            "C": "O(log n) best, O(n log n) average",
            "D": "O(n²) for all cases",
        },
        "answer": "B",
        "explanation": (
            "B — Merge Sort is always O(n log n) regardless of input order. "
            "It divides the array into two halves (log n levels) and merges them (O(n) per level). "
            "Unlike QuickSort, it does not depend on pivot selection, so it has no bad cases. "
            "A) This describes a case where best case could be O(n) (e.g. TimSort, an optimized merge sort), "
            "but standard Merge Sort is always O(n log n)."
        ),
        "tip": "",
    },
    {
        "id": "algo_006",
        "topic": "Algorithms",
        "difficulty": "easy",
        "q": "What is the time and space complexity of Fibonacci using naive recursion (fib(n) = fib(n-1) + fib(n-2))?",
        "options": {
            "A": "Time O(n), Space O(n)",
            "B": "Time O(2ⁿ), Space O(n)",
            "C": "Time O(n²), Space O(1)",
            "D": "Time O(n log n), Space O(log n)",
        },
        "answer": "B",
        "explanation": (
            "B — Naive recursive Fibonacci has exponential time O(2ⁿ) because it recomputes the same subproblems "
            "repeatedly (e.g. fib(n-2) is computed by both fib(n) and fib(n-1)). "
            "Space is O(n) due to the recursion call stack depth. "
            "With memoization (DP), time drops to O(n) with O(n) space. "
            "With bottom-up DP and two variables, time O(n) and space O(1) is achievable."
        ),
        "tip": "This is a classic interview progression: naive → memoization → bottom-up DP → matrix exponentiation O(log n).",
    },

    # ──────────────────────────────── OOP ─────────────────────────────────────

    {
        "id": "oop_001",
        "topic": "Object-Oriented Programming",
        "difficulty": "interview",
        "q": "What is the key difference between an Abstract Class and an Interface in Java?",
        "options": {
            "A": "Abstract classes can have constructors; interfaces cannot have any method implementations",
            "B": "Abstract classes can have state (fields) and partial implementations; interfaces define a pure contract (Java 8+ allows default methods)",
            "C": "Interfaces support multiple inheritance; abstract classes support single inheritance only, with no common use case for interfaces",
            "D": "There is no practical difference in modern Java",
        },
        "answer": "B",
        "explanation": (
            "B — The key distinction: "
            "Abstract class: can have instance fields (state), constructors, concrete methods, and abstract methods. "
            "A class can extend only ONE abstract class. "
            "Interface: traditionally only method signatures (contract). Java 8+ allows default and static methods, "
            "but interfaces cannot have instance fields or constructors. "
            "A class can implement MULTIPLE interfaces (solving multiple inheritance of type). "
            "A) Partially correct but incomplete — abstract classes can have both abstract and concrete methods. "
            "C) Misleading — both are important and complementary. "
            "D) Incorrect — the distinction still matters architecturally."
        ),
        "tip": "Interview answer: 'Use abstract class when classes share code/state. Use interface to define a contract and support multiple inheritance of type.'",
    },
    {
        "id": "oop_002",
        "topic": "Object-Oriented Programming",
        "difficulty": "tricky",
        "q": (
            "What is the output of this Java code?\n"
            "```java\n"
            "class Animal {\n"
            "    void sound() { System.out.println(\"Animal\"); }\n"
            "}\n"
            "class Dog extends Animal {\n"
            "    void sound() { System.out.println(\"Woof\"); }\n"
            "}\n"
            "Animal a = new Dog();\n"
            "a.sound();\n"
            "```"
        ),
        "options": {
            "A": "Animal",
            "B": "Woof",
            "C": "Compilation error",
            "D": "Runtime error",
        },
        "answer": "B",
        "explanation": (
            "B — 'Woof'. This demonstrates Runtime Polymorphism (Dynamic Method Dispatch). "
            "Even though the reference type is Animal, the actual object is Dog. "
            "Java resolves method calls at RUNTIME based on the actual object type, not the reference type. "
            "This is why OOP is powerful — you can write code against an interface/superclass "
            "and the correct subclass behaviour is invoked automatically."
        ),
        "tip": "Overriding is resolved at runtime (dynamic dispatch). Overloading is resolved at compile time (static dispatch). This is a core OOP interview concept.",
    },
    {
        "id": "oop_003",
        "topic": "Object-Oriented Programming",
        "difficulty": "medium",
        "q": "Which SOLID principle states that a class should have only one reason to change?",
        "options": {
            "A": "Open/Closed Principle",
            "B": "Liskov Substitution Principle",
            "C": "Single Responsibility Principle",
            "D": "Dependency Inversion Principle",
        },
        "answer": "C",
        "explanation": (
            "C — Single Responsibility Principle (SRP): A class should have one and only one reason to change, "
            "meaning it should have only one job. "
            "A) Open/Closed: open for extension, closed for modification. "
            "B) Liskov Substitution: objects of a superclass should be replaceable with objects of its subclasses. "
            "D) Dependency Inversion: depend on abstractions, not on concretions."
        ),
        "tip": "",
    },
    {
        "id": "oop_004",
        "topic": "Object-Oriented Programming",
        "difficulty": "easy",
        "q": "Which OOP concept allows a subclass to provide a specific implementation of a method already defined in its parent class?",
        "options": {
            "A": "Method Overloading",
            "B": "Method Overriding",
            "C": "Encapsulation",
            "D": "Abstraction",
        },
        "answer": "B",
        "explanation": (
            "B — Method Overriding. The subclass redefines a method from the parent class with the same "
            "signature, changing its behaviour. This is the basis of runtime polymorphism. "
            "A) Overloading = same method name, different parameters, resolved at COMPILE time. "
            "C) Encapsulation = hiding internal state. "
            "D) Abstraction = hiding implementation details behind an interface."
        ),
        "tip": "Overloading vs Overriding is a classic interview trap. Overloading = same name, different signature (compile-time). Overriding = same signature, different class (runtime).",
    },
    {
        "id": "oop_005",
        "topic": "Object-Oriented Programming",
        "difficulty": "medium",
        "q": "What is Composition over Inheritance and why is it often preferred?",
        "options": {
            "A": "Composition is faster at runtime than inheritance",
            "B": "Composition builds complex behaviour by combining objects, giving more flexibility and avoiding tight coupling",
            "C": "Composition eliminates the need for interfaces",
            "D": "Inheritance should never be used in modern software",
        },
        "answer": "B",
        "explanation": (
            "B — Composition builds objects from other objects ('has-a' relationship) instead of inheriting ('is-a'). "
            "Benefits: (1) Avoids the fragile base class problem. (2) Behaviour can be changed at runtime by swapping components. "
            "(3) No deep, rigid inheritance hierarchies. "
            "Example: Instead of Car extends Vehicle, use Car has-a Engine. "
            "A) Performance is not the reason. C) Interfaces are still essential. D) Inheritance is valid for true 'is-a' relationships."
        ),
        "tip": "",
    },

    # ─────────────────────────── OPERATING SYSTEMS ────────────────────────────

    {
        "id": "os_001",
        "topic": "Operating Systems",
        "difficulty": "interview",
        "q": "What is the fundamental difference between a Process and a Thread?",
        "options": {
            "A": "Processes are faster than threads because they use less memory",
            "B": "A process has its own memory space; threads within a process share the same memory space",
            "C": "Threads cannot communicate with each other",
            "D": "A process can only contain one thread",
        },
        "answer": "B",
        "explanation": (
            "B — Process: independent program in execution with its own virtual address space, file handles, "
            "and resources. Processes are isolated from each other. "
            "Thread: the smallest unit of execution within a process. Multiple threads SHARE the process's "
            "memory (heap, code, data) but each has its own stack and registers. "
            "A) Threads are lighter than processes (less creation overhead), not the other way around. "
            "C) Threads can communicate via shared memory (but need synchronization). "
            "D) Every process has at least one thread (the main thread)."
        ),
        "tip": "Follow-up: 'When would you use multiple processes vs multiple threads?' — Processes for isolation and fault tolerance; threads for shared-state tasks and lower overhead.",
    },
    {
        "id": "os_002",
        "topic": "Operating Systems",
        "difficulty": "medium",
        "q": "Which of the four Coffman conditions is NOT required for a deadlock to occur?",
        "options": {
            "A": "Mutual Exclusion",
            "B": "Hold and Wait",
            "C": "Starvation",
            "D": "Circular Wait",
        },
        "answer": "C",
        "explanation": (
            "C — Starvation is NOT a Coffman condition for deadlock. "
            "The four necessary conditions for deadlock are: "
            "(1) Mutual Exclusion — at least one resource is held in a non-shareable mode. "
            "(2) Hold and Wait — a process holds resources while waiting for others. "
            "(3) No Preemption — resources cannot be forcibly taken. "
            "(4) Circular Wait — a circular chain of processes, each waiting for the next. "
            "Starvation is a separate problem where a process waits indefinitely but is not technically deadlocked."
        ),
        "tip": "",
    },
    {
        "id": "os_003",
        "topic": "Operating Systems",
        "difficulty": "tricky",
        "q": "What is a Race Condition and how can it be prevented?",
        "options": {
            "A": "When two processes compete for CPU speed; prevented by faster hardware",
            "B": "When multiple threads access shared data concurrently and the result depends on execution order; prevented using synchronization mechanisms",
            "C": "When a process runs out of memory; prevented by allocating more RAM",
            "D": "When a thread finishes before the main thread; prevented using sleep()",
        },
        "answer": "B",
        "explanation": (
            "B — A race condition occurs when the correctness of a program depends on the relative timing "
            "or interleaving of multiple threads/processes. "
            "Example: two threads both read a counter (value=5), both increment it, and both write 6 — "
            "but the expected result is 7. "
            "Prevention: Mutexes, semaphores, monitors, atomic operations, or lock-free data structures."
        ),
        "tip": "Race conditions are one of the hardest bugs to reproduce because they are timing-dependent. Always identify the critical section — the code accessing shared state.",
    },
    {
        "id": "os_004",
        "topic": "Operating Systems",
        "difficulty": "easy",
        "q": "What is Virtual Memory?",
        "options": {
            "A": "Extra RAM added by plugging in a USB drive",
            "B": "A technique that gives each process the illusion of having its own large, contiguous address space using disk storage as an extension of RAM",
            "C": "Memory allocated exclusively for the operating system kernel",
            "D": "A type of cache memory inside the CPU",
        },
        "answer": "B",
        "explanation": (
            "B — Virtual Memory allows the OS to run programs larger than physical RAM by storing "
            "less-used pages on disk (swap space). Each process sees a private virtual address space, "
            "providing isolation and simplifying memory management. "
            "The MMU (Memory Management Unit) translates virtual addresses to physical addresses. "
            "A) USB drives can be used as ReadyBoost on Windows but that is not virtual memory. "
            "C) Kernel memory is a subset of virtual memory. "
            "D) CPU caches (L1, L2, L3) are not virtual memory."
        ),
        "tip": "",
    },
    {
        "id": "os_005",
        "topic": "Operating Systems",
        "difficulty": "medium",
        "q": "What is Context Switching and what is its main performance cost?",
        "options": {
            "A": "Switching between two programming languages; costs compilation time",
            "B": "Saving and restoring the state of a CPU so multiple processes can share it; the cost is CPU time spent saving/restoring registers and cache invalidation",
            "C": "Changing the active window on a desktop; costs GPU time",
            "D": "Switching between kernel and user mode; costs one CPU cycle",
        },
        "answer": "B",
        "explanation": (
            "B — Context switching is the OS mechanism to share the CPU among multiple processes/threads. "
            "The OS saves the current process's registers, program counter, and stack pointer, then loads "
            "the next process's saved state. "
            "Main costs: (1) Direct cost of saving/restoring CPU state. (2) Cache pollution — the new process "
            "has different data, causing cache misses. (3) TLB flushes when switching address spaces. "
            "Excessive context switching degrades performance significantly."
        ),
        "tip": "",
    },

    # ─────────────────────────── COMPUTER NETWORKS ────────────────────────────

    {
        "id": "net_001",
        "topic": "Computer Networks",
        "difficulty": "interview",
        "q": "Why does TCP use a three-way handshake before data transfer?",
        "options": {
            "A": "To encrypt the data before sending",
            "B": "To establish a reliable, bidirectional connection by synchronizing sequence numbers and confirming both sides are ready to communicate",
            "C": "To check if the server has enough bandwidth",
            "D": "To prevent IP spoofing attacks",
        },
        "answer": "B",
        "explanation": (
            "B — The TCP 3-way handshake (SYN → SYN-ACK → ACK) achieves: "
            "(1) Synchronization of initial sequence numbers (ISN) in both directions. "
            "(2) Confirmation that both client and server can send AND receive data. "
            "(3) Establishment of connection state before data flows. "
            "Without it, a server could not know if a client's initial packet was delayed and retransmitted, "
            "causing duplicate connections. "
            "A) Encryption is handled by TLS, a separate layer. "
            "C and D) Not the purpose of the handshake."
        ),
        "tip": "A two-way handshake is insufficient because it cannot confirm the client can receive the server's SYN-ACK. The third ACK proves bidirectional reachability.",
    },
    {
        "id": "net_002",
        "topic": "Computer Networks",
        "difficulty": "medium",
        "q": "What is the key difference between TCP and UDP?",
        "options": {
            "A": "TCP is faster in all scenarios",
            "B": "TCP provides reliable, ordered, connection-based delivery; UDP is connectionless and does not guarantee delivery or order",
            "C": "UDP is only used for file transfers",
            "D": "TCP uses IP addresses; UDP uses MAC addresses",
        },
        "answer": "B",
        "explanation": (
            "B — TCP (Transmission Control Protocol): connection-oriented, provides reliability via "
            "acknowledgements, retransmission, flow control, and congestion control. "
            "Overhead: the 3-way handshake and ACKs. Use when correctness matters (HTTP, email, file transfer). "
            "UDP (User Datagram Protocol): connectionless, no handshake, no ACKs. "
            "Faster, lower latency. Use when speed > reliability (video streaming, DNS, gaming, VoIP). "
            "A) UDP is faster due to no overhead. "
            "C) UDP is used for DNS, streaming, gaming — not file transfers typically."
        ),
        "tip": "DNS uses UDP for queries (fast, small packets) but switches to TCP for large responses or zone transfers.",
    },
    {
        "id": "net_003",
        "topic": "Computer Networks",
        "difficulty": "easy",
        "q": "How many layers does the OSI model have?",
        "options": {
            "A": "4",
            "B": "5",
            "C": "7",
            "D": "9",
        },
        "answer": "C",
        "explanation": (
            "C — The OSI (Open Systems Interconnection) model has 7 layers: "
            "1. Physical, 2. Data Link, 3. Network, 4. Transport, 5. Session, "
            "6. Presentation, 7. Application. "
            "Mnemonic: 'Please Do Not Throw Sausage Pizza Away'. "
            "The TCP/IP model condenses this into 4 layers: Network Access, Internet, Transport, Application."
        ),
        "tip": "",
    },
    {
        "id": "net_004",
        "topic": "Computer Networks",
        "difficulty": "tricky",
        "q": "What is the difference between Authentication and Authorization?",
        "options": {
            "A": "They are the same thing; both verify identity",
            "B": "Authentication verifies WHO you are; Authorization determines WHAT you are allowed to do",
            "C": "Authorization happens before Authentication",
            "D": "Authentication uses tokens; Authorization uses passwords",
        },
        "answer": "B",
        "explanation": (
            "B — Authentication (AuthN): proving identity. Example: logging in with username/password. "
            "Authorization (AuthZ): determining what an authenticated user is permitted to do. "
            "Example: an admin can delete users, but a regular user cannot. "
            "The order is always: Authenticate first, then Authorize. "
            "A) They are distinct concepts. "
            "C) Wrong order — you must know WHO someone is before deciding what they can do. "
            "D) Both can use various mechanisms; this is not the distinction."
        ),
        "tip": "Common interview confusion: JWT tokens carry BOTH authentication (user identity) and authorization (roles/claims). Understand which part of the token serves which purpose.",
    },
    {
        "id": "net_005",
        "topic": "Computer Networks",
        "difficulty": "medium",
        "q": "What happens when you type 'google.com' in your browser and press Enter? (First step)",
        "options": {
            "A": "The browser immediately connects to Google's IP address",
            "B": "The browser checks its DNS cache, then queries a DNS resolver to resolve 'google.com' to an IP address",
            "C": "The browser sends an HTTP GET request directly",
            "D": "The OS establishes a TCP connection to port 80",
        },
        "answer": "B",
        "explanation": (
            "B — The first step is DNS resolution. The browser checks: "
            "(1) Its own DNS cache → (2) OS DNS cache → (3) Router DNS cache → "
            "(4) ISP's recursive resolver → (5) Root nameservers → (6) TLD nameservers → "
            "(7) Authoritative nameserver for google.com. "
            "Once the IP is resolved, the browser establishes a TCP connection (3-way handshake), "
            "then TLS handshake (for HTTPS), then sends the HTTP GET request."
        ),
        "tip": "This is one of the most common system design interview questions. Prepare to describe the FULL flow: DNS → TCP → TLS → HTTP → Server → CDN → Response.",
    },

    # ──────────────────────────────── DBMS ────────────────────────────────────

    {
        "id": "db_001",
        "topic": "Databases",
        "difficulty": "medium",
        "q": "What does ACID stand for in database transactions?",
        "options": {
            "A": "Availability, Consistency, Isolation, Durability",
            "B": "Atomicity, Consistency, Isolation, Durability",
            "C": "Atomicity, Concurrency, Integrity, Distribution",
            "D": "Availability, Concurrency, Isolation, Distribution",
        },
        "answer": "B",
        "explanation": (
            "B — ACID properties ensure reliable transactions: "
            "Atomicity: a transaction is all-or-nothing (either fully completes or fully rolls back). "
            "Consistency: a transaction brings the database from one valid state to another. "
            "Isolation: concurrent transactions execute as if they were sequential. "
            "Durability: once committed, changes persist even after system failure. "
            "A) 'Availability' is from the CAP theorem, not ACID."
        ),
        "tip": "",
    },
    {
        "id": "db_002",
        "topic": "Databases",
        "difficulty": "interview",
        "q": "What is the difference between DELETE, TRUNCATE, and DROP in SQL?",
        "options": {
            "A": "They all do the same thing — remove data permanently",
            "B": "DELETE removes specific rows (logged, can rollback); TRUNCATE removes all rows quickly (minimal logging, usually cannot rollback); DROP removes the entire table structure",
            "C": "DELETE is faster than TRUNCATE",
            "D": "TRUNCATE can use a WHERE clause; DELETE cannot",
        },
        "answer": "B",
        "explanation": (
            "B — DELETE: DML command, removes specific rows matching WHERE clause. "
            "Fully logged, can be rolled back within a transaction. "
            "TRUNCATE: DDL command, removes ALL rows very fast by deallocating data pages. "
            "Minimal logging, usually cannot be rolled back (DB-specific). Resets identity counters. "
            "DROP: DDL command, removes the entire table including structure, indexes, and constraints. "
            "A) They behave very differently. "
            "C) TRUNCATE is FASTER than DELETE (no row-by-row logging). "
            "D) Reversed — DELETE can use WHERE; TRUNCATE cannot."
        ),
        "tip": "This is asked in nearly every SQL interview. Remember the three: DELETE = surgical, TRUNCATE = bulldoze the data, DROP = bulldoze the building.",
    },
    {
        "id": "db_003",
        "topic": "Databases",
        "difficulty": "tricky",
        "q": "What is the difference between SQL WHERE and HAVING clauses?",
        "options": {
            "A": "HAVING is used with SELECT; WHERE is not",
            "B": "WHERE filters rows BEFORE grouping; HAVING filters groups AFTER GROUP BY aggregation",
            "C": "WHERE works on aggregated values; HAVING works on individual rows",
            "D": "They are interchangeable",
        },
        "answer": "B",
        "explanation": (
            "B — WHERE is applied to individual rows BEFORE any GROUP BY operation. "
            "HAVING is applied to GROUPS AFTER aggregation. "
            "Example: SELECT dept, COUNT(*) as cnt FROM employees WHERE salary > 50000 GROUP BY dept HAVING cnt > 5. "
            "WHERE filters employees before grouping; HAVING filters departments with more than 5 qualifying employees. "
            "You CANNOT use aggregate functions (COUNT, SUM, AVG) in a WHERE clause."
        ),
        "tip": "Interview rule: If you need to filter on an aggregated value, use HAVING. If filtering individual rows, use WHERE.",
    },
    {
        "id": "db_004",
        "topic": "Databases",
        "difficulty": "medium",
        "q": "What type of JOIN returns only rows where there is a match in BOTH tables?",
        "options": {
            "A": "LEFT JOIN",
            "B": "RIGHT JOIN",
            "C": "INNER JOIN",
            "D": "FULL OUTER JOIN",
        },
        "answer": "C",
        "explanation": (
            "C — INNER JOIN returns only rows with matching values in both tables. "
            "LEFT JOIN: all rows from left table + matching rows from right (NULLs for unmatched right rows). "
            "RIGHT JOIN: all rows from right table + matching rows from left (NULLs for unmatched left rows). "
            "FULL OUTER JOIN: all rows from both tables (NULLs where no match exists)."
        ),
        "tip": "",
    },
    {
        "id": "db_005",
        "topic": "Databases",
        "difficulty": "easy",
        "q": "What is an Index in a database and what is its primary benefit?",
        "options": {
            "A": "A backup copy of the table",
            "B": "A data structure that speeds up data retrieval by allowing faster lookup without scanning the entire table",
            "C": "A constraint that prevents duplicate rows",
            "D": "A way to join two tables",
        },
        "answer": "B",
        "explanation": (
            "B — An index (typically a B-tree) stores a sorted structure of column values with pointers "
            "to the full rows, allowing the database engine to find rows without a full table scan. "
            "Trade-off: Indexes speed up reads but slow down writes (INSERT, UPDATE, DELETE must update indexes too) "
            "and consume extra storage. "
            "A) That is a database backup. "
            "C) That is a UNIQUE constraint. "
            "D) Joins use keys, not indexes (though indexes on join columns greatly improve join performance)."
        ),
        "tip": "Common interview question: 'When would you NOT add an index?' — On small tables, or on columns with very low cardinality (e.g., a boolean column).",
    },
    {
        "id": "db_006",
        "topic": "Databases",
        "difficulty": "tricky",
        "q": "What is the difference between a Primary Key and a Unique Key?",
        "options": {
            "A": "Both enforce uniqueness; Primary Key cannot be NULL, Unique Key can have one NULL value per column",
            "B": "Primary Key can have duplicates; Unique Key cannot",
            "C": "A table can have multiple Primary Keys but only one Unique Key",
            "D": "They are identical — no practical difference",
        },
        "answer": "A",
        "explanation": (
            "A — Both enforce uniqueness. Key differences: "
            "(1) Primary Key cannot be NULL — it must uniquely and non-nullably identify each row. "
            "(2) Unique Key allows NULL (in most databases, one NULL per column in standard SQL). "
            "(3) A table can have only ONE Primary Key (which can be composite). "
            "(4) A table can have MULTIPLE Unique Keys. "
            "(5) Primary Key automatically creates a clustered index in most databases; Unique Key creates a non-clustered index."
        ),
        "tip": "",
    },

    # ──────────────────────────── PROGRAMMING FUNDAMENTALS ─────────────────────

    {
        "id": "prog_001",
        "topic": "Programming Fundamentals",
        "difficulty": "tricky",
        "q": "What is the difference between Stack memory and Heap memory?",
        "options": {
            "A": "Stack is faster; it stores local variables and function call frames managed automatically (LIFO); Heap is slower, stores dynamic allocations managed manually or by GC",
            "B": "Heap is faster than Stack because it is larger",
            "C": "Stack stores global variables; Heap stores local variables",
            "D": "Both Stack and Heap are managed by the garbage collector",
        },
        "answer": "A",
        "explanation": (
            "A — Stack: fast (just moving a pointer), automatically managed, LIFO structure. "
            "Stores: local variables, function parameters, return addresses. "
            "Limited size (typically 1–8 MB); overflow = StackOverflowError. "
            "Heap: slower, larger, dynamically allocated at runtime. "
            "Stores: objects created with 'new', data structures. "
            "In Java/Python: GC manages heap. In C/C++: programmer manages heap (malloc/free). "
            "B) Stack is FASTER, not heap. "
            "C) Global/static variables are stored in the Data Segment, not stack or heap."
        ),
        "tip": "Interview question: 'Where is a Java object stored?' — The object is on the HEAP; the reference variable is on the STACK.",
    },
    {
        "id": "prog_002",
        "topic": "Programming Fundamentals",
        "difficulty": "medium",
        "q": "What is the difference between Compilation and Interpretation?",
        "options": {
            "A": "Compiled programs run slower than interpreted programs",
            "B": "A compiler translates the entire program to machine code before execution; an interpreter translates and executes line-by-line at runtime",
            "C": "Python is a compiled language; Java is interpreted",
            "D": "Compilation requires more RAM than interpretation",
        },
        "answer": "B",
        "explanation": (
            "B — Compiler: translates entire source code to machine code (or bytecode) in one step before execution. "
            "Result: faster execution (no translation overhead at runtime). Example: C, C++. "
            "Interpreter: reads and executes source code line-by-line at runtime. "
            "Result: slower execution but more flexible (dynamic typing, easier debugging). Example: Python. "
            "A) Compiled programs are typically FASTER. "
            "C) Java compiles to bytecode (JVM), then JIT-compiles to machine code — it is BOTH. "
            "Python has a compilation step (to .pyc) before interpretation."
        ),
        "tip": "Java's JVM uses JIT (Just-In-Time) compilation — it compiles bytecode to native machine code at runtime for frequently executed sections, blending both approaches.",
    },

    # ─────────────────────────── SYSTEM DESIGN BASICS ─────────────────────────

    {
        "id": "sys_001",
        "topic": "System Design",
        "difficulty": "interview",
        "q": "What is the difference between Horizontal Scaling and Vertical Scaling?",
        "options": {
            "A": "Horizontal scaling means adding more CPU cores to one machine; vertical means adding more machines",
            "B": "Horizontal scaling (scale out) means adding more machines; vertical scaling (scale up) means adding more resources to one machine",
            "C": "Vertical scaling is always cheaper and more effective",
            "D": "Horizontal scaling only applies to databases",
        },
        "answer": "B",
        "explanation": (
            "B — Vertical scaling (scale up): add more CPU, RAM, or storage to a single server. "
            "Simple but has hardware limits and creates a single point of failure. "
            "Horizontal scaling (scale out): add more servers/instances. "
            "More complex (requires load balancing, distributed coordination) but theoretically unlimited "
            "and provides fault tolerance. "
            "A) The definitions are reversed. "
            "C) Vertical scaling has hard limits and SPOF issues. "
            "D) Both apply to web servers, application servers, and databases."
        ),
        "tip": "Most modern cloud architectures prefer horizontal scaling with stateless services and managed databases, because it is elastic and fault-tolerant.",
    },
    {
        "id": "sys_002",
        "topic": "System Design",
        "difficulty": "medium",
        "q": "What is the role of a Load Balancer in a system?",
        "options": {
            "A": "To increase database storage",
            "B": "To distribute incoming requests across multiple servers to improve availability and prevent any one server from being overwhelmed",
            "C": "To compress network traffic",
            "D": "To cache database queries",
        },
        "answer": "B",
        "explanation": (
            "B — A load balancer sits in front of multiple application servers and distributes incoming "
            "requests using algorithms like Round Robin, Least Connections, or IP Hash. "
            "Benefits: (1) Prevents overloading a single server. "
            "(2) Enables horizontal scaling. "
            "(3) Provides high availability — if one server fails, traffic is routed to healthy servers. "
            "(4) Can perform health checks to detect failed servers."
        ),
        "tip": "",
    },

    # ─────────────────────────── SOFTWARE ENGINEERING ─────────────────────────

    {
        "id": "se_001",
        "topic": "Software Engineering",
        "difficulty": "medium",
        "q": "What is CI/CD and why is it important?",
        "options": {
            "A": "Client/Interface Controller Device — a hardware component",
            "B": "Continuous Integration/Continuous Delivery — automating code integration, testing, and deployment to deliver software faster and more reliably",
            "C": "Code Inspection/Code Deployment — a manual review process",
            "D": "Compiler Infrastructure/Code Distribution — a compiler toolchain",
        },
        "answer": "B",
        "explanation": (
            "B — CI (Continuous Integration): developers frequently merge code to a shared branch; "
            "automated builds and tests run on every commit to catch integration issues early. "
            "CD (Continuous Delivery): code is automatically prepared and staged for release. "
            "Continuous Deployment: every passing build is automatically deployed to production. "
            "Benefits: faster release cycles, early bug detection, reduced integration hell, "
            "and consistent deployment processes."
        ),
        "tip": "",
    },
    {
        "id": "se_002",
        "topic": "Software Engineering",
        "difficulty": "easy",
        "q": "What is the purpose of Version Control (e.g., Git)?",
        "options": {
            "A": "To compile code automatically",
            "B": "To track changes to code over time, enabling collaboration, history, branching, and rollback",
            "C": "To run automated tests",
            "D": "To deploy applications to servers",
        },
        "answer": "B",
        "explanation": (
            "B — Version control systems like Git track every change to the codebase. "
            "Key benefits: (1) Full history of who changed what and when. "
            "(2) Branching — work on features in isolation. "
            "(3) Merging — combine changes from multiple developers. "
            "(4) Rollback — revert to any previous working state. "
            "(5) Collaboration without overwriting each other's work."
        ),
        "tip": "",
    },

    # ─────────────────────────── COMPUTER ARCHITECTURE ────────────────────────

    {
        "id": "arch_001",
        "topic": "Computer Architecture",
        "difficulty": "medium",
        "q": "What is the Memory Hierarchy and why does it exist?",
        "options": {
            "A": "A ranking of programming languages by memory efficiency",
            "B": "A layered structure (Registers → Cache → RAM → Disk) where faster memory is smaller and more expensive; it exists to balance speed and cost",
            "C": "The order in which variables are stored in a program",
            "D": "A list of memory allocation functions",
        },
        "answer": "B",
        "explanation": (
            "B — Memory hierarchy (fastest to slowest, smallest to largest): "
            "CPU Registers → L1 Cache → L2 Cache → L3 Cache → RAM → SSD/HDD → Network Storage. "
            "Why: Faster memory (SRAM in cache) is exponentially more expensive than slower memory (DRAM in RAM). "
            "The hierarchy exploits temporal and spatial locality — recently and nearby accessed data "
            "is kept in fast cache to minimize latency."
        ),
        "tip": "Knowing memory latency numbers is impressive in interviews: L1 cache ~1ns, L2 ~5ns, L3 ~40ns, RAM ~100ns, SSD ~100μs, HDD ~10ms.",
    },

    # ─────────────────────────── WEB FUNDAMENTALS ─────────────────────────────

    {
        "id": "web_001",
        "topic": "Web Fundamentals",
        "difficulty": "medium",
        "q": "What is the difference between HTTP status codes 401 and 403?",
        "options": {
            "A": "401 means server error; 403 means client error",
            "B": "401 (Unauthorized) means authentication is required or failed; 403 (Forbidden) means the server understood the request but refuses to authorize it",
            "C": "They are identical — both mean access denied",
            "D": "401 means the resource is not found; 403 means it moved permanently",
        },
        "answer": "B",
        "explanation": (
            "B — 401 Unauthorized: the client must authenticate itself to get the requested response. "
            "Despite the name, it means 'unauthenticated'. Login again or provide credentials. "
            "403 Forbidden: the client IS authenticated but does NOT have permission to access the resource. "
            "Sending credentials again will not help. "
            "Example: A logged-in regular user trying to access an admin page gets 403."
        ),
        "tip": "Authentication vs Authorization confusion extends to HTTP status codes: 401 = authentication problem, 403 = authorization problem.",
    },
    {
        "id": "web_002",
        "topic": "Web Fundamentals",
        "difficulty": "easy",
        "q": "What does REST stand for and what is its most important constraint?",
        "options": {
            "A": "Remote Execution Service Technology; encryption",
            "B": "Representational State Transfer; statelessness — each request must contain all information needed to process it",
            "C": "Resource Encoding Standard Technology; caching",
            "D": "Real-time Event Streaming Transport; bidirectional communication",
        },
        "answer": "B",
        "explanation": (
            "B — REST (Representational State Transfer) is an architectural style for distributed systems. "
            "Key constraints: (1) Stateless — server stores NO client session state between requests. "
            "(2) Uniform Interface — standard HTTP methods (GET, POST, PUT, DELETE, PATCH). "
            "(3) Client-Server separation. (4) Cacheable responses. (5) Layered system. "
            "Statelessness is the most important for scalability — any server can handle any request."
        ),
        "tip": "",
    },
]
