"""
question_bank_extra.py — Extended high-quality CS Fundamentals questions (~110 new).
Imported and merged by question_bank.py.
"""

EXTRA_QUESTIONS: list[dict] = [

    # ─────────────────────── ADVANCED DATA STRUCTURES ─────────────────────────

    {
        "id": "ds_008",
        "topic": "Data Structures",
        "difficulty": "interview",
        "q": "Why does iterating an array have better cache performance than iterating a linked list, even though both are O(n)?",
        "options": {
            "A": "Arrays use less memory than linked lists",
            "B": "Array elements are contiguous in memory, exploiting spatial locality; linked list nodes are scattered in the heap, causing a cache miss on every traversal step",
            "C": "Arrays are stored in CPU registers",
            "D": "Linked lists do not support sequential access",
        },
        "answer": "B",
        "explanation": (
            "B — Spatial locality: when the CPU loads one array element into a 64-byte cache line, "
            "it pre-fetches the next ~15 adjacent elements. Subsequent accesses hit cache (~1ns). "
            "Linked list: each node's 'next' pointer leads to a random heap address → likely a cache miss "
            "(fetch from RAM: ~100ns). "
            "On modern hardware with large datasets, this can make array traversal 10-100x faster "
            "despite the same O(n) complexity. "
            "D) Linked lists support sequential access — they're just cache-unfriendly doing it."
        ),
        "tip": "This is why Java ArrayList is usually preferred over LinkedList even for many inserts/deletes, unless you're inserting at a known node.",
    },
    {
        "id": "ds_009",
        "topic": "Data Structures",
        "difficulty": "tricky",
        "q": (
            "Design a MinStack supporting push, pop, top, getMin() all in O(1). Which approach works?\n"
            "```\n"
            "class MinStack:\n"
            "    def push(self, val): ...\n"
            "    def pop(self): ...\n"
            "    def top(self): ...\n"
            "    def getMin(self): ...\n"
            "```"
        ),
        "options": {
            "A": "Sort the stack on every push so the minimum is at the bottom",
            "B": "Maintain a second auxiliary 'min-stack'; push min(val, current_min) on every push, pop it simultaneously",
            "C": "Scan the full stack on every getMin() call",
            "D": "Store only the current minimum in a single variable",
        },
        "answer": "B",
        "explanation": (
            "B — Auxiliary min-stack: "
            "push(x): push x to main; push min(x, min_stack.top()) to min_stack. "
            "pop(): pop from both. "
            "getMin(): min_stack.top() — always O(1). "
            "A) Sorting breaks LIFO ordering. "
            "C) Scanning is O(n). "
            "D) Storing one variable fails when you pop the current min — you lose the previous minimum. "
            "The min-stack keeps a snapshot of the minimum at every historical state."
        ),
        "tip": "Follow-up: 'Can you do it O(1) extra space?' — encode (val - currentMin) in the stack; use a negative delta as a sentinel. Complex but doable.",
    },
    {
        "id": "ds_010",
        "topic": "Data Structures",
        "difficulty": "medium",
        "q": "What is the amortized cost of implementing a Queue using two Stacks?",
        "options": {
            "A": "O(n) per operation always",
            "B": "O(1) amortized per operation — worst-case single dequeue is O(n) but each element moves at most twice total",
            "C": "O(log n) per operation",
            "D": "O(1) worst-case for all operations",
        },
        "answer": "B",
        "explanation": (
            "B — Two stacks: 'inbox' for enqueue, 'outbox' for dequeue. "
            "Enqueue: push to inbox — O(1). "
            "Dequeue: if outbox empty, pour all inbox items into outbox (O(n) one time). Pop outbox. "
            "Each element moves at most twice (once into inbox, once into outbox). "
            "Over n operations: total work = 2n → amortized O(1) per operation. "
            "D) Worst-case single dequeue is O(n), not O(1) — only amortized is O(1)."
        ),
        "tip": "Amortized analysis: the expensive pour-operation is paid for by the cheap enqueue operations. Interview: name all three amortized analysis methods (aggregate, accounting, potential).",
    },
    {
        "id": "ds_011",
        "topic": "Data Structures",
        "difficulty": "medium",
        "q": "Compare adjacency matrix vs adjacency list space complexity for a graph with V vertices and E edges.",
        "options": {
            "A": "Both use O(V + E) space",
            "B": "Adjacency matrix: O(V²); Adjacency list: O(V + E) — matrix wastes space for sparse graphs",
            "C": "Adjacency matrix: O(E); Adjacency list: O(V²)",
            "D": "Both use O(V²) space",
        },
        "answer": "B",
        "explanation": (
            "B — Adjacency matrix: V×V grid, allocated regardless of actual edges. "
            "Edge lookup O(1), but for a sparse graph (E << V²) most cells are zero — wasted memory. "
            "Adjacency list: array of V lists, each holding actual neighbors. Total storage = O(V + E). "
            "For a social network with 1B users but average 200 friends each: "
            "matrix = 10^18 cells (impossible). List = 1B + 200B entries (feasible). "
            "Matrix is better when: dense graph (E ≈ V²), or when O(1) edge-existence check is critical."
        ),
        "tip": "Rule: sparse graph → adjacency list. Dense graph → adjacency matrix. Almost all real-world graphs (social, road, web) are extremely sparse.",
    },
    {
        "id": "ds_012",
        "topic": "Data Structures",
        "difficulty": "interview",
        "q": "When should you use BFS over DFS and vice versa?",
        "options": {
            "A": "BFS is always faster than DFS",
            "B": "BFS: shortest path in unweighted graphs, level-order traversal. DFS: cycle detection, topological sort, strongly connected components, exhaustive search with less memory for deep narrow graphs.",
            "C": "DFS is always better because it uses recursion",
            "D": "They always produce identical results on the same graph",
        },
        "answer": "B",
        "explanation": (
            "B — BFS (queue, O(V) space): explores layer by layer, guarantees shortest path in unweighted graphs. "
            "Best for: shortest path, finding nearest nodes, bipartiteness check, connected components. "
            "DFS (stack/recursion, O(h) space where h = max depth): "
            "Best for: cycle detection, topological sort, SCC (Tarjan/Kosaraju), "
            "generating all paths/permutations, maze solving. "
            "Memory: DFS uses O(h) — great for deep graphs. BFS uses O(w) — great for wide graphs. "
            "Both have O(V + E) time complexity."
        ),
        "tip": "Classic interview: shortest path in a grid (maze)? BFS. Detect cycle in directed graph? DFS with visited-state coloring (white/gray/black).",
    },
    {
        "id": "ds_013",
        "topic": "Data Structures",
        "difficulty": "tricky",
        "q": "Floyd's Cycle Detection (tortoise and hare) uses two pointers at 1x and 2x speed. What is its time and space complexity?",
        "options": {
            "A": "O(n²) time, O(1) space",
            "B": "O(n) time, O(1) space — if a cycle exists, the fast pointer must lap the slow pointer inside the cycle",
            "C": "O(n log n) time, O(n) space",
            "D": "O(n) time, O(n) space",
        },
        "answer": "B",
        "explanation": (
            "B — If a cycle exists, fast eventually laps slow inside the cycle → they meet. "
            "O(n) time (at most one full cycle), O(1) space (just two pointers). "
            "If no cycle, fast reaches null. "
            "Bonus: resetting slow to head and advancing both at 1x finds the cycle entry point. "
            "Used for: cycle detection in linked lists, finding duplicate in array where values in [1,n] "
            "(treat as next pointers), finding repeating number without extra space."
        ),
        "tip": "This same principle solves LeetCode 287 (Find Duplicate Number) in O(n) time O(1) space without modifying the array.",
    },
    {
        "id": "ds_014",
        "topic": "Data Structures",
        "difficulty": "interview",
        "q": "What are the key differences between Red-Black Trees and AVL Trees, and when would you prefer each?",
        "options": {
            "A": "Red-Black Trees are always faster than AVL Trees in all operations",
            "B": "AVL Trees are more strictly balanced (better lookup), Red-Black Trees have fewer rotations (better insert/delete). Prefer AVL for read-heavy; Red-Black for write-heavy workloads.",
            "C": "Red-Black Trees cannot store duplicate values",
            "D": "AVL Trees only work with integer keys",
        },
        "answer": "B",
        "explanation": (
            "B — AVL: height difference between siblings ≤ 1. "
            "More balanced → faster lookups (smaller height). "
            "More rotations on insert/delete to rebalance. "
            "Red-Black: allows height up to ~2log(n) via color invariants. "
            "At most 2 rotations on insert, 3 on delete → better write performance. "
            "Java TreeMap, C++ std::map, Linux CFS scheduler, nginx all use Red-Black Trees — "
            "write performance matters more than optimal lookup in most applications."
        ),
        "tip": "",
    },
    {
        "id": "ds_015",
        "topic": "Data Structures",
        "difficulty": "medium",
        "q": "What are the two main strategies for handling hash collisions, and what is the key trade-off?",
        "options": {
            "A": "Open addressing (probing within the array) vs Chaining (linked list at each bucket) — chaining handles high load factors better; open addressing has better cache locality",
            "B": "Open addressing resizes on every collision; chaining never resizes",
            "C": "Chaining is always faster than open addressing",
            "D": "Both require O(n²) space in worst case",
        },
        "answer": "A",
        "explanation": (
            "A — Chaining: each bucket holds a linked list. Simple, handles any load factor, "
            "but pointer overhead and poor cache performance. "
            "Open Addressing (linear/quadratic probing, double hashing): all keys stored in the array. "
            "Better cache performance (contiguous memory), but requires load factor < 1, prone to clustering. "
            "Java HashMap uses chaining (switches to Red-Black tree at 8 collisions per bucket). "
            "Python dict and Go map use open addressing with pseudorandom probing."
        ),
        "tip": "Load factor matters: hash tables typically resize at 0.75 (Java) or 2/3 (Python) to maintain O(1) average performance.",
    },
    {
        "id": "ds_016",
        "topic": "Data Structures",
        "difficulty": "interview",
        "q": "What data structures would you combine to implement an LRU Cache with O(1) get and O(1) put?",
        "options": {
            "A": "Two sorted arrays",
            "B": "HashMap + Doubly Linked List — map gives O(1) lookup; DLL gives O(1) move-to-front and remove-from-tail",
            "C": "Binary Search Tree only",
            "D": "Stack + Queue",
        },
        "answer": "B",
        "explanation": (
            "B — HashMap: key → node pointer (O(1) lookup). "
            "Doubly Linked List: maintains recency order (head = most recent, tail = least recent). "
            "get(key): find in map (O(1)), move node to head (O(1) with prev/next). "
            "put(key, val): if exists, update & move to head; if new, add to head; if over capacity, remove tail & map entry. "
            "All O(1). Java's LinkedHashMap is essentially this. "
            "Singly linked list fails: to remove a node you need its predecessor → O(n) traversal."
        ),
        "tip": "LRU Cache is one of the most common system design + coding questions combined. Know the implementation cold: HashMap for lookup, DLL for order.",
    },
    {
        "id": "ds_017",
        "topic": "Data Structures",
        "difficulty": "interview",
        "q": "What is a Trie and when is it better than a HashMap for string operations?",
        "options": {
            "A": "A Trie is always slower than a HashMap",
            "B": "A Trie stores strings character-by-character in a tree; enables O(m) prefix search and autocomplete that HashMap cannot do. HashMap is better for exact lookups; Trie for prefix operations.",
            "C": "A Trie is a balanced binary tree for strings",
            "D": "Tries always use less memory than HashMaps",
        },
        "answer": "B",
        "explanation": (
            "B — Trie: each edge represents a character, paths from root spell strings. "
            "O(m) insert/search where m = string length. "
            "Key advantage: prefix queries. 'Find all words starting with pre-' = traverse to 'pre' node, DFS all descendants. "
            "HashMap: O(1) exact match but cannot answer prefix queries. "
            "Tries avoid hash collisions entirely. "
            "D) Tries can use MORE memory for sparse key sets (each node may hold an array of 26 children)."
        ),
        "tip": "Used in: autocomplete (search engines), spell checkers, IP routing (prefix matching), contact search. T9 phone keyboards used tries.",
    },
    {
        "id": "ds_018",
        "topic": "Data Structures",
        "difficulty": "medium",
        "q": "Union-Find (Disjoint Set Union) with path compression and union by rank has what amortized complexity?",
        "options": {
            "A": "O(log n) per operation",
            "B": "O(n) per operation",
            "C": "O(alpha(n)) — nearly O(1), where alpha is the inverse Ackermann function",
            "D": "O(n log n) total for n operations",
        },
        "answer": "C",
        "explanation": (
            "C — Path compression (flatten tree on find) + union by rank (attach shorter tree under taller) "
            "gives amortized O(alpha(n)) per operation, where alpha(n) <= 4 for any realistic input. "
            "Practically constant time. "
            "Applications: Kruskal's MST, cycle detection in undirected graphs, connected components, "
            "network connectivity, image segmentation. "
            "Without optimizations: O(n) worst case per find."
        ),
        "tip": "Union-Find pattern: if you see 'group elements' or 'find connected components' in an interview, think Union-Find before DFS/BFS — it's often cleaner.",
    },
    {
        "id": "ds_019",
        "topic": "Data Structures",
        "difficulty": "tricky",
        "q": "What is a Bloom Filter and what is its fundamental limitation?",
        "options": {
            "A": "A Bloom Filter is a sorted array; limitation is slow insertion",
            "B": "A probabilistic data structure that answers 'definitely NOT in set' or 'PROBABLY in set' — has false positives but ZERO false negatives; cannot delete elements",
            "C": "A Bloom Filter supports deletion but with high memory cost",
            "D": "A Bloom Filter gives exact membership with O(1) lookup",
        },
        "answer": "B",
        "explanation": (
            "B — Uses multiple hash functions + a bit array. "
            "Add element: set bits at all k hash positions. "
            "Query: if ANY bit is 0 → definitely NOT in set (no false negatives). "
            "If ALL bits are 1 → PROBABLY in set (false positive possible — other elements set those bits). "
            "No deletion (clearing a bit might affect other elements). "
            "Applications: Chrome safe browsing (check malicious URL), Cassandra, HBase, "
            "Redis, web crawlers (avoid revisiting URLs)."
        ),
        "tip": "Interview question: 'A web crawler has billions of visited URLs. Exact HashSet needs TBs. What do you use?' Bloom Filter. Then discuss the false positive rate tuning.",
    },

    # ─────────────────────────── ADVANCED ALGORITHMS ──────────────────────────

    {
        "id": "algo_007",
        "topic": "Algorithms",
        "difficulty": "medium",
        "q": "Kadane's Algorithm solves which problem and in what complexity?",
        "options": {
            "A": "Maximum element in array; O(n log n)",
            "B": "Maximum sum contiguous subarray; O(n) time O(1) space",
            "C": "Sorting an array in linear time",
            "D": "Longest increasing subsequence; O(n²)",
        },
        "answer": "B",
        "explanation": (
            "B — At each index: max_here = max(arr[i], max_here + arr[i]). "
            "Track global max. O(n) time, O(1) space — a single pass. "
            "This is DP where state = 'max subarray sum ending at index i'. "
            "Edge case: if all numbers are negative, answer = max single element "
            "(handle by initializing max_so_far = arr[0] and starting at index 1)."
        ),
        "tip": "Extensions: maximum circular subarray = max(kadane_normal, totalSum - kadane_on_negated_array). 2D max sum submatrix uses Kadane as a subroutine.",
    },
    {
        "id": "algo_008",
        "topic": "Algorithms",
        "difficulty": "interview",
        "q": "Why does Dijkstra's algorithm fail with negative edge weights, and which algorithm handles them?",
        "options": {
            "A": "Dijkstra fails because it uses DFS; use BFS with negatives",
            "B": "Dijkstra's greedy assumption (settled node has final shortest path) breaks with negative edges — a later path can improve it; Bellman-Ford handles negatives in O(VE) and detects negative cycles",
            "C": "Dijkstra fails on undirected graphs; use A* for negatives",
            "D": "Negative weights are impossible in real-world graphs",
        },
        "answer": "B",
        "explanation": (
            "B — Dijkstra: once a node is extracted from the min-heap with distance d, d is assumed final. "
            "Negative edge: a later path could be d + (negative) < d, violating the assumption. "
            "Bellman-Ford: relax ALL edges V-1 times. O(VE). Correct for any weights. "
            "Detects negative cycles: if an edge can still be relaxed after V-1 iterations, a negative cycle exists. "
            "Floyd-Warshall: all-pairs shortest paths in O(V³), handles negatives (not negative cycles)."
        ),
        "tip": "Dijkstra with Fibonacci heap = O(E + V log V). For sparse graphs, nearly linear. For negatives, Bellman-Ford. Know when each applies.",
    },
    {
        "id": "algo_009",
        "topic": "Algorithms",
        "difficulty": "medium",
        "q": "Topological Sort only applies to which type of graph, and what does it produce?",
        "options": {
            "A": "Any graph; produces a sorted list by node weight",
            "B": "A Directed Acyclic Graph (DAG); produces a linear ordering where every directed edge u→v has u before v",
            "C": "Undirected graph; produces BFS traversal order",
            "D": "Weighted graph; produces shortest path",
        },
        "answer": "B",
        "explanation": (
            "B — Only DAGs support topological ordering. A cycle makes ordering impossible. "
            "Algorithms: Kahn's (BFS, uses in-degree counts) or DFS post-order reversal. "
            "Applications: build systems, package dependency resolution, course prerequisite ordering, "
            "spreadsheet evaluation, compiler instruction ordering. "
            "Cycle detection bonus: if Kahn's processes fewer than V nodes, a cycle exists."
        ),
        "tip": "",
    },
    {
        "id": "algo_010",
        "topic": "Algorithms",
        "difficulty": "medium",
        "q": "The Two-Pointer technique is most effective for which class of problems?",
        "options": {
            "A": "Finding cycles in linked lists only",
            "B": "Problems on sorted arrays/strings that would be O(n²) with nested loops — two pointers eliminate the inner loop, achieving O(n)",
            "C": "Graph traversal problems",
            "D": "Any problem with multiple arrays",
        },
        "answer": "B",
        "explanation": (
            "B — Classic examples on sorted arrays: "
            "Two Sum → left+right pointers, move based on sum vs target. "
            "Container With Most Water → move the pointer at the shorter wall. "
            "Remove duplicates in-place. Palindrome check. "
            "The key insight: on a sorted array, moving a pointer eliminates an entire half of remaining comparisons. "
            "Result: O(n) instead of O(n²) brute force."
        ),
        "tip": "",
    },
    {
        "id": "algo_011",
        "topic": "Algorithms",
        "difficulty": "medium",
        "q": "When does the Sliding Window technique apply and what is its time-complexity advantage?",
        "options": {
            "A": "For circular arrays only; reduces O(n²) to O(n log n)",
            "B": "For problems on contiguous subarrays/substrings; reduces O(n²) or O(n³) brute force to O(n) by incrementally updating the window",
            "C": "For graph shortest-path problems",
            "D": "For binary search problems",
        },
        "answer": "B",
        "explanation": (
            "B — Sliding window: expand right to include new elements, shrink left when condition is violated. "
            "Critical insight: instead of recomputing the entire window from scratch, update in O(1). "
            "Each element enters and exits the window at most once → O(n) overall. "
            "Examples: longest substring without repeating characters, minimum window substring, "
            "max sum subarray of size k, number of subarrays with product < k."
        ),
        "tip": "Fixed window: both pointers at same speed. Variable window: right always moves right; left advances only when window constraint is violated.",
    },
    {
        "id": "algo_012",
        "topic": "Algorithms",
        "difficulty": "tricky",
        "q": (
            "What does binary_search([1,2,2,2,3], 2) return with standard binary search?\n"
            "```python\n"
            "def binary_search(arr, target):\n"
            "    lo, hi = 0, len(arr) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] == target: return mid\n"
            "        elif arr[mid] < target: lo = mid + 1\n"
            "        else: hi = mid - 1\n"
            "    return -1\n"
            "```"
        ),
        "options": {
            "A": "0 — first occurrence",
            "B": "2 — middle index (standard binary search finds ANY match, not first/last)",
            "C": "4 — last occurrence",
            "D": "-1 — not found",
        },
        "answer": "B",
        "explanation": (
            "B — Standard binary search returns ANY match. "
            "Array=[1,2,2,2,3], target=2: lo=0,hi=4 → mid=2, arr[2]=2 → return 2. "
            "This is the classic trap: if you need FIRST occurrence, when arr[mid]==target "
            "set hi=mid-1 and record mid. For LAST occurrence: set lo=mid+1 and record mid. "
            "Always clarify with interviewer: first, last, or any occurrence?"
        ),
        "tip": "Binary search variations are extremely common in interviews. Master: exact match, first occurrence, last occurrence, 'insert position' (lo after the loop).",
    },
    {
        "id": "algo_013",
        "topic": "Algorithms",
        "difficulty": "interview",
        "q": "Why does greedy fail for the Coin Change problem in general?",
        "options": {
            "A": "Greedy always works for coin change",
            "B": "Greedy (pick largest coin ≤ remaining) fails for non-standard coin systems. Example: coins=[1,3,4], N=6 → greedy: 4+1+1=3 coins; optimal: 3+3=2 coins. Use DP: O(N×coins).",
            "C": "Greedy fails because coins cannot be reused",
            "D": "There is no polynomial solution for coin change",
        },
        "answer": "B",
        "explanation": (
            "B — Greedy works for US coins (1,5,10,25) because they have the greedy property, "
            "but this must be proven — it's NOT universally true. "
            "Counter-example: coins=[1,3,4], amount=6. Greedy: 4+1+1=3 coins. DP optimal: 3+3=2 coins. "
            "DP: dp[0]=0, dp[i] = min(dp[i-c]+1) for each coin c≤i. "
            "Time: O(N × |coins|), Space: O(N). "
            "This demonstrates why greedy requires an exchange argument proof."
        ),
        "tip": "Key rule: always prove greedy correctness with an exchange argument. 'It seems right' is not a proof. Greedy works for Interval Scheduling, Huffman, MST — all provable.",
    },
    {
        "id": "algo_014",
        "topic": "Algorithms",
        "difficulty": "interview",
        "q": "When should you use Dynamic Programming vs Backtracking?",
        "options": {
            "A": "DP is for graphs; backtracking is for trees",
            "B": "DP: overlapping subproblems + optimal substructure → memoize results. Backtracking: enumerate all solutions with pruning. When backtracking + memoization → essentially top-down DP.",
            "C": "Backtracking is always slower than DP",
            "D": "They are the same technique with different names",
        },
        "answer": "B",
        "explanation": (
            "B — DP (memoization/tabulation): compute each subproblem once, reuse. "
            "Best for: optimization (min/max), counting problems, sequence problems (LCS, LIS, Knapsack). "
            "Backtracking: build solution incrementally, undo (backtrack) on dead ends. "
            "Best for: enumeration (N-Queens, Sudoku, generate all permutations/subsets). "
            "Key distinction: DP avoids recomputing identical states. "
            "Backtracking may revisit states unless memoized."
        ),
        "tip": "'Number of ways' or 'minimum cost' → DP. 'Generate all solutions' → backtracking. 'Generate all + count distinct' → backtracking with memoization = DP.",
    },
    {
        "id": "algo_015",
        "topic": "Algorithms",
        "difficulty": "tricky",
        "q": (
            "What does this bit manipulation expression compute?\n"
            "```python\n"
            "n = n & (n - 1)\n"
            "```"
        ),
        "options": {
            "A": "Checks if n is even",
            "B": "Clears the lowest set (1) bit of n — n & (n-1) always removes exactly the rightmost 1 bit",
            "C": "Sets all bits to 1",
            "D": "Reverses the bits of n",
        },
        "answer": "B",
        "explanation": (
            "B — n-1 flips the lowest set bit to 0 and all lower bits to 1. "
            "ANDing with n clears those bits. "
            "n=12 (1100), n-1=11 (1011), 12&11=8 (1000). Lowest set bit cleared. "
            "Applications: "
            "1. Count set bits (Brian Kernighan): 'while n: count++; n &= n-1' → O(k) where k=set bits. "
            "2. Power of 2 check: n>0 and (n & (n-1))==0 (exactly one bit set)."
        ),
        "tip": "Bit manipulation fluency is a differentiator in interviews. Know: n&(n-1) clears lowest bit, n&(-n) isolates lowest bit, n^n=0, n^0=n.",
    },
    {
        "id": "algo_016",
        "topic": "Algorithms",
        "difficulty": "medium",
        "q": "What is the time complexity of building a heap from n elements using heapify?",
        "options": {
            "A": "O(n log n) — same as inserting n elements one by one",
            "B": "O(n) — heapify-from-bottom is linear despite appearing quadratic",
            "C": "O(log n)",
            "D": "O(n²)",
        },
        "answer": "B",
        "explanation": (
            "B — Classic interview trap: build-heap is O(n), NOT O(n log n). "
            "Start from the last non-leaf and sift down. "
            "Half the nodes are leaves (0 work), quarter have height 1 (1 sift), etc. "
            "Total: sum over height h of (n/2^(h+1)) * h = O(n). "
            "Inserting n elements one-by-one (sift up each) = O(n log n). "
            "This is why Heap Sort's build phase is O(n) even though total sort is O(n log n)."
        ),
        "tip": "Proving O(n) requires summing the series: sum_{h=0}^{log n} h * n/2^(h+1) = O(n). Know this proof — it impresses interviewers.",
    },
    {
        "id": "algo_017",
        "topic": "Algorithms",
        "difficulty": "medium",
        "q": "What is the time complexity of the Longest Common Subsequence (LCS) DP solution?",
        "options": {
            "A": "O(n + m)",
            "B": "O(n * m) time, reducible to O(min(n,m)) space",
            "C": "O(n log n)",
            "D": "O(2^n) exponential",
        },
        "answer": "B",
        "explanation": (
            "B — dp[i][j] = LCS length of s1[:i] and s2[:j]. "
            "If s1[i-1]==s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1. "
            "Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1]). "
            "Fill (n+1)*(m+1) table → O(n*m) time and space. "
            "Space optimization: only previous row needed → O(min(n,m)) space. "
            "D) Naive recursion without memoization IS O(2^n) — DP is the fix."
        ),
        "tip": "LCS is foundational for: git diff (longest common substring), DNA alignment, plagiarism detection. Understand it deeply — many DP problems reduce to variants of LCS.",
    },

    # ─────────────────────── OOP & DESIGN PATTERNS ────────────────────────────

    {
        "id": "oop_006",
        "topic": "Object-Oriented Programming",
        "difficulty": "interview",
        "q": "What is the Singleton pattern's main thread-safety issue in Java?",
        "options": {
            "A": "Singleton cannot be serialized",
            "B": "Naive lazy initialization is not thread-safe: two threads can both see null and both create instances. Fix: double-checked locking with volatile, eager init, or Bill Pugh (inner static class).",
            "C": "Singleton automatically handles thread safety",
            "D": "The problem only affects Python, not Java",
        },
        "answer": "B",
        "explanation": (
            "B — 'if (instance==null) instance = new Singleton()' is not atomic. "
            "Two threads both pass the null check before either creates the instance → two instances. "
            "Fix 1: Eager init: static final Singleton INSTANCE = new Singleton() — JVM guarantees thread safety at class load. "
            "Fix 2: synchronized getInstance() — correct but slow (lock on every call). "
            "Fix 3: Double-checked locking + volatile — lock only when null, volatile prevents instruction reorder. "
            "Fix 4: Bill Pugh (inner static holder class) — lazy, thread-safe, no synchronization needed. "
            "Fix 5: Enum Singleton — best: thread-safe, serialization-safe, reflection-proof."
        ),
        "tip": "In Java, the enum Singleton is the most recommended approach (Joshua Bloch, Effective Java). In Python, module-level singleton is idiomatic.",
    },
    {
        "id": "oop_007",
        "topic": "Object-Oriented Programming",
        "difficulty": "medium",
        "q": "What is the difference between Factory Method and Abstract Factory design patterns?",
        "options": {
            "A": "They are identical",
            "B": "Factory Method creates ONE product type; Abstract Factory creates FAMILIES of related products ensuring consistency",
            "C": "Abstract Factory only works with interfaces",
            "D": "Factory Method is for runtime; Abstract Factory for compile-time",
        },
        "answer": "B",
        "explanation": (
            "B — Factory Method: interface for creating one object type, subclasses choose the implementation. "
            "Example: Logger factory returning FileLogger or ConsoleLogger. "
            "Abstract Factory: creates a family of related objects. "
            "Example: UI factory producing Button + Checkbox + Textbox all consistent for Windows or Mac theme. "
            "If a new Windows Button is added, its matching Checkbox and Textbox come from the same factory, "
            "ensuring visual consistency. "
            "Rule: one product type → Factory Method. Product family → Abstract Factory."
        ),
        "tip": "",
    },
    {
        "id": "oop_008",
        "topic": "Object-Oriented Programming",
        "difficulty": "interview",
        "q": "Which classic example VIOLATES the Liskov Substitution Principle?",
        "options": {
            "A": "Dog extends Animal",
            "B": "Square extends Rectangle — setWidth(5) on a Square changes height too, breaking Rectangle's contract that width and height are independent",
            "C": "ArrayList implements List",
            "D": "FileLogger implements Logger",
        },
        "answer": "B",
        "explanation": (
            "B — Rectangle contract: setWidth and setHeight are independent. "
            "Square override must keep width==height, so setWidth(5) also sets height to 5. "
            "Code for Rectangle: 'r.setWidth(5); r.setHeight(3); assert r.area()==15' — FAILS with Square (area=9). "
            "LSP: objects of subtype must be substitutable without breaking the program. "
            "Square breaks this. Fix: use a common Shape interface — don't make Square extend Rectangle."
        ),
        "tip": "LSP violations signal a modeling problem. Mathematical 'is-a' doesn't always equal OOP inheritance. Test: can you substitute child for parent everywhere without breaking correctness?",
    },
    {
        "id": "oop_009",
        "topic": "Object-Oriented Programming",
        "difficulty": "medium",
        "q": "What is the Observer pattern and name a real-world example?",
        "options": {
            "A": "Observer allows one object to copy another's private state",
            "B": "One-to-many dependency: when Subject changes state, all Observers are notified automatically. Used in: React state (component re-renders), event listeners, Kafka/RabbitMQ pub-sub, MVC (View observes Model).",
            "C": "Observer creates object copies",
            "D": "Observer only works in single-threaded apps",
        },
        "answer": "B",
        "explanation": (
            "B — Subject (publisher) maintains a list of observers and calls update() on all when state changes. "
            "Observers implement an update() interface. "
            "Benefits: loose coupling — Subject doesn't know Observer implementation details. "
            "Examples: Java EventListener, React useEffect, RxJava/Reactive Streams, "
            "DOM event system, Angular change detection."
        ),
        "tip": "",
    },
    {
        "id": "oop_010",
        "topic": "Object-Oriented Programming",
        "difficulty": "medium",
        "q": "What does the Dependency Inversion Principle state and how does Dependency Injection implement it?",
        "options": {
            "A": "High-level modules should directly instantiate low-level modules for efficiency",
            "B": "High-level modules should depend on abstractions (interfaces), not concrete classes. DI provides the concrete implementation from outside, enabling swapping and mocking.",
            "C": "DI means creating all objects in main()",
            "D": "It only applies to database connections",
        },
        "answer": "B",
        "explanation": (
            "B — Without DI: 'class UserService { EmailSender s = new EmailSender(); }' — tightly coupled. "
            "With DI: 'class UserService { UserService(MessageSender s) {} }' — inject any MessageSender. "
            "Benefits: testability (inject mock), flexibility (swap Email→SMS), reduced coupling. "
            "Frameworks: Spring IoC, Angular DI, .NET built-in DI."
        ),
        "tip": "The D in SOLID is most impactful for testability. If you can't easily unit test a class in isolation, you're likely violating DIP.",
    },
    {
        "id": "oop_011",
        "topic": "Object-Oriented Programming",
        "difficulty": "tricky",
        "q": (
            "What does this Java code print? (Static method in parent and child)\n"
            "```java\n"
            "class Base {\n"
            "    static void show() { System.out.println(\"Base\"); }\n"
            "}\n"
            "class Child extends Base {\n"
            "    static void show() { System.out.println(\"Child\"); }\n"
            "}\n"
            "Base obj = new Child();\n"
            "obj.show();\n"
            "```"
        ),
        "options": {
            "A": "Child",
            "B": "Base — static methods are resolved at compile time by reference type, not object type (method hiding, not overriding)",
            "C": "Compilation error",
            "D": "Runtime exception",
        },
        "answer": "B",
        "explanation": (
            "B — Static methods belong to the class, not the object. "
            "They are resolved at COMPILE TIME based on the declared reference type (Base), not the actual object type (Child). "
            "This is called METHOD HIDING, not overriding. "
            "Polymorphism does NOT apply to static methods. "
            "If show() were instance methods, the answer would be 'Child' (runtime dispatch). "
            "Trying to put @Override on a static method causes a compile error."
        ),
        "tip": "Critical Java trap: static methods are never polymorphic. Always call static methods on the class name (Base.show()), not on an instance, to make the intent clear.",
    },
    {
        "id": "oop_012",
        "topic": "Object-Oriented Programming",
        "difficulty": "medium",
        "q": "What does the Open/Closed Principle mean in practice?",
        "options": {
            "A": "Classes should always be open to modification when adding features",
            "B": "Classes should be open for EXTENSION (add behavior via new classes/interfaces) but CLOSED for MODIFICATION (don't change existing tested code)",
            "C": "Open source code is better than closed source",
            "D": "Files should be opened before reading",
        },
        "answer": "B",
        "explanation": (
            "B — Bad: add a new payment type by adding an 'if' branch in processPayment(). Modifies tested code. "
            "Good: define PaymentMethod interface; add class StripePayment implements PaymentMethod. "
            "Existing code untouched. New class independently tested. "
            "Achieved via: interfaces, abstract classes, Strategy pattern, plugin systems."
        ),
        "tip": "",
    },
    {
        "id": "oop_013",
        "topic": "Object-Oriented Programming",
        "difficulty": "medium",
        "q": "What is the Strategy pattern and how does it differ from using inheritance to vary behavior?",
        "options": {
            "A": "Strategy modifies the parent class at runtime",
            "B": "Strategy encapsulates interchangeable algorithms as objects, injected via composition — enables runtime behavior switching without subclassing",
            "C": "Strategy only applies to sorting",
            "D": "Strategy and inheritance are identical in practice",
        },
        "answer": "B",
        "explanation": (
            "B — Inheritance to vary behavior: class NaturalSort extends Sort, class ReverseSort extends Sort — "
            "rigid, compile-time decision, class explosion. "
            "Strategy: sort() accepts a Comparator (strategy object). "
            "Pass any Comparator at runtime: naturalOrder(), reverseOrder(), customComparator. "
            "This is 'program to an interface, not an implementation'. "
            "Java's Comparator, Python's sorted(key=...) are classic examples."
        ),
        "tip": "",
    },

    # ─────────────────────────── ADVANCED OS ──────────────────────────────────

    {
        "id": "os_006",
        "topic": "Operating Systems",
        "difficulty": "interview",
        "q": "What is the key difference between a Mutex and a Semaphore?",
        "options": {
            "A": "A Mutex can be released by any thread; Semaphore is released by its owner",
            "B": "Mutex has OWNERSHIP — only the locking thread can unlock it (mutual exclusion). Semaphore is a signaling counter with NO ownership — any thread can signal. Counting semaphore allows N concurrent accesses.",
            "C": "Semaphores are only in Linux kernel",
            "D": "They are the same with different names",
        },
        "answer": "B",
        "explanation": (
            "B — Mutex: binary lock with ownership. Used to protect a critical section (one thread at a time). "
            "Only the thread that acquired the mutex can release it. "
            "Semaphore: a counter (0 to N). wait() decrements (blocks if 0). signal() increments. "
            "No ownership concept — any thread can signal, even one that didn't wait. "
            "Binary semaphore (0/1) resembles a mutex but lacks ownership — different semantics. "
            "Use mutex for mutual exclusion; semaphore for signaling (Producer-Consumer) or resource counting."
        ),
        "tip": "Mutex = mutual exclusion with ownership. Semaphore = signaling + resource counting. A mutex is not just a binary semaphore — the ownership distinction matters for debugging and correctness.",
    },
    {
        "id": "os_007",
        "topic": "Operating Systems",
        "difficulty": "medium",
        "q": "What is Thrashing and how can it be prevented?",
        "options": {
            "A": "CPU running too many threads; prevented by fewer cores",
            "B": "A process spends more time swapping pages to/from disk than executing because its working set exceeds physical memory. Prevented by working set model or reducing multiprogramming degree.",
            "C": "Disk I/O is too slow; prevented by SSD",
            "D": "Network packets are dropped; prevented by flow control",
        },
        "answer": "B",
        "explanation": (
            "B — Thrashing symptom: high page fault rate, low CPU utilization (CPU waits for disk). "
            "Detection: OS sees many page faults while CPU is near-idle. "
            "Prevention: "
            "1. Working Set Model: only keep pages a process actively uses (working set). "
            "2. Page Fault Frequency Control: give more frames to processes with high fault rates. "
            "3. Reduce degree of multiprogramming: suspend some processes to free memory. "
            "4. Prepaging: load expected pages before they're needed."
        ),
        "tip": "",
    },
    {
        "id": "os_008",
        "topic": "Operating Systems",
        "difficulty": "medium",
        "q": "What is the difference between a System Call and a regular function call?",
        "options": {
            "A": "System calls are faster because they skip userspace",
            "B": "A system call crosses user-mode → kernel-mode boundary via a trap/interrupt, involves privilege elevation, and is 100-1000x slower than a regular function call that stays in user space",
            "C": "System calls are only made in C",
            "D": "Regular function calls require network access",
        },
        "answer": "B",
        "explanation": (
            "B — Regular function call: CPU jumps to a memory address in userspace, no privilege change. ~nanoseconds. "
            "System call: triggers a software trap, CPU switches ring 3 (user) → ring 0 (kernel), "
            "executes OS code, switches back. ~hundreds of nanoseconds to microseconds. "
            "This is why: database connection pools exist (reuse connections to avoid repeated open() syscalls), "
            "buffered I/O batches writes (one write() call for many small writes), "
            "zero-copy sendfile() avoids user-space buffer copies."
        ),
        "tip": "In Linux, use 'strace' to trace system calls. The vDSO (virtual dynamic shared object) allows some syscalls like clock_gettime() to execute in user space, avoiding full context switch.",
    },
    {
        "id": "os_009",
        "topic": "Operating Systems",
        "difficulty": "interview",
        "q": "What is Priority Inversion and how was it demonstrated in the Mars Pathfinder?",
        "options": {
            "A": "High-priority tasks always complete first — no inversion possible",
            "B": "High-priority task H blocks waiting for a mutex held by low-priority task L, which is preempted by medium-priority M — H effectively runs at low priority. Mars Pathfinder experienced watchdog resets due to this.",
            "C": "Priority is assigned in reverse order by the scheduler",
            "D": "A process priority is manually lowered by an admin",
        },
        "answer": "B",
        "explanation": (
            "B — L holds mutex. H needs mutex → H blocks. M (needs no mutex) preempts L. "
            "Now M runs while H waits — H (highest priority) runs last! "
            "Mars Pathfinder 1997: high-priority meteorological task blocked by low-priority bus management task. "
            "Watchdog timer repeatedly reset the spacecraft. "
            "Fix: Priority Inheritance Protocol — temporarily raise L's priority to H's level while L holds the mutex. "
            "Solution was uploaded remotely to Mars."
        ),
        "tip": "Priority Inheritance is enabled by PTHREAD_PRIO_INHERIT flag in POSIX. Real-time embedded systems (RTOS) always need to handle this.",
    },
    {
        "id": "os_010",
        "topic": "Operating Systems",
        "difficulty": "medium",
        "q": "What is the difference between internal and external fragmentation?",
        "options": {
            "A": "Internal fragmentation is in networks; external is in files",
            "B": "Internal: wasted space WITHIN an allocated block (block > request). External: total free memory is sufficient, but fragmented into non-contiguous chunks too small to satisfy a large request.",
            "C": "Both only occur in virtual memory",
            "D": "External in fixed-size; internal in variable-size allocation",
        },
        "answer": "B",
        "explanation": (
            "B — Internal fragmentation: request 100 bytes, get 128-byte block → 28 bytes wasted inside. "
            "Caused by fixed-size pages/blocks. "
            "External fragmentation: total free = 200 bytes, but largest contiguous free = 60 bytes. "
            "Request for 100 bytes fails. Caused by variable-size allocation and deallocation over time. "
            "Paging: eliminates external fragmentation (fixed page sizes) but causes internal. "
            "Segmentation: causes external fragmentation. "
            "Solutions: compaction, buddy system, slab allocator (for fixed-size kernel objects)."
        ),
        "tip": "",
    },

    # ──────────────────────── ADVANCED NETWORKS ───────────────────────────────

    {
        "id": "net_006",
        "topic": "Computer Networks",
        "difficulty": "interview",
        "q": "What key steps occur during a TLS/HTTPS handshake before data is transmitted?",
        "options": {
            "A": "Only the password is encrypted; other data is plain text",
            "B": "Client and server negotiate TLS version/cipher, server sends certificate with public key, exchange key material via Diffie-Hellman to derive shared symmetric session keys, then use fast symmetric encryption (AES) for data",
            "C": "Server encrypts data with client's password hash",
            "D": "TLS only adds a checksum to HTTP packets",
        },
        "answer": "B",
        "explanation": (
            "B — TLS 1.3 handshake (simplified): "
            "1. ClientHello: TLS version, ciphers, key share (Diffie-Hellman public key). "
            "2. ServerHello: chosen cipher, certificate, key share, signature. "
            "3. Client verifies certificate against trusted CA chain. "
            "4. Both sides derive the same session key (neither transmitted directly). "
            "5. All application data encrypted with AES. "
            "Asymmetric crypto (RSA/ECDH) used only for key exchange — ~1000x slower than AES. "
            "TLS 1.3: 1-RTT handshake (down from 2-RTT in TLS 1.2)."
        ),
        "tip": "Perfect Forward Secrecy (PFS): TLS 1.3 mandates ephemeral DH key exchange — even if the server's private key is later compromised, past sessions cannot be decrypted.",
    },
    {
        "id": "net_007",
        "topic": "Computer Networks",
        "difficulty": "medium",
        "q": "What is CORS and why does the browser enforce it?",
        "options": {
            "A": "A server-side firewall rule blocking all external requests",
            "B": "A browser security mechanism blocking JavaScript from reading responses from a different origin — prevents malicious sites from reading your bank data using your cookies",
            "C": "Only relevant for mobile apps",
            "D": "Blocks image loading from external domains",
        },
        "answer": "B",
        "explanation": (
            "B — Same-Origin Policy: JS can only read responses from its own origin (protocol+domain+port). "
            "CORS allows servers to explicitly grant cross-origin access via response headers. "
            "Without CORS: evil.com JS could fetch bank.com/account using your stored cookies and read the response. "
            "Preflight: for non-simple requests, browser sends OPTIONS first. "
            "Server responds with Access-Control-Allow-Origin if allowed. "
            "CORS is enforced by the BROWSER only — server-to-server calls are not restricted."
        ),
        "tip": "Common dev mistake: 'CORS error' looks like a server error but it's a browser security feature. The fix belongs on the server (add CORS headers), not the browser or client.",
    },
    {
        "id": "net_008",
        "topic": "Computer Networks",
        "difficulty": "medium",
        "q": "What is HTTP/2's main improvement over HTTP/1.1?",
        "options": {
            "A": "HTTP/2 is encrypted by default; HTTP/1.1 is not",
            "B": "HTTP/2 multiplexing: multiple request/response streams simultaneously over ONE TCP connection, eliminating per-resource connection overhead and head-of-line blocking",
            "C": "HTTP/2 uses UDP instead of TCP",
            "D": "HTTP/2 compresses only the response body",
        },
        "answer": "B",
        "explanation": (
            "B — HTTP/1.1: one request per TCP connection at a time. Browsers open 6 connections per domain as workaround. "
            "HTTP/2 multiplexing: stream many requests/responses on one connection simultaneously. "
            "Also adds: HPACK header compression (drastically reduces repeated header overhead), "
            "server push (send CSS/JS before client requests them), binary framing. "
            "HTTP/3 goes further: QUIC (UDP-based) eliminates TCP-level head-of-line blocking."
        ),
        "tip": "",
    },
    {
        "id": "net_009",
        "topic": "Computer Networks",
        "difficulty": "tricky",
        "q": "What is the difference between WebSockets and HTTP long-polling for real-time communication?",
        "options": {
            "A": "Identical in performance",
            "B": "WebSockets: persistent full-duplex connection, ~2-byte frame overhead. Long-polling: client reopens an HTTP connection after each response, ~700-byte header overhead per message. WebSockets are far more efficient.",
            "C": "Long-polling is always faster than WebSockets",
            "D": "WebSockets only work over HTTP/2",
        },
        "answer": "B",
        "explanation": (
            "B — Long-polling: client sends request → server holds it until data available → "
            "client immediately re-requests. Repeated HTTP handshakes, large headers, latency. "
            "WebSocket: client sends HTTP Upgrade request → connection upgrades to WebSocket protocol. "
            "Persistent bidirectional channel with minimal framing (~2 bytes vs ~700 bytes HTTP headers). "
            "Perfect for: chat, live scores, collaborative editing, stock feeds. "
            "SSE (Server-Sent Events): server-push only, simpler, auto-reconnect, good for dashboards."
        ),
        "tip": "Choose: bidirectional real-time → WebSocket. Server-push only → SSE. Avoid long-polling unless WebSocket is blocked.",
    },
    {
        "id": "net_010",
        "topic": "Computer Networks",
        "difficulty": "medium",
        "q": "What is NAT (Network Address Translation) and what problem does it solve?",
        "options": {
            "A": "NAT translates domain names to IP addresses",
            "B": "NAT allows many devices with private IPs to share a single public IP by remapping source ports, solving IPv4 address exhaustion",
            "C": "NAT encrypts network traffic between routers",
            "D": "NAT is only used in mobile networks",
        },
        "answer": "B",
        "explanation": (
            "B — IPv4: ~4.3 billion addresses, far fewer than internet-connected devices. "
            "NAT: router has one public IP. Internal devices have private IPs (192.168.x.x, 10.x.x.x). "
            "Outgoing packet: router replaces private_ip:port with public_ip:unique_port. "
            "Tracks the mapping table. Incoming response: routes to correct internal device. "
            "Downside: breaks end-to-end principle — devices behind NAT aren't directly addressable. "
            "Peer-to-peer (video calls) requires NAT traversal techniques (STUN, TURN, ICE). "
            "IPv6 (128-bit) provides enough addresses to eliminate NAT."
        ),
        "tip": "",
    },
    {
        "id": "net_011",
        "topic": "Computer Networks",
        "difficulty": "interview",
        "q": "What are the key DNS record types and their purposes?",
        "options": {
            "A": "DNS only has one type: A records",
            "B": "A (IPv4), AAAA (IPv6), CNAME (alias to another hostname), MX (mail server), TXT (arbitrary text / SPF / domain verification), NS (authoritative nameserver), SOA (zone authority info)",
            "C": "DNS records are only for email",
            "D": "CNAME and A records are identical",
        },
        "answer": "B",
        "explanation": (
            "B — A: example.com → 93.184.216.34. "
            "AAAA: example.com → ::1 (IPv6). "
            "CNAME: www.example.com → example.com (cannot coexist with other records at same name). "
            "MX: mail.example.com with priority. "
            "TXT: arbitrary text — SPF (anti-spam), DKIM (email signing), Google/AWS domain verification. "
            "NS: which nameservers are authoritative for the domain. "
            "Gotcha: CNAME at root domain (example.com) conflicts with SOA/NS records — use ALIAS/ANAME."
        ),
        "tip": "Common interview: 'Use CNAME for www.example.com to point to example.com. Use A for root domain.' You cannot use CNAME for root because it conflicts with required NS/SOA records.",
    },

    # ──────────────────────── ADVANCED DATABASES ──────────────────────────────

    {
        "id": "db_007",
        "topic": "Databases",
        "difficulty": "interview",
        "q": "What is the CAP Theorem and what does it mean for distributed databases?",
        "options": {
            "A": "A system can achieve all three: Consistency, Availability, Partition Tolerance simultaneously",
            "B": "During a network partition, a distributed system must choose between Consistency (correct data or error) and Availability (response, possibly stale). Network partitions are inevitable → real systems are CP or AP.",
            "C": "CAP only applies to relational databases",
            "D": "CAP means databases must be SQL or NoSQL",
        },
        "answer": "B",
        "explanation": (
            "B — CAP (Brewer 2000): Consistency (all nodes return same data), "
            "Availability (every request gets a response), Partition Tolerance (works despite network splits). "
            "Since network partitions are inevitable in distributed systems, you choose: "
            "CP: consistent but may reject requests during partition. "
            "Examples: HBase, ZooKeeper, etcd, MongoDB (default). "
            "AP: always available but may return stale data. "
            "Examples: Cassandra, DynamoDB (default), CouchDB. "
            "Modern refinement: PACELC also captures latency vs consistency trade-off when there's NO partition."
        ),
        "tip": "Cassandra: tunable consistency (ONE, QUORUM, ALL). QUORUM (majority) gives 'consistent enough' for most cases. ALL gives strong consistency but lowest availability.",
    },
    {
        "id": "db_008",
        "topic": "Databases",
        "difficulty": "medium",
        "q": "What is the N+1 query problem in ORMs and how do you fix it?",
        "options": {
            "A": "A table with N+1 rows causes a query to fail",
            "B": "Fetching N records runs 1 query for the list then N queries for each record's related data. Fix: use JOIN or eager loading (include/select_related in the ORM).",
            "C": "N+1 indexes on a table slow down inserts",
            "D": "A query returning N+1 rows instead of N",
        },
        "answer": "B",
        "explanation": (
            "B — Example: 1 query SELECT * FROM orders (N orders returned). "
            "Then N queries: SELECT * FROM customers WHERE id = ? for each order. "
            "Total: N+1 queries when 1 JOIN suffices. "
            "Fix: JOIN, or ORM eager loading: "
            "Django: Order.objects.select_related('customer'). "
            "Rails: Order.includes(:customer). "
            "JPA: @ManyToOne(fetch=EAGER) or JOIN FETCH in JPQL. "
            "Symptoms: dev tools show dozens of identical queries with different IDs."
        ),
        "tip": "Always log SQL in development! If you see the same query repeating N times with different IDs, you have N+1. Tools: Django Debug Toolbar, Laravel Debugbar, Hibernate statistics.",
    },
    {
        "id": "db_009",
        "topic": "Databases",
        "difficulty": "interview",
        "q": "What is database sharding and what challenges does it introduce?",
        "options": {
            "A": "Sharding replicates data to multiple servers for read scaling",
            "B": "Sharding horizontally partitions data across multiple databases (each holds a subset of rows), enabling write scaling, but introducing: cross-shard queries, re-sharding complexity, distributed transactions",
            "C": "Sharding compresses data to reduce storage",
            "D": "Sharding is a backup strategy",
        },
        "answer": "B",
        "explanation": (
            "B — Strategies: range (user_id 1-1M on shard 1), hash (hash(user_id) % N), "
            "directory (lookup table maps keys to shards). "
            "Benefits: each shard handles fraction of writes, horizontal scalability. "
            "Challenges: "
            "Cross-shard JOINs: must query multiple shards and merge in app. "
            "Re-sharding: adding a shard requires redistributing data (consistent hashing helps). "
            "Distributed transactions: ACID across shards requires 2PC or Saga pattern. "
            "Hotspots: celebrity user problem (one shard overloaded)."
        ),
        "tip": "Don't shard prematurely. Use read replicas and caching first. Sharding is a last resort due to operational complexity. Instagram ran on a single PostgreSQL server for a long time.",
    },
    {
        "id": "db_010",
        "topic": "Databases",
        "difficulty": "tricky",
        "q": "What is MVCC (Multi-Version Concurrency Control) and what problem does it solve?",
        "options": {
            "A": "MVCC uses locks to prevent concurrent reads and writes",
            "B": "MVCC maintains multiple row versions — readers see a consistent snapshot as of their transaction start, without blocking writers. Writers never block readers.",
            "C": "MVCC is only in NoSQL databases",
            "D": "MVCC prevents all dirty reads with pessimistic locking",
        },
        "answer": "B",
        "explanation": (
            "B — Traditional locking: writer blocks reader, reader blocks writer → poor concurrency. "
            "MVCC: updating a row creates a new version; old version kept for concurrent readers. "
            "Each transaction sees a snapshot from its start timestamp. "
            "Readers never block writers. Writers never block readers. "
            "Solves: dirty reads, non-repeatable reads (depending on isolation level). "
            "Used by: PostgreSQL, MySQL InnoDB, Oracle, SQL Server, CockroachDB. "
            "Downside: old versions must be cleaned up (VACUUM in PostgreSQL)."
        ),
        "tip": "Long-running transactions in PostgreSQL prevent VACUUM from removing old row versions → table bloat. This is why transaction duration monitoring matters in production.",
    },
    {
        "id": "db_011",
        "topic": "Databases",
        "difficulty": "medium",
        "q": "What is the difference between a clustered index and a non-clustered index?",
        "options": {
            "A": "Clustered sorts alphabetically; non-clustered sorts numerically",
            "B": "Clustered index: rows stored on disk in index order (one per table, usually PK). Non-clustered: separate B-tree with key → row pointer; extra hop to fetch row data.",
            "C": "Non-clustered indexes are always on foreign keys",
            "D": "Both store identical data structures",
        },
        "answer": "B",
        "explanation": (
            "B — Clustered: table data IS the index. Range queries on PK are fast (contiguous disk pages). "
            "Only ONE clustered index per table. "
            "MySQL InnoDB: PK is always clustered. "
            "Non-clustered: separate structure. Lookup = find in secondary index (key), get PK/row pointer, "
            "then look up in clustered index. Two B-tree traversals in MySQL InnoDB. "
            "Why PK queries are fastest: only one B-tree traversal."
        ),
        "tip": "In MySQL InnoDB, secondary indexes store the PK value (not physical row pointer) as the 'row locator'. Changing the PK requires rebuilding ALL secondary indexes — choose PK wisely.",
    },
    {
        "id": "db_012",
        "topic": "Databases",
        "difficulty": "interview",
        "q": "What are the four database isolation levels and what anomalies does each prevent?",
        "options": {
            "A": "There is only one isolation level: SERIALIZABLE",
            "B": "Read Uncommitted → dirty reads allowed. Read Committed → prevents dirty reads. Repeatable Read → prevents non-repeatable reads. Serializable → prevents all anomalies. Higher isolation = lower concurrency.",
            "C": "Isolation levels only apply to NoSQL",
            "D": "SERIALIZABLE is the default in all databases",
        },
        "answer": "B",
        "explanation": (
            "B — Anomalies: "
            "Dirty Read: read uncommitted data from another transaction. "
            "Non-Repeatable Read: same row read twice returns different values (committed change in between). "
            "Phantom Read: same query returns different rows (another transaction inserted/deleted rows). "
            "Levels: "
            "READ UNCOMMITTED: all anomalies possible. "
            "READ COMMITTED (default in PostgreSQL, Oracle): prevents dirty reads only. "
            "REPEATABLE READ (default in MySQL InnoDB): prevents dirty + non-repeatable. "
            "SERIALIZABLE: prevents all — transactions appear sequential."
        ),
        "tip": "Most web apps use READ COMMITTED. Financial transactions (double-spend prevention) may need SERIALIZABLE. Higher isolation = more locking = lower throughput.",
    },

    # ─────────────────────── PROGRAMMING CONCEPTS ─────────────────────────────

    {
        "id": "prog_003",
        "topic": "Programming Fundamentals",
        "difficulty": "tricky",
        "q": (
            "What is the output? (Java is always pass-by-value)\n"
            "```java\n"
            "void modify(int x, int[] arr) {\n"
            "    x = 100;\n"
            "    arr[0] = 100;\n"
            "}\n"
            "int a = 5; int[] b = {1,2,3};\n"
            "modify(a, b);\n"
            "System.out.println(a + \" \" + b[0]);\n"
            "```"
        ),
        "options": {
            "A": "5 1",
            "B": "100 100",
            "C": "5 100",
            "D": "100 1",
        },
        "answer": "C",
        "explanation": (
            "C — Java is always pass-by-value. "
            "Primitive a=5: a copy (5) is passed as x. x=100 only changes the local copy. a remains 5. "
            "Array b: the VALUE of the reference (memory address of the array) is copied. "
            "arr and b point to the SAME array object in heap. arr[0]=100 modifies the shared array. "
            "b[0] = 100. "
            "This is NOT pass-by-reference — you cannot rebind b to a new array from inside modify()."
        ),
        "tip": "The confusion: 'value of an object variable' IS the reference (pointer). You can mutate the object's contents but cannot rebind the caller's variable to a new object.",
    },
    {
        "id": "prog_004",
        "topic": "Programming Fundamentals",
        "difficulty": "interview",
        "q": "Can Java have memory leaks despite having a garbage collector?",
        "options": {
            "A": "No — GC eliminates all memory leaks",
            "B": "Yes — GC only collects unreachable objects. Holding references to unused objects (e.g., in a static collection, underegistered listeners) prevents GC → logical memory leak",
            "C": "Java memory leaks only occur in native code (JNI)",
            "D": "Memory leaks crash the JVM immediately",
        },
        "answer": "B",
        "explanation": (
            "B — Common Java memory leaks: "
            "1. Static collections that grow but never shrink (static Map<K,V> cache). "
            "2. Event listeners registered but never removed. "
            "3. Unclosed resources (Connection, Stream) — especially pre Java 7 try-with-resources. "
            "4. ThreadLocal not cleaned up in thread-pool threads. "
            "5. Non-static inner class holding reference to outer class. "
            "Symptom: heap grows monotonically, eventually OutOfMemoryError. "
            "Tools: heap dumps + MAT (Memory Analyzer Tool), Java VisualVM, JProfiler."
        ),
        "tip": "Most common production leak: a HashMap used as a cache with no eviction policy. Fix: use Guava/Caffeine cache with TTL and max size, or WeakHashMap for weak-reference keys.",
    },
    {
        "id": "prog_005",
        "topic": "Programming Fundamentals",
        "difficulty": "tricky",
        "q": (
            "What is the output of this JavaScript code?\n"
            "```javascript\n"
            "var funcs = [];\n"
            "for (var i = 0; i < 3; i++) {\n"
            "    funcs.push(function() { return i; });\n"
            "}\n"
            "console.log(funcs[0](), funcs[1](), funcs[2]());\n"
            "```"
        ),
        "options": {
            "A": "0 1 2",
            "B": "3 3 3",
            "C": "0 0 0",
            "D": "undefined undefined undefined",
        },
        "answer": "B",
        "explanation": (
            "B — Classic JavaScript closure-over-var trap. "
            "var is function-scoped: all three closures share THE SAME variable i. "
            "After the loop, i = 3. All functions return the current value of i = 3. "
            "Fix 1: use 'let' instead of 'var' — let is block-scoped, each iteration gets its own i. "
            "Fix 2: IIFE to capture i by value: funcs.push((function(j){ return function(){return j;} })(i)); "
            "Fix 3: funcs.push(function(j){return function(){return j;}}(i));"
        ),
        "tip": "One of the most famous JavaScript interview questions. The answer to 'why?' is that var creates a single binding per function scope, not per loop iteration. 'let' creates a new binding per iteration.",
    },
    {
        "id": "prog_006",
        "topic": "Programming Fundamentals",
        "difficulty": "medium",
        "q": "What is the difference between static typing, dynamic typing, and type inference?",
        "options": {
            "A": "Static = runtime type checks; Dynamic = compile-time type checks",
            "B": "Static: types checked at compile time (early error detection, verbose). Dynamic: types checked at runtime (flexible, runtime errors). Type inference: compiler deduces types (static, but concise).",
            "C": "Dynamic typing is always faster than static typing",
            "D": "Type inference is only in Python",
        },
        "answer": "B",
        "explanation": (
            "B — Static: Java, C, C++, Go, Rust. Compiler knows all types. Catches type errors before running. "
            "Dynamic: Python, JavaScript, Ruby. Types checked when code executes. Flexible but runtime TypeErrors. "
            "Type inference: Kotlin (val x = 5 → compiler infers Int), Swift, Rust, C++ auto. "
            "Static typing with less verbosity. "
            "Gradual typing: TypeScript adds optional static types to JavaScript. "
            "Note: Python has type hints (PEP 484) but they're not enforced at runtime."
        ),
        "tip": "Strong vs Weak typing is separate from Static vs Dynamic: Python is dynamically AND strongly typed (no implicit int+str coercion). JavaScript is dynamically AND weakly typed ('5'+1='51').",
    },
    {
        "id": "prog_007",
        "topic": "Programming Fundamentals",
        "difficulty": "interview",
        "q": "What is tail recursion and why is it important?",
        "options": {
            "A": "Recursion that never terminates",
            "B": "The recursive call is the LAST operation — no pending computation after it. Compilers can reuse the current stack frame (Tail Call Optimization), giving O(1) stack space instead of O(n).",
            "C": "Only applies to sorting algorithms",
            "D": "Always faster than iteration",
        },
        "answer": "B",
        "explanation": (
            "B — Regular recursion: each call pushes a new frame. Deep recursion → StackOverflow. "
            "Tail recursion: recursive call is the very last operation, no pending work. "
            "TCO: compiler replaces the call with a jump to function start, reusing the same frame → O(1) space. "
            "Languages with TCO: Scheme (mandated), Kotlin, Scala, Erlang, Haskell. "
            "Java does NOT perform TCO — use loops or trampolining for deep recursion. "
            "Converting to tail-recursive form: add an accumulator parameter."
        ),
        "tip": "Convert fib(n) to tail-recursive: fib(n, a=0, b=1) where base case returns a, recursive case calls fib(n-1, b, a+b).",
    },
    {
        "id": "prog_008",
        "topic": "Programming Fundamentals",
        "difficulty": "medium",
        "q": "What is the difference between Checked and Unchecked Exceptions in Java?",
        "options": {
            "A": "Checked exceptions crash programs; unchecked are handled automatically",
            "B": "Checked exceptions: compiler-enforced — must be caught or declared in 'throws'. Unchecked (RuntimeException subclasses): not compiler-enforced, represent programming bugs.",
            "C": "Unchecked exceptions are only in the standard library",
            "D": "They are identical — just naming conventions",
        },
        "answer": "B",
        "explanation": (
            "B — Checked: IOException, SQLException, ClassNotFoundException. "
            "Compiler forces you to handle or declare. Represent recoverable conditions. "
            "Unchecked: NullPointerException, ArrayIndexOutOfBoundsException, IllegalArgumentException. "
            "Represent programming errors. Not compiler-enforced. "
            "Debate: many frameworks (Spring) wrap checked in unchecked for cleaner API. "
            "Kotlin and C# have NO checked exceptions. "
            "Java trend: newer libraries (Streams, Optional) avoid checked exceptions."
        ),
        "tip": "",
    },

    # ─────────────────────────── SYSTEM DESIGN ────────────────────────────────

    {
        "id": "sys_003",
        "topic": "System Design",
        "difficulty": "interview",
        "q": "What is Consistent Hashing and why is it preferred over simple modulo hashing for distributed caches?",
        "options": {
            "A": "Consistent hashing is slower but uses less memory",
            "B": "Maps keys AND nodes to a ring. Adding/removing one node only remaps ~K/N keys on average (vs. almost ALL keys with modulo hashing when N changes).",
            "C": "Requires all servers to have equal capacity",
            "D": "Simple modulo is always preferred",
        },
        "answer": "B",
        "explanation": (
            "B — Modulo: server = hash(key) % N. Change N → almost every key remaps → cache stampede. "
            "Consistent hashing: both keys and servers hashed onto a ring (0 to 2^32). "
            "Each key served by the first server clockwise. "
            "Add server: only keys between it and its predecessor remap → K/N average remapping. "
            "Virtual nodes (vnodes): each physical server has multiple ring positions → better load balance. "
            "Used by: DynamoDB, Cassandra, Memcached (ketama), Akamai."
        ),
        "tip": "Without virtual nodes, if two servers are adjacent on the ring, one gets nearly all keys. ~100-150 vnodes per server is typical. Also enables heterogeneous server capacities.",
    },
    {
        "id": "sys_004",
        "topic": "System Design",
        "difficulty": "interview",
        "q": "What rate-limiting algorithms exist and what are their trade-offs?",
        "options": {
            "A": "Rate limiting can only use a database counter",
            "B": "Token Bucket (allows burst), Fixed Window Counter (simple, edge burst problem), Sliding Window Log (precise, memory-heavy), Leaky Bucket (smooth output), Sliding Window Counter (hybrid, recommended)",
            "C": "Rate limiting must be done client-side only",
            "D": "All algorithms are identical in practice",
        },
        "answer": "B",
        "explanation": (
            "B — Token Bucket: bucket refills at rate r, max capacity b. Allows burst up to b. Used by AWS. "
            "Fixed Window: count per window. Edge: 90 req last 10s of minute + 90 first 10s of next = 180 in 20s. "
            "Sliding Window Log: store all request timestamps. Precise but O(requests) memory. "
            "Sliding Window Counter: weighted blend of two fixed windows. Good trade-off. "
            "Implementation: Redis INCR + EXPIRE for distributed rate limiting. "
            "Leaky Bucket: requests enter a queue, processed at fixed rate — smooth output."
        ),
        "tip": "In interviews: clarify rate limit scope (per user? per IP? per API key?), where to store counters (Redis for distributed), and how to handle limit exceeded (429 Too Many Requests).",
    },
    {
        "id": "sys_005",
        "topic": "System Design",
        "difficulty": "interview",
        "q": "What is the Circuit Breaker pattern and what states does it transition between?",
        "options": {
            "A": "Circuit breaker disconnects database on high load",
            "B": "Monitors failures to a downstream service. States: CLOSED (normal), OPEN (fast-fail all calls), HALF-OPEN (test one request for recovery). Prevents cascade failures.",
            "C": "Only applies to network sockets",
            "D": "Retries failed requests indefinitely",
        },
        "answer": "B",
        "explanation": (
            "B — Problem: A calls B, B is slow/down, A's threads pile up → A runs out of threads → cascade. "
            "Circuit breaker (like an electrical circuit): "
            "CLOSED: track failures. Normal operation. "
            "OPEN (threshold exceeded): immediately return error/fallback, don't call B. Fast fail. "
            "HALF-OPEN (after timeout): allow one test request. Success → CLOSED. Fail → OPEN again. "
            "Libraries: Resilience4j (Java), Polly (.NET), Hystrix (deprecated). "
            "Combine with: retry, timeout, fallback, bulkhead."
        ),
        "tip": "Circuit breaker + retry + timeout form the resilience trio. Retry without circuit breaker can worsen things during recovery (thundering herd).",
    },
    {
        "id": "sys_006",
        "topic": "System Design",
        "difficulty": "medium",
        "q": "What is the key difference between monolith and microservices architecture?",
        "options": {
            "A": "Microservices are always better than monoliths",
            "B": "Monolith: single deployable unit, simple for small teams, ACID transactions easy. Microservices: independent services per domain, team autonomy, independent scaling — but adds network, observability, and distributed systems complexity.",
            "C": "Monoliths cannot be scaled",
            "D": "Microservices require different programming languages per service",
        },
        "answer": "B",
        "explanation": (
            "B — Monolith strengths: simple deployment, easy debugging, in-process calls, "
            "straightforward ACID transactions, lower operational overhead. "
            "Microservices strengths: independent deployment, scaling, team ownership, tech diversity. "
            "Microservices costs: distributed system complexity, network failures, distributed tracing, "
            "eventual consistency, service discovery, much higher DevOps overhead. "
            "Advice (Martin Fowler): 'Don't start with microservices. Start with a modular monolith, "
            "find seams, extract services when scaling demands it.'"
        ),
        "tip": "Segment.com (analytics company) famously migrated from microservices BACK to a monolith due to operational complexity. Premature microservices is a real anti-pattern.",
    },
    {
        "id": "sys_007",
        "topic": "System Design",
        "difficulty": "interview",
        "q": "How would you design a URL shortener like bit.ly? What are the key design decisions?",
        "options": {
            "A": "Store in a text file with random 6-character strings",
            "B": "Short code generation (base62 of auto-increment ID or hash prefix), high-read/write throughput with Redis cache + DB, 301 vs 302 redirect strategy, analytics tracking",
            "C": "Simple array to store mappings",
            "D": "MD5 has no collisions so no collision handling needed",
        },
        "answer": "B",
        "explanation": (
            "B — POST /shorten → generate short code → store {code: long_url} in DB → return short URL. "
            "GET /abc123 → Redis cache (hot URLs, ~1ms) → DB fallback → HTTP redirect. "
            "Code generation: "
            "base62(auto-increment_id) — 62^6 ≈ 56B unique codes, no collision. "
            "MD5(url) prefix — may collide, needs collision handling. "
            "301 (Permanent): browser caches, bypasses your server later → lose analytics. "
            "302 (Temporary): browser always checks your server → analytics captured. "
            "Scale: Redis cache for hot URLs, CDN for global latency, DB read replicas."
        ),
        "tip": "301 vs 302 is a classic interview detail. Choose 302 for URL shorteners that need click analytics. 301 is better for pure performance with no analytics requirement.",
    },
    {
        "id": "sys_008",
        "topic": "System Design",
        "difficulty": "interview",
        "q": "What is eventual consistency and how does it differ from strong consistency?",
        "options": {
            "A": "Eventual consistency means data is never consistent",
            "B": "Strong consistency: every read sees the latest write. Eventual: writes propagate over time — reads may return stale data temporarily but all replicas converge. Enables higher availability and lower latency.",
            "C": "They are identical — 'eventual' just means 1ms delay",
            "D": "Eventual consistency only applies to file systems",
        },
        "answer": "B",
        "explanation": (
            "B — Strong consistency (linearizability): all reads reflect the latest committed write. "
            "Requires coordination across replicas → higher latency, lower availability during partitions. "
            "Eventual consistency: no coordination required. Replicas may diverge temporarily. "
            "Given no new writes, all nodes eventually converge. "
            "Examples: DNS propagation (minutes), Amazon S3 (now strongly consistent), "
            "social media like counts, Cassandra default. "
            "Real-world: after tweeting, refreshing might briefly show 0 likes even after receiving some."
        ),
        "tip": "For user-facing features (view counts, likes), eventual consistency is acceptable and enables massive scale. For bank transfers, inventory (prevent overselling), strong consistency is critical.",
    },

    # ──────────────────────── SOFTWARE ENGINEERING ────────────────────────────

    {
        "id": "se_003",
        "topic": "Software Engineering",
        "difficulty": "medium",
        "q": "What is Test-Driven Development (TDD) and what is the Red-Green-Refactor cycle?",
        "options": {
            "A": "TDD means writing tests after code to verify it works",
            "B": "TDD: write a failing test (Red) → write minimal code to pass it (Green) → improve code without breaking tests (Refactor). Drives design and ensures testability from the start.",
            "C": "TDD is only for unit tests",
            "D": "TDD always doubles development time with no benefit",
        },
        "answer": "B",
        "explanation": (
            "B — Red: write a test for non-existent feature. It must fail (proves it tests something real). "
            "Green: write the simplest code to make the test pass. Don't over-engineer. "
            "Refactor: improve code and tests. Remove duplication. Tests must still pass. "
            "Benefits: tests are always runnable, design emerges from usage, "
            "safe refactoring. "
            "Studies: TDD reduces defect density 40-80% at cost of 15-35% more initial development time."
        ),
        "tip": "If a class is hard to test, it's a design signal — too many dependencies, too much responsibility. TDD enforces good design through the discipline of writing tests first.",
    },
    {
        "id": "se_004",
        "topic": "Software Engineering",
        "difficulty": "medium",
        "q": "What is technical debt and when is it acceptable?",
        "options": {
            "A": "Technical debt is money owed to software vendors",
            "B": "The implied cost of rework from choosing a quick solution now over a better one — acceptable for MVPs, tight deadlines, or validating ideas before investing fully. Must be tracked and paid down.",
            "C": "Technical debt should never be taken on",
            "D": "Technical debt only refers to outdated languages",
        },
        "answer": "B",
        "explanation": (
            "B — Ward Cunningham's metaphor: like financial debt, some is OK (mortgage), "
            "but it accrues interest (slower development, more bugs). "
            "Acceptable: MVP to validate idea, tight deadline with a clear remediation ticket, research spikes. "
            "Unacceptable: cumulative neglect making the codebase unmaintainable. "
            "Two types: deliberate (conscious trade-off) vs inadvertent (not knowing the better approach). "
            "Key rule: track it. Write the ticket. 'Temporary' becomes permanent without discipline."
        ),
        "tip": "",
    },
    {
        "id": "se_005",
        "topic": "Software Engineering",
        "difficulty": "easy",
        "q": "What does Semantic Versioning (SemVer) 2.7.3 mean?",
        "options": {
            "A": "Year.Month.Day of release",
            "B": "MAJOR.MINOR.PATCH: 2 = breaking changes; 7 = new backward-compatible features since v2.0.0; 3 = backward-compatible bug fixes since v2.7.0",
            "C": "All three numbers are arbitrary",
            "D": "Third number = number of files changed",
        },
        "answer": "B",
        "explanation": (
            "B — MAJOR: breaking API changes (callers may need code changes). "
            "MINOR: new features, backward compatible. "
            "PATCH: bug fixes, backward compatible. "
            "Pre-release: 1.0.0-alpha, 1.0.0-beta, 1.0.0-rc.1. "
            "0.x.y: unstable, API may change freely. "
            "Used by: npm, Maven, pip, Cargo, GitHub Releases. "
            "npm caret (^1.2.3): allows minor+patch updates but not major."
        ),
        "tip": "Breaking changes MUST bump the major version. If a library goes from 1.x to 2.0, expect to update your code. This is why npm caret (^) protects you from breaking changes.",
    },
    {
        "id": "se_006",
        "topic": "Software Engineering",
        "difficulty": "medium",
        "q": "What is the difference between DRY, KISS, and YAGNI principles?",
        "options": {
            "A": "They all mean: write short code",
            "B": "DRY: eliminate duplication (one canonical source of truth). KISS: prefer simple solutions. YAGNI: don't build features until actually needed (from XP).",
            "C": "YAGNI means test everything; DRY means use functional programming",
            "D": "These principles only apply to databases",
        },
        "answer": "B",
        "explanation": (
            "B — DRY (Don't Repeat Yourself): every piece of knowledge has one unambiguous representation. "
            "Copy-paste = DRY violation. Change in one place must propagate to all copies. "
            "KISS (Keep It Simple, Stupid): simplest solution that works. "
            "Avoid premature optimization, over-engineering, gold plating. "
            "YAGNI (You Aren't Gonna Need It): don't add generalization 'just in case'. "
            "Build for today's requirement. Future requirement may never come or be different."
        ),
        "tip": "DRY violation is obvious (copy-pasted code). YAGNI violation is subtle — 'what if we need this later?' is the danger phrase. Balance: don't be so YAGNI that you paint yourself into a corner.",
    },

    # ─────────────────────── COMPUTER ARCHITECTURE ────────────────────────────

    {
        "id": "arch_002",
        "topic": "Computer Architecture",
        "difficulty": "interview",
        "q": "What are the three types of CPU pipeline hazards?",
        "options": {
            "A": "A pipeline hazard is when two programs run on one core simultaneously",
            "B": "Structural (resource conflict), Data (instruction B needs result of unfinished instruction A), Control (branch — unknown next instruction until branch resolves)",
            "C": "Pipeline hazards only occur in GPUs",
            "D": "There is only one type: data hazard",
        },
        "answer": "B",
        "explanation": (
            "B — CPU pipelines overlap multiple instructions across stages (Fetch → Decode → Execute → Memory → Writeback). "
            "Structural: two instructions need the same resource simultaneously. "
            "Data: instruction B depends on result of A still in-flight. "
            "Solutions: stalling (NOP bubbles), data forwarding (bypass unit sends result early). "
            "Control (branch): fetched instructions after a branch may be wrong. "
            "Solutions: branch prediction (predict taken/not-taken), speculative execution. "
            "Misprediction penalty: flush pipeline, lose 15-20 cycles on modern CPUs."
        ),
        "tip": "Spectre/Meltdown (2018) exploited speculative execution — CPU executed instructions speculatively, leaving side-channel traces in cache even after rollback.",
    },
    {
        "id": "arch_003",
        "topic": "Computer Architecture",
        "difficulty": "medium",
        "q": "What is endianness and when does it matter in practice?",
        "options": {
            "A": "Endianness is character encoding in memory",
            "B": "Byte order of multi-byte values in memory. Big-endian: MSB at lowest address. Little-endian: LSB at lowest address. Matters for: network protocols (always big-endian/network byte order), binary file exchange between systems.",
            "C": "Only matters for floating-point numbers",
            "D": "All modern systems use the same endianness",
        },
        "answer": "B",
        "explanation": (
            "B — 32-bit value 0x12345678: "
            "Big-endian: [12][34][56][78] — most significant byte first. Used by: network protocols, SPARC, Motorola. "
            "Little-endian: [78][56][34][12] — least significant byte first. Used by: x86, ARM (usually LE mode). "
            "Practical impact: "
            "Network byte order is big-endian → use htons()/htonl() in C to convert. "
            "Reading binary file from a different endian system requires byte-swapping. "
            "Java: big-endian JVM internally. Python struct module: '>' for big-endian, '<' for little-endian."
        ),
        "tip": "Named from Gulliver's Travels (which end to crack an egg). Most data exchange formats (JSON, HTTP) avoid the issue by using text. Binary formats must specify endianness explicitly.",
    },
    {
        "id": "arch_004",
        "topic": "Computer Architecture",
        "difficulty": "medium",
        "q": "What is the fundamental difference between RISC and CISC instruction set architectures?",
        "options": {
            "A": "RISC has more complex instructions than CISC",
            "B": "RISC: small set of simple fixed-length instructions (easy pipeline, compiler does more). CISC: large set of complex variable-length instructions (fewer instructions per program, complex hardware). Modern CPUs blur the line.",
            "C": "CISC is always faster",
            "D": "RISC is only for mobile; CISC only for desktops",
        },
        "answer": "B",
        "explanation": (
            "B — RISC (ARM, MIPS, RISC-V): simple operations, fixed-length (4 bytes), "
            "typically one clock cycle per instruction. Easy pipelining. Compiler generates more instructions. "
            "ARM dominates mobile (every smartphone), embedded, Apple Silicon M-series. "
            "CISC (x86/x64): variable-length instructions (1-15 bytes), complex operations, harder pipelining. "
            "Irony: modern x86 CPUs internally decode CISC instructions to RISC-like micro-ops. "
            "Apple M-series beating x86 in performance-per-watt demonstrates RISC advantages for power-constrained workloads."
        ),
        "tip": "",
    },
    {
        "id": "arch_005",
        "topic": "Computer Architecture",
        "difficulty": "medium",
        "q": "How does a CPU cache work and what are the types of cache misses?",
        "options": {
            "A": "CPU cache is RAM installed separately from the motherboard",
            "B": "Fast SRAM near CPU stores recently used data. On access: L1→L2→L3→RAM. Miss types: Cold (first access), Capacity (working set too large), Conflict (multiple data map to same cache set).",
            "C": "Cache misses are handled by the OS",
            "D": "Modern CPUs have only one cache level",
        },
        "answer": "B",
        "explanation": (
            "B — Memory hierarchy: L1 (~1ns, 32-64KB per core) → L2 (~5ns, 256KB-1MB) → "
            "L3 (~20-40ns, 4-64MB shared) → RAM (~100ns) → SSD (~100µs). "
            "Cache lines: 64-byte chunks. Accessing one element pre-fetches adjacent elements. "
            "Cold miss: first access, unavoidable. "
            "Capacity miss: working set larger than cache. "
            "Conflict miss: cache associativity limits. "
            "Cache-friendly code: iterate arrays sequentially (spatial locality), "
            "reuse data while it's hot in cache (temporal locality)."
        ),
        "tip": "Column-wise iteration of a 2D array (C/Java row-major layout) causes a cache miss on every step. Row-wise iteration is dramatically faster. This is why matrix multiplication order matters.",
    },

    # ───────────────────────── WEB FUNDAMENTALS ───────────────────────────────

    {
        "id": "web_003",
        "topic": "Web Fundamentals",
        "difficulty": "interview",
        "q": "What is the difference between JWT (JSON Web Token) and session-based authentication?",
        "options": {
            "A": "JWT is more secure because it is always encrypted",
            "B": "Sessions: server stores state (DB/Redis lookup per request, hard to scale). JWT: self-contained stateless token (server verifies signature without DB, scales horizontally). JWT tradeoff: hard to invalidate before expiry.",
            "C": "Session-based auth is only for mobile apps",
            "D": "JWT cannot expire",
        },
        "answer": "B",
        "explanation": (
            "B — Session: server creates session record in DB/Redis on login, sends session_id cookie. "
            "Per request: DB/Redis lookup to validate → sticky sessions or centralized store needed. "
            "JWT: server signs header.payload.signature with secret. Client stores token. "
            "Per request: verify signature locally → no DB call → stateless, scales horizontally. "
            "JWT downside: cannot invalidate individual tokens before expiry (logout problem). "
            "Mitigations: short expiry (15min) + refresh tokens, or token blacklist (reintroduces state). "
            "Note: JWT is signed (integrity), not encrypted — payload is base64, readable by anyone."
        ),
        "tip": "JWT storage: httpOnly cookie (CSRF risk, XSS-safe) vs localStorage (XSS risk, no CSRF). httpOnly cookie + SameSite=Strict is generally recommended.",
    },
    {
        "id": "web_004",
        "topic": "Web Fundamentals",
        "difficulty": "medium",
        "q": "What is OAuth 2.0 and how does it differ from OpenID Connect (OIDC)?",
        "options": {
            "A": "OAuth is for authentication; OIDC is for authorization",
            "B": "OAuth 2.0: authorization framework (grant access to resources). OIDC: authentication layer ON TOP of OAuth 2.0 — adds ID token (JWT with user identity), enabling 'Login with Google/Facebook'.",
            "C": "They are competing standards",
            "D": "Both are deprecated",
        },
        "answer": "B",
        "explanation": (
            "B — OAuth 2.0: 'Allow this app to read your Google Drive on your behalf.' "
            "Issues access tokens for resource access. NOT designed for authentication. "
            "OIDC: adds identity layer. 'Who is this user?' "
            "Adds: ID token (JWT with name, email, user_id), UserInfo endpoint, standard scopes (openid, profile). "
            "'Login with Google' uses OIDC — Google authenticates the user, issues an ID token. "
            "Anti-pattern: using an OAuth access token as authentication is the 'OAuth for authentication' mistake."
        ),
        "tip": "Memory aid: OAuth = Authorization (car key to let someone borrow your car). OIDC = Authentication + Authorization (passport + car key). OIDC tells you WHO, OAuth tells you WHAT they can access.",
    },
    {
        "id": "web_005",
        "topic": "Web Fundamentals",
        "difficulty": "medium",
        "q": "What is the Critical Rendering Path and why does it matter for web performance?",
        "options": {
            "A": "Order of network requests",
            "B": "HTML→DOM, CSS→CSSOM, both→Render Tree, Layout, Paint. CSS is render-blocking; synchronous JS is parser-blocking. Optimizing CRP reduces First/Largest Contentful Paint (Core Web Vitals).",
            "C": "Only applies to server-side rendered pages",
            "D": "A network protocol for faster image loading",
        },
        "answer": "B",
        "explanation": (
            "B — Steps: parse HTML → DOM. Parse CSS → CSSOM (render-blocking — browser must finish CSS before rendering). "
            "Execute JS (parser-blocking by default if in <head>). DOM + CSSOM → Render Tree. Layout. Paint. "
            "Optimizations: async/defer on scripts, inline critical CSS, lazy-load images below the fold. "
            "async: downloads JS without blocking, executes when ready (may interrupt parsing). "
            "defer: downloads without blocking, executes after HTML fully parsed. "
            "Core Web Vitals: FCP, LCP measure CRP efficiency."
        ),
        "tip": "CSS is ALWAYS render-blocking. You cannot make it async. Solution: inline critical CSS (above-the-fold styles), load remaining CSS asynchronously via JS.",
    },
    {
        "id": "web_006",
        "topic": "Web Fundamentals",
        "difficulty": "medium",
        "q": "What is the difference between localStorage, sessionStorage, and cookies?",
        "options": {
            "A": "They are identical",
            "B": "localStorage: persistent ~5MB, JS-only access. sessionStorage: cleared on tab close, ~5MB. Cookies: sent with every HTTP request (server reads them), ~4KB, can be httpOnly/Secure/SameSite/expiry.",
            "C": "Cookies cannot store strings",
            "D": "localStorage is sent to the server on every request",
        },
        "answer": "B",
        "explanation": (
            "B — localStorage: survives browser restart. Same-origin only. JS access only. Good for: app settings, cached data. "
            "sessionStorage: cleared when tab/window closes. Per-tab isolation. Good for: per-session form state. "
            "Cookies: automatically sent in HTTP headers. Server can set and read. "
            "Security flags: httpOnly (JS cannot read → XSS-safe), Secure (HTTPS only), "
            "SameSite=Strict (CSRF protection), Max-Age (expiry). "
            "Auth tokens typically stored in httpOnly cookies."
        ),
        "tip": "For auth: httpOnly cookie is safer against XSS (JS can't steal it) but needs CSRF protection. localStorage is easier but vulnerable to XSS. Choose based on threat model.",
    },
    {
        "id": "web_007",
        "topic": "Web Fundamentals",
        "difficulty": "interview",
        "q": "What problems does GraphQL solve that REST does not?",
        "options": {
            "A": "GraphQL is a database query language",
            "B": "Solves over-fetching (REST returns fixed data regardless of what client needs) and under-fetching (needing N REST round-trips for related data). Client specifies exactly what fields it needs.",
            "C": "GraphQL is always faster than REST",
            "D": "GraphQL only works with JavaScript",
        },
        "answer": "B",
        "explanation": (
            "B — Over-fetching: GET /users returns 50 fields, UI needs only name+email. Wasted bandwidth. "
            "Under-fetching: GET /user → GET /posts → GET /comments. Three round-trips. "
            "GraphQL: one POST /graphql with a query specifying exact fields and nested data. One round-trip. "
            "Strongly typed schema: auto-documentation, IDE completion, validation. "
            "GraphQL drawbacks: N+1 problem on server (use DataLoader to batch DB calls), "
            "caching harder (POST requests), higher server complexity. "
            "Used by: GitHub, Facebook, Shopify, Twitter."
        ),
        "tip": "GraphQL's N+1: resolving 100 users' posts without DataLoader issues 100 separate DB queries. DataLoader batches them into one query in a single event loop tick.",
    },
    {
        "id": "web_008",
        "topic": "Web Fundamentals",
        "difficulty": "medium",
        "q": "What do the Cache-Control headers 'no-cache' vs 'no-store' mean?",
        "options": {
            "A": "no-cache and no-store are identical — both prevent all caching",
            "B": "no-store: never cache anywhere (sensitive data). no-cache: may cache, but MUST revalidate with server before using cached copy (sends conditional request with ETag/Last-Modified).",
            "C": "no-cache means cache for 0 seconds",
            "D": "Cache-Control only applies to images",
        },
        "answer": "B",
        "explanation": (
            "B — no-store: do not save the response anywhere — not in browser, CDN, or proxy. "
            "For truly sensitive data (bank statements, medical records). "
            "no-cache (misleading name): cached but must always revalidate with server. "
            "Server responds 304 Not Modified (fast, no body) or 200 with new content. "
            "ETag: hash of content. Client sends If-None-Match: <etag>. "
            "Best practice: content-hashed filenames (bundle.abc.js) + max-age=31536000,immutable. "
            "HTML: no-cache (always get latest asset file URLs)."
        ),
        "tip": "no-cache does NOT mean 'don't cache'. It means 'cache, but always check freshness'. This naming has confused developers for decades. Think of it as 'always-revalidate'.",
    },
]
