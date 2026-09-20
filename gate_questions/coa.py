"""Computer Organization & Architecture (COA) GATE Question Bank."""

QUESTIONS = [
    {
        "id": "coa_cache_001",
        "subject": "Computer Organization & Architecture",
        "topic": "Memory Hierarchy",
        "subtopic": "Cache Mapping (Direct, Associative, Set-Associative)",
        "concept": "Tag, Set Index, and Word Offset bit fields in a Set-Associative Cache",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "A 4-way set-associative cache memory with a total capacity of 64 KB has a block size of 32 bytes. The CPU generates 32-bit byte addresses. How many bits are required for the CACHE TAG field?",
        "options": None,
        "answer": "18",
        "msq_answers": None,
        "explanation": "1. Block size = 32 bytes = 2^5 bytes ⟹ Byte Offset = 5 bits.\n2. Total cache size = 64 KB = 2^16 bytes.\n3. Total number of lines/blocks = 64 KB / 32 B = 2^16 / 2^5 = 2^11 = 2048 blocks.\n4. Set Associativity = 4-way (4 blocks per set).\n5. Number of sets = Total blocks / Associativity = 2^11 / 4 = 2^9 = 512 sets ⟹ Set Index = 9 bits.\n6. Address size = 32 bits.\n7. Tag bits = Total Address bits - (Set Index bits + Offset bits)\n   Tag bits = 32 - (9 + 5) = 32 - 14 = 18 bits.",
        "gate_trap": "Do not divide cache size by set associativity to find block count. First calculate total blocks, then divide by associativity to find set count.",
        "key_concept": "Tag bits = Address bits − log2(# of Sets) − log2(Block Size in bytes).",
        "reference_url": "https://www.geeksforgeeks.org/cache-memory-in-computer-organization/"
    },
    {
        "id": "coa_pipe_001",
        "subject": "Computer Organization & Architecture",
        "topic": "Instruction Pipelining",
        "subtopic": "Pipeline Stages & Throughput Calculation",
        "concept": "Speedup and cycle time calculation in a non-uniform pipeline with stage delays",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "A 5-stage non-pipelined processor has stage delays of 150 ps, 120 ps, 180 ps, 160 ps, and 140 ps. It is converted into a 5-stage pipelined processor where each stage has an additional pipeline latch delay of 20 ps. What is the clock cycle time (in ps) of the pipelined processor?",
        "options": None,
        "answer": "200",
        "msq_answers": None,
        "explanation": "In a synchronous pipelined processor:\nClock cycle time = (Maximum stage delay) + (Pipeline latch / register delay)\nMax stage delay = max(150, 120, 180, 160, 140) = 180 ps.\nLatch delay = 20 ps.\nClock cycle time = 180 + 20 = 200 ps.",
        "gate_trap": "In pipelining, the clock period is constrained by the BOTTLENECK (slowest) stage plus the latch overhead, not the average stage delay.",
        "key_concept": "Pipeline Clock Cycle (Tp) = max(Stage Delays) + Latch Overhead Delay.",
        "reference_url": "https://www.geeksforgeeks.org/pipelining-set-2-dependencies-and-data-hazard/"
    },
    {
        "id": "coa_hazard_001",
        "subject": "Computer Organization & Architecture",
        "topic": "Instruction Pipelining",
        "subtopic": "Structural, Data & Control Hazards",
        "concept": "RAW data hazards and forwarding paths in pipelined execution",
        "type": "MSQ",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Which of the following techniques can eliminate or reduce stalls caused by Data Hazards in an instruction pipeline?\n\nSelect all that apply:",
        "options": {
            "A": "Operand Forwarding / Bypassing from EX/MEM or MEM/WB pipeline registers",
            "B": "Instruction Scheduling / Reordering by the compiler",
            "C": "Increasing the number of general-purpose CPU registers",
            "D": "Branch Prediction"
        },
        "answer": "A, B",
        "msq_answers": ["A", "B"],
        "explanation": "- A is TRUE: Operand forwarding feeds computed ALU results directly to waiting instructions without waiting for the WB (Write Back) stage.\n- B is TRUE: Static instruction scheduling by compiler inserts independent instructions between producer and consumer.\n- C is FALSE: Increasing registers alone does not resolve RAW hazards between dependent instructions.\n- D is FALSE: Branch prediction addresses CONTROL hazards, not data hazards.",
        "gate_trap": "Branch prediction is strictly for Control Hazards (conditional jumps), NOT Data Hazards (RAW/WAR/WAW).",
        "key_concept": "Data hazards are mitigated by Operand Forwarding, Compiler Scheduling, and Hardware Interlocking (hazard stalls).",
        "reference_url": "https://www.geeksforgeeks.org/pipeline-hazards-in-computer-architecture/"
    }
]
