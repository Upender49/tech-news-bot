"""
question_bank_advanced.py — Additional high-standard, interview-level CS Fundamentals questions.
Focuses on advanced DSA, OS internals, DBMS architecture, Network protocols, System Design, and Concurrency.
"""

ADVANCED_QUESTIONS: list[dict] = [

    # ─────────────────────── ADVANCED DSA / CODING ────────────────────────────

    {
        "id": "dsa_adv_001",
        "topic": "Algorithms",
        "difficulty": "hard",
        "q": "What is the time complexity to find the Next Greater Element for every element in an array of size n using a Monotonic Stack?",
        "options": {
            "A": "O(n²)",
            "B": "O(n log n)",
            "C": "O(n) time and O(n) space",
            "D": "O(1) auxiliary space",
        },
        "answer": "C",
        "explanation": (
            "C — Using a monotonic decreasing stack, each array element is pushed onto the stack at most once "
            "and popped at most once. Therefore, the inner while loop executes at most n times in total across the entire algorithm. "
            "This gives an amortized O(n) runtime and O(n) auxiliary space for the stack."
        ),
        "tip": "Monotonic Stack is the standard technique for Next/Previous Greater/Smaller Element, Daily Temperatures, and Largest Rectangle in Histogram.",
    },
    {
        "id": "dsa_adv_002",
        "topic": "Data Structures",
        "difficulty": "hard",
        "q": "Which data structure allows both point updates and range sum queries on an array in O(log n) time with O(n) space?",
        "options": {
            "A": "Prefix Sum Array",
            "B": "Binary Indexed Tree (Fenwick Tree) or Segment Tree",
            "C": "Binary Search Tree without balancing",
            "D": "Skip List",
        },
        "answer": "B",
        "explanation": (
            "B — A Binary Indexed Tree (Fenwick Tree) and Segment Tree both support point update in O(log n) and range query in O(log n). "
            "A prefix sum array answers range queries in O(1) but updates take O(n). A regular array updates in O(1) but queries take O(n)."
        ),
        "tip": "Fenwick tree uses `i += i & (-i)` for updates and `i -= i & (-i)` for prefix queries. It is shorter to implement than a Segment Tree.",
    },
    {
        "id": "dsa_adv_003",
        "topic": "Algorithms",
        "difficulty": "tricky",
        "q": (
            "Consider finding the Longest Increasing Subsequence (LIS) of an array of length n. "
            "What are the time complexities of the standard Dynamic Programming approach vs the Patience Sorting (Binary Search) approach?"
        ),
        "options": {
            "A": "DP is O(n), Binary Search is O(log n)",
            "B": "DP is O(n²), Patience Sorting / Binary Search is O(n log n)",
            "C": "Both are O(n²)",
            "D": "DP is O(2ⁿ), Binary Search is O(n)",
        },
        "answer": "B",
        "explanation": (
            "B — Standard DP maintains `dp[i]` as the LIS ending at index i, checking all previous j < i, which takes O(n²). "
            "The patience sorting approach maintains an array `tails` where `tails[len]` is the smallest tail of all increasing subsequences of length len+1. "
            "Using `bisect_left` (binary search) to place each number yields O(n log n) total time."
        ),
        "tip": "In interviews, starting with O(n²) DP and optimizing to O(n log n) using patience sorting / tails array shows deep algorithmic mastery.",
    },
    {
        "id": "dsa_adv_004",
        "topic": "Algorithms",
        "difficulty": "hard",
        "q": "What is Tarjan's algorithm used for in graph theory, and what is its time complexity?",
        "options": {
            "A": "Minimum Spanning Tree in O(E log V)",
            "B": "Finding Strongly Connected Components (SCCs) and Bridges/Articulation Points in a directed/undirected graph in O(V + E) using DFS with discovery and low-link values",
            "C": "All-Pairs Shortest Path in O(V³)",
            "D": "Maximum Bipartite Matching in O(V * E)",
        },
        "answer": "B",
        "explanation": (
            "B — Tarjan's algorithm uses a single Depth First Search (DFS) traversal to find Strongly Connected Components (SCCs) in a directed graph "
            "or articulation points/bridges in an undirected graph in O(V + E) time. It tracks discovery time `disc[u]` and the lowest reachable ancestor `low[u]`."
        ),
        "tip": "Tarjan's algorithm is preferred over Kosaraju's algorithm because Kosaraju requires two full DFS passes and a graph transpose, whereas Tarjan requires only one pass.",
    },
    {
        "id": "dsa_adv_005",
        "topic": "Algorithms",
        "difficulty": "interview",
        "q": "What is the time complexity of the KMP (Knuth-Morris-Pratt) pattern matching algorithm for text of length N and pattern of length M?",
        "options": {
            "A": "O(N * M)",
            "B": "O(N + M)",
            "C": "O(N log M)",
            "D": "O(M log N)",
        },
        "answer": "B",
        "explanation": (
            "B — KMP preprocesses the pattern into a Longest Prefix Suffix (LPS / Pi) array in O(M) time and space. "
            "The search phase then traverses the text of length N without ever backtracking the text pointer, taking O(N) comparisons. "
            "Total time complexity is strictly O(N + M)."
        ),
        "tip": "The LPS array `lps[i]` stores the length of the longest proper prefix of `pattern[0...i]` that is also a suffix of `pattern[0...i]`.",
    },

    # ─────────────────────── ADVANCED OPERATING SYSTEMS ───────────────────────

    {
        "id": "os_adv_001",
        "topic": "Operating Systems",
        "difficulty": "hard",
        "q": "What is the purpose of the Translation Lookaside Buffer (TLB) and what happens on a TLB Shootdown in a multi-core system?",
        "options": {
            "A": "The TLB is a disk buffer; shootdown writes dirty buffers to SSD",
            "B": "The TLB is an on-chip hardware cache for virtual-to-physical address translations. When a page table entry is modified on one core, an inter-processor interrupt (IPI) forces all other cores sharing that address space to invalidate their cached TLB entries.",
            "C": "The TLB is used only for kernel stack pointers",
            "D": "TLB Shootdown happens only when the system runs out of physical RAM",
        },
        "answer": "B",
        "explanation": (
            "B — The TLB caches recent Virtual-to-Physical page translations to avoid 4-5 memory lookups per access (in 4-level/5-level page tables). "
            "When page permissions or mappings change (e.g. `mprotect`, `munmap`, page migration), the OS must ensure other cores do not use stale translations. "
            "It sends Inter-Processor Interrupts (IPIs) to invalidate that TLB entry on all other active CPU cores (TLB Shootdown), which can be an expensive scalability bottleneck."
        ),
        "tip": "TLB shootdown overhead is a major reason why high-performance systems use huge pages (2MB/1GB) — fewer page table entries means fewer TLB misses and less shootdown traffic.",
    },
    {
        "id": "os_adv_002",
        "topic": "Operating Systems",
        "difficulty": "interview",
        "q": "What is Copy-on-Write (COW) during a `fork()` system call in Unix/Linux?",
        "options": {
            "A": "The child process immediately copies the entire RAM of the parent process before executing",
            "B": "Parent and child initially share the same physical memory pages marked as read-only. A private copy of a page is duplicated only when either process attempts to modify (write to) that specific page.",
            "C": "COW writes all memory changes directly to the swap partition",
            "D": "COW is a file system journaling feature unrelated to processes",
        },
        "answer": "B",
        "explanation": (
            "B — Copy-on-Write makes `fork()` fast and memory-efficient. Instead of copying gigabytes of memory immediately, the OS copies only page tables "
            "and marks physical pages read-only for both processes. When either writes to a page, a page-fault trap triggers the kernel to duplicate that single page and mark it writable."
        ),
        "tip": "This is why `fork()` followed immediately by `exec()` is fast — `exec()` replaces the address space without triggering copies of the old pages.",
    },
    {
        "id": "os_adv_003",
        "topic": "Operating Systems",
        "difficulty": "interview",
        "q": "Why is Linux `epoll` more scalable than `select` or `poll` for handling 100,000+ concurrent network connections (C10K problem)?",
        "options": {
            "A": "epoll runs entirely inside user space without system calls",
            "B": "select/poll pass the full list of file descriptors on every call (O(N) scan in kernel and userspace). epoll registers FDs once via epoll_ctl in an in-kernel red-black tree, and epoll_wait returns only the ready FDs in O(1) / O(ready) time via a ready list.",
            "C": "select is limited to 10 connections only",
            "D": "epoll creates a new OS thread for every socket connection",
        },
        "answer": "B",
        "explanation": (
            "B — With `select()` / `poll()`, the application must construct an array/bitmask of all N descriptors and pass it to the kernel on every loop iteration, requiring O(N) scanning. "
            "`epoll` registers sockets once (`epoll_ctl`). The kernel uses socket callback interrupts to add ready descriptors to an internal ready-list (doubly linked list), and `epoll_wait` returns only ready descriptors in O(ready) time."
        ),
        "tip": "Modern web servers (Nginx, Node.js libuv, Netty, Redis, Go runtime) all rely on epoll (Linux), kqueue (BSD/macOS), or IOCP (Windows) for event-driven I/O.",
    },
    {
        "id": "os_adv_004",
        "topic": "Operating Systems",
        "difficulty": "tricky",
        "q": "What is the difference between a Spinlock and a Mutex, and when is a Spinlock appropriate?",
        "options": {
            "A": "Spinlocks are always faster and should replace all mutexes",
            "B": "A Spinlock busy-waits (loops consuming CPU) until the lock is freed; a Mutex puts the waiting thread to sleep (context switch). Spinlocks are suitable only in kernel/low-level code for very short critical sections where context switch overhead exceeds wait time and the thread cannot sleep (e.g. interrupt handlers).",
            "C": "Spinlocks can only be used on single-core processors",
            "D": "Mutexes can only be used in kernel mode",
        },
        "answer": "B",
        "explanation": (
            "B — When a thread tries to acquire a locked Mutex, the OS puts the thread to sleep and context switches to another thread (~1-10 microseconds cost). "
            "A Spinlock keeps spinning in a CPU loop checking an atomic variable. If the lock is held for just a few nanoseconds, spinlock avoids the context switch penalty. "
            "However, if held longer, spinlock wastes CPU cycles. Spinlocks must NEVER be used on single-core systems (as the holder cannot run while the waiter spins) or for long operations."
        ),
        "tip": "In user space, hybrid mutexes (like glibc's pthread_mutex) adaptively spin for a few cycles before falling back to sleeping via futex.",
    },

    # ─────────────────────── ADVANCED DATABASES ───────────────────────────────

    {
        "id": "db_adv_001",
        "topic": "Databases",
        "difficulty": "hard",
        "q": "Why do relational database indexes use B+ Trees instead of standard B-Trees or Binary Search Trees for disk-based storage?",
        "options": {
            "A": "B+ Trees have fewer nodes and use less disk space",
            "B": "B+ Trees store all actual data records/pointers exclusively in leaf nodes and link all leaf nodes in a doubly-linked list. Internal nodes only store routing keys, maximizing fan-out (reducing tree height/disk I/O) and enabling fast range scans.",
            "C": "B-Trees do not support logarithmic search time",
            "D": "Binary Search Trees have higher fan-out than B+ Trees",
        },
        "answer": "B",
        "explanation": (
            "B — In a B+ Tree: "
            "(1) Internal nodes hold ONLY search keys and child pointers, so a single 4KB/16KB disk page can hold hundreds of keys (high fan-out, shallow height ~3-4 levels for billions of rows). "
            "(2) Leaf nodes contain all actual data/pointers and are linked sequentially, allowing range queries (e.g., `WHERE age BETWEEN 20 AND 30`) to find the start key in O(log n) and simply traverse leaf pointers horizontally without going up and down the tree."
        ),
        "tip": "Standard B-Trees store data pointers in internal nodes, which reduces the number of keys per page, increases tree height, and makes range scans require complex in-order tree traversals.",
    },
    {
        "id": "db_adv_002",
        "topic": "Databases",
        "difficulty": "hard",
        "q": "What is Write-Ahead Logging (WAL) and why is it essential for database ACID durability and crash recovery?",
        "options": {
            "A": "WAL writes audit logs to disk after user transactions are completed",
            "B": "WAL requires that any change (redo/undo log record) must be appended sequentially to stable disk storage BEFORE the corresponding dirty data pages are flushed to table files. This enables fast sequential writes and crash recovery via ARIES protocol.",
            "C": "WAL prevents SQL injection attacks",
            "D": "WAL is only used for read-only database replicas",
        },
        "answer": "B",
        "explanation": (
            "B — Flushing random 16KB data pages to disk on every transaction commit is too slow (random I/O). "
            "Instead, the database appends a compact log record sequentially to the WAL file (fast sequential I/O) and flushes the log with `fsync`. "
            "Once the log is safely on disk, the transaction is committed. If a crash occurs before dirty data pages reach disk, the DB replays the WAL on reboot (Redo) to recover committed data and rolls back uncommitted ones (Undo)."
        ),
        "tip": "PostgreSQL, MySQL InnoDB (redo log), SQLite, and distributed DBs like CockroachDB all use WAL for durability and replication.",
    },
    {
        "id": "db_adv_003",
        "topic": "Databases",
        "difficulty": "interview",
        "q": "What is Write Skew anomaly and at which database isolation level can it occur?",
        "options": {
            "A": "Write Skew occurs only in Read Uncommitted",
            "B": "Write Skew occurs under Snapshot Isolation / Repeatable Read: two concurrent transactions read overlapping state, satisfy constraints based on what they read, and make disjoint updates that together violate a global constraint. Only Serializable isolation prevents it.",
            "C": "Write Skew occurs when two transactions update the exact same row simultaneously",
            "D": "Write Skew is a hardware disk write failure",
        },
        "answer": "B",
        "explanation": (
            "B — Classic example: 'At least one doctor must be on call.' "
            "Doctor A and Doctor B are both on call. A checks if another doctor is on call (sees B is on call) and goes off call. "
            "Concurrently, B checks (sees A is on call) and goes off call. "
            "Under Snapshot Isolation / Repeatable Read, both transactions commit because they modified different rows, but now ZERO doctors are on call! "
            "Only `SERIALIZABLE` isolation or explicit locking (`SELECT FOR UPDATE`) prevents Write Skew."
        ),
        "tip": "Write Skew is a favorite senior/architect interview question to test if a candidate understands the subtle differences between Repeatable Read and true Serializable isolation.",
    },
    {
        "id": "db_adv_004",
        "topic": "Databases",
        "difficulty": "interview",
        "q": "What is the difference between Two-Phase Locking (2PL) and Two-Phase Commit (2PC)?",
        "options": {
            "A": "They are the same protocol with two different names",
            "B": "2PL is a concurrency control mechanism on a single database (growing phase acquires locks, shrinking phase releases locks) guaranteeing serializability. 2PC is a distributed consensus/atomic commitment protocol (prepare phase, commit phase) ensuring atomic commits across multiple nodes.",
            "C": "2PL is for NoSQL and 2PC is for SQL",
            "D": "2PC acquires locks and 2PL commits transactions",
        },
        "answer": "B",
        "explanation": (
            "B — Two-Phase Locking (2PL) prevents concurrency conflicts within a database engine: once a transaction releases any lock (shrinking phase), it cannot acquire any new locks. "
            "Two-Phase Commit (2PC) is a distributed transaction protocol involving a coordinator and participants: "
            "Phase 1 (Prepare): Coordinator asks all nodes 'can you commit?'. Nodes write to log and reply YES/NO. "
            "Phase 2 (Commit): If all voted YES, coordinator writes COMMIT and tells all nodes to commit; otherwise ABORT."
        ),
        "tip": "A classic interview trap! 2PL = Concurrency control (Isolation). 2PC = Distributed transaction atomicity (Atomicity across nodes).",
    },

    # ─────────────────────── ADVANCED COMPUTER NETWORKS ───────────────────────

    {
        "id": "net_adv_001",
        "topic": "Computer Networks",
        "difficulty": "hard",
        "q": "How does TCP Congestion Control adapt its Congestion Window (cwnd) across its four phases: Slow Start, Congestion Avoidance, Fast Retransmit, and Fast Recovery?",
        "options": {
            "A": "cwnd increases by a fixed 1MB per second regardless of ACKs",
            "B": "Slow Start: cwnd doubles every RTT (exponential growth) until ssthresh. Congestion Avoidance: cwnd increases by 1 MSS per RTT (linear additive increase). Fast Retransmit: 3 duplicate ACKs trigger immediate retransmission without waiting for timeout. Fast Recovery: ssthresh set to cwnd/2 and cwnd inflated to avoid dropping back to 1 MSS (AIMD).",
            "C": "TCP does not adjust window size dynamically",
            "D": "Fast Retransmit only triggers after a 30-second timeout",
        },
        "answer": "B",
        "explanation": (
            "B — TCP Congestion Control uses AIMD (Additive Increase Multiplicative Decrease): "
            "1. Slow Start: cwnd starts at initial window (e.g. 10 MSS) and doubles every RTT (`cwnd += 1` per ACK). "
            "2. When `cwnd >= ssthresh`, enters Congestion Avoidance (`cwnd += 1/cwnd` per ACK, +1 MSS per RTT). "
            "3. On 3 Duplicate ACKs (packet loss without full stall): Fast Retransmit resends lost segment; Fast Recovery sets `ssthresh = cwnd/2` and keeps sending instead of resetting cwnd to 1 MSS (which only happens on a full RTO timeout)."
        ),
        "tip": "Modern algorithms like Google's BBR (Bottleneck Bandwidth and RTT) move away from loss-based congestion control to bandwidth/delay-product modeling.",
    },
    {
        "id": "net_adv_002",
        "topic": "Computer Networks",
        "difficulty": "interview",
        "q": "Why does QUIC (HTTP/3) run over UDP instead of TCP, and what major problems does it solve?",
        "options": {
            "A": "UDP is unencrypted and therefore faster than TCP",
            "B": "QUIC solves TCP Head-of-Line (HoL) blocking at the transport layer, supports 0-RTT connection resumption, enables connection migration across IP changes (e.g. WiFi to LTE via Connection IDs), and integrates TLS 1.3 directly into the transport handshake.",
            "C": "QUIC eliminates the need for congestion control",
            "D": "QUIC is designed only for DNS lookups",
        },
        "answer": "B",
        "explanation": (
            "B — In HTTP/2 over TCP, if a single packet is lost, the entire TCP connection stalls waiting for retransmission (Transport Head-of-Line blocking), even for unrelated streams. "
            "QUIC runs over UDP and handles independent per-stream retransmissions so packet loss on one stream does not block other streams. "
            "It also binds connections to a 64-bit Connection ID rather than IP:Port tuple, enabling seamless handover when switching networks (WiFi to mobile data)."
        ),
        "tip": "QUIC also eliminates TCP + TLS two-step handshakes by combining transport connection and cryptographic key exchange into a single 1-RTT (or 0-RTT) handshake.",
    },
    {
        "id": "net_adv_003",
        "topic": "Computer Networks",
        "difficulty": "medium",
        "q": "Given the IP address 192.168.10.68 with subnet mask 255.255.255.224 (/27), what is the Network Address and the Broadcast Address?",
        "options": {
            "A": "Network: 192.168.10.0, Broadcast: 192.168.10.255",
            "B": "Network: 192.168.10.64, Broadcast: 192.168.10.95",
            "C": "Network: 192.168.10.64, Broadcast: 192.168.10.127",
            "D": "Network: 192.168.10.32, Broadcast: 192.168.10.63",
        },
        "answer": "B",
        "explanation": (
            "B — Subnet mask 255.255.255.224 has 27 network bits (32 - 27 = 5 host bits). "
            "Block size = 2⁵ = 32. "
            "Subnet ranges in the last octet: 0–31, 32–63, 64–95, 96–127... "
            "Since the IP is .68, it falls into the block 64–95. "
            "Network Address (first IP): 192.168.10.64. "
            "Broadcast Address (last IP): 192.168.10.95. "
            "Usable host IPs: 192.168.10.65 to 192.168.10.94 (30 hosts)."
        ),
        "tip": "Formula for usable hosts: `2^(32 - prefix_length) - 2` (subtracting network and broadcast addresses).",
    },

    # ─────────────────────── ADVANCED SYSTEM DESIGN & DISTRIBUTED SYSTEMS ──────

    {
        "id": "sys_adv_001",
        "topic": "System Design",
        "difficulty": "hard",
        "q": "What is the Saga Pattern in distributed microservices and how does Orchestration vs Choreography compare?",
        "options": {
            "A": "Saga is a database indexing technique for distributed tables",
            "B": "A Saga manages distributed transactions as a sequence of local transactions where each step updates its local DB and publishes an event; if a step fails, compensating transactions are executed in reverse. Choreography uses event-driven pub-sub without a coordinator; Orchestration uses a central orchestrator service telling participants what to execute.",
            "C": "Sagas guarantee ACID isolation across all microservices simultaneously",
            "D": "Saga pattern replaces the need for message brokers",
        },
        "answer": "B",
        "explanation": (
            "B — Because 2-Phase Commit (2PC) does not scale across microservices with independent databases, the Saga pattern provides eventual consistency: "
            "Each microservice executes a local transaction. If step 3 fails, compensating actions (e.g. refund payment, cancel booking) undo steps 1 and 2. "
            "Choreography: Services listen to domain events and react (loose coupling, but hard to track flow). "
            "Orchestration: A central orchestrator (e.g. Temporal, Camunda, AWS Step Functions) explicitly invokes service endpoints and handles failures."
        ),
        "tip": "Sagas provide Atomicity, Consistency, and Durability, but NOT Isolation (ACID without I). Compensating transactions must be idempotent.",
    },
    {
        "id": "sys_adv_002",
        "topic": "System Design",
        "difficulty": "hard",
        "q": "What is the Transactional Outbox Pattern and what fundamental distributed systems problem does it solve?",
        "options": {
            "A": "It sends emails asynchronously to prevent blocking the web thread",
            "B": "It solves dual-write inconsistency (updating database and publishing a message to Kafka/RabbitMQ atomically) by writing the event to an 'outbox' table in the SAME database transaction, and using a separate CDC/poller process to publish to the broker.",
            "C": "It is an outgoing network firewall filter",
            "D": "It replaces relational database replication",
        },
        "answer": "B",
        "explanation": (
            "B — If a service updates its database and then calls `kafkaProducer.send()`, the network may fail or the process may crash between the two actions, leaving the DB updated but the event lost (or vice versa if reversed). "
            "Transactional Outbox writes the business data AND an outbox event row inside a SINGLE local ACID database transaction. "
            "A Change Data Capture (CDC) tool like Debezium or a background poller reads the outbox table and guarantees at-least-once delivery to the message broker."
        ),
        "tip": "Transactional Outbox + CDC + Idempotent Consumer is the gold standard architecture for reliable event-driven microservices.",
    },
    {
        "id": "sys_adv_003",
        "topic": "System Design",
        "difficulty": "interview",
        "q": "How does Snowflake ID generator (Twitter Snowflake) produce 64-bit unique, roughly time-sorted IDs at high scale without central database coordination?",
        "options": {
            "A": "By hashing the entire user request payload with SHA-256",
            "B": "Bit layout: 1 sign bit (0) + 41 bits millisecond timestamp (~69 years) + 10 bits worker/datacenter ID (1024 nodes) + 12 bits sequence counter (4096 IDs per millisecond per node).",
            "C": "By using UUIDv4 random numbers exclusively",
            "D": "By querying a centralized Redis counter via atomic INCR",
        },
        "answer": "B",
        "explanation": (
            "B — Twitter Snowflake generates 64-bit integers structured as: "
            "- 1 bit unused (sign bit) "
            "- 41 bits timestamp in milliseconds since custom epoch (gives 2⁴¹ ms ≈ 69.7 years) "
            "- 10 bits machine/datacenter ID (supports up to 1024 distinct worker nodes) "
            "- 12 bits sequence number (allows up to 4096 unique IDs per millisecond per node). "
            "Because the timestamp is in the highest-order bits, IDs naturally sort chronologically, which keeps database B+ tree index insertions efficient (appending rather than random insertion)."
        ),
        "tip": "UUIDv4 is 128-bit and randomly distributed, causing severe B+ tree index fragmentation. Snowflake IDs are 64-bit (fits in BIGINT) and index-friendly.",
    },

    # ─────────────────────── ADVANCED CONCURRENCY & MEMORY MODELS ─────────────

    {
        "id": "concur_adv_001",
        "topic": "Programming Fundamentals",
        "difficulty": "hard",
        "q": "In the Java Memory Model, what guarantees does the `volatile` keyword provide and what does it NOT provide?",
        "options": {
            "A": "`volatile` makes all compound operations atomic, such as `count++`",
            "B": "`volatile` guarantees Visibility (reads/writes go directly to main memory, bypassing CPU registers/caches) and Ordering (prevents compiler/CPU instruction reordering via memory barriers), but does NOT guarantee Atomicity for compound operations like `count++`.",
            "C": "`volatile` creates a mutex lock around the variable",
            "D": "`volatile` variables are stored exclusively on the thread's local stack",
        },
        "answer": "B",
        "explanation": (
            "B — `volatile` establishes a happens-before relationship: "
            "1. Visibility: Changes made by one thread are immediately visible to all other threads. "
            "2. Instruction Reordering: Inserts memory fences (LoadLoad, LoadStore, StoreStore, StoreLoad) preventing CPU/compiler reordering around volatile reads/writes. "
            "However, `volatile` is NOT atomic for read-modify-write operations: `count++` is 3 instructions (read, increment, write) and subject to race conditions. Use `AtomicInteger` (CAS) or `synchronized` for atomicity."
        ),
        "tip": "Double-checked locking for Singleton requires `volatile` on the instance variable to prevent the constructor instruction reordering where a partially-initialized object reference is published.",
    },
    {
        "id": "concur_adv_002",
        "topic": "Programming Fundamentals",
        "difficulty": "hard",
        "q": "What is Compare-And-Swap (CAS) and what is the ABA problem in lock-free concurrency?",
        "options": {
            "A": "CAS is a software lock; ABA is an operating system deadlock",
            "B": "CAS is an atomic CPU hardware instruction (`CMPXCHG`) that updates a memory location only if it equals an expected value. The ABA problem occurs when a value changes from A to B and back to A; a naive CAS thinks nothing changed even though state/pointers were modified. Fix: Version stamped references (e.g. `AtomicStampedReference`).",
            "C": "CAS is only used in single-threaded Python programs",
            "D": "The ABA problem can only happen with integer primitive types",
        },
        "answer": "B",
        "explanation": (
            "B — CAS (`atomic.compare_exchange` / `AtomicInteger.compareAndSet`) allows lock-free optimistic concurrency: read old value, calculate new value, try CAS. If another thread changed it, retry loop. "
            "The ABA problem: Thread 1 reads value A from node head. Thread 2 changes A -> B -> frees A and allocates new node at same memory address A. "
            "Thread 1 executes CAS(A, new) and succeeds, but the underlying data structure was modified! "
            "Solution: Attach a version/generation counter to the pointer (e.g. `AtomicStampedReference` in Java or tagged pointers)."
        ),
        "tip": "Lock-free structures (Treiber stack, Michael-Scott queue) rely on CAS and must handle the ABA problem.",
    },

    # ─────────────────────── ADVANCED WEB & SECURITY ──────────────────────────

    {
        "id": "sec_adv_001",
        "topic": "Web Fundamentals",
        "difficulty": "interview",
        "q": "What is the difference between Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF), and how is each prevented?",
        "options": {
            "A": "XSS and CSRF are identical attack vectors",
            "B": "XSS injects and executes malicious JavaScript in the victim's browser (prevented by contextual output encoding, CSP, and httpOnly cookies). CSRF tricks an authenticated user's browser into submitting unauthorized requests to a trusted site (prevented by SameSite cookies, anti-CSRF tokens, and custom headers).",
            "C": "CSRF is prevented by encoding HTML outputs",
            "D": "XSS only attacks the backend database",
        },
        "answer": "B",
        "explanation": (
            "B — XSS (Cross-Site Scripting): Attacker executes script inside the victim's browser context to steal cookies, session tokens, or manipulate DOM. Defense: Output encoding (sanitize HTML/JS), Content Security Policy (CSP), `httpOnly` cookie flags. "
            "CSRF (Cross-Site Request Forgery): Attacker hosts a malicious link/form that triggers an unauthorized POST request to `bank.com/transfer` using the browser's automatically attached session cookies. Defense: `SameSite=Strict/Lax` cookie attribute, Synchronizer Anti-CSRF tokens, verifying Origin/Referer headers."
        ),
        "tip": "Remember: XSS exploits the user's trust in a website (runs unauthorized script on the website). CSRF exploits the website's trust in the user's browser (sends unauthorized requests with user credentials).",
    },
]
