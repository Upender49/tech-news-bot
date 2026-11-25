"""Aptitude Syllabus — Phase-wise topic tree for Placement & GATE Aptitude.

Based on the 13-phase curriculum designed for final-year B.Tech students
targeting campus placements and GATE General Aptitude section.
"""

APTITUDE_SYLLABUS = {
    "Percentages": {
        "phase": 1,
        "weight": 10.0,     # Importance weight (1-10 scale; ⭐⭐⭐⭐⭐ = 10)
        "importance": 5,
        "topics": {
            "Basic Percentage Calculations": [
                "Percentage of a number", "Fraction-to-percent conversion",
                "Percentage increase/decrease", "Net successive percentage change"
            ],
            "Applications of Percentages": [
                "Population growth/decline", "Exam marks percentage",
                "Salary hike/demotion", "Income & expenditure percentage"
            ]
        }
    },
    "Ratios & Proportions": {
        "phase": 1,
        "weight": 9.5,
        "importance": 5,
        "topics": {
            "Ratios": [
                "Compound ratios", "Inverse ratios", "Dividing a quantity in a ratio",
                "Ratios involving increase/decrease"
            ],
            "Proportions": [
                "Direct proportion", "Inverse proportion", "Chain rule (unitary method)",
                "Partnership — simple and weighted"
            ]
        }
    },
    "Averages": {
        "phase": 2,
        "weight": 8.5,
        "importance": 4,
        "topics": {
            "Simple & Weighted Averages": [
                "Average of consecutive integers", "Weighted average formula",
                "Combined average of groups"
            ],
            "Age Problems": [
                "Present age calculation", "Average age with joins/removals",
                "Age ratio problems"
            ]
        }
    },
    "Mixtures & Alligation": {
        "phase": 2,
        "weight": 8.0,
        "importance": 4,
        "topics": {
            "Alligation Rule": [
                "Mean price using alligation cross", "Mixing two mixtures",
                "Three-component mixing"
            ],
            "Replacement Problems": [
                "Successive replacement formula", "Wine-water replacement",
                "Concentration after n replacements"
            ]
        }
    },
    "Profit Loss Discounts": {
        "phase": 3,
        "weight": 10.0,
        "importance": 5,
        "topics": {
            "Profit & Loss": [
                "CP, SP, Profit%, Loss% relationships", "Dishonest dealings (false weight)",
                "Overall P&L on multiple transactions"
            ],
            "Discount & Marked Price": [
                "Single discount equivalent to successive discounts",
                "Marked price from given conditions",
                "Combined effect of discount and profit"
            ]
        }
    },
    "Time & Work": {
        "phase": 4,
        "weight": 10.0,
        "importance": 5,
        "topics": {
            "Work Rate Problems": [
                "LCM method", "Efficiency ratios",
                "Work done in fractional days", "Alternate-day work"
            ],
            "Combined Work": [
                "A + B together finish in X days", "Joining mid-task",
                "Negative work (opposition)", "Wages proportional to work"
            ]
        }
    },
    "Pipes & Cisterns": {
        "phase": 4,
        "weight": 9.0,
        "importance": 5,
        "topics": {
            "Fill & Drain": [
                "Time to fill with both open", "Leak-based problems",
                "Fraction filled in time t"
            ],
            "Combined Pipe Problems": [
                "Two inlets one outlet", "Opening/closing at different times",
                "Finding time for one pipe given combined time"
            ]
        }
    },
    "Time Speed Distance": {
        "phase": 5,
        "weight": 10.0,
        "importance": 5,
        "topics": {
            "Basic TSD": [
                "Relative speed (same/opposite)", "km/h ↔ m/s conversion",
                "Average speed (harmonic mean for equal distances)"
            ],
            "Trains": [
                "Crossing a pole/person", "Crossing a platform",
                "Two trains crossing each other"
            ],
            "Boats & Streams": [
                "Upstream / downstream time", "Speed of boat in still water",
                "Speed of stream"
            ],
            "Circular Tracks": [
                "Meeting time at start point", "First meeting on the track",
                "Multiple runners"
            ]
        }
    },
    "Simple & Compound Interest": {
        "phase": 6,
        "weight": 7.0,
        "importance": 3,
        "topics": {
            "Simple Interest": [
                "SI formula applications", "Finding unknown (P, R, T)",
                "Comparing SI at different rates"
            ],
            "Compound Interest": [
                "Annual / half-yearly / quarterly compounding",
                "CI - SI difference for 2 and 3 years",
                "Population and depreciation problems"
            ]
        }
    },
    "Number System": {
        "phase": 7,
        "weight": 10.0,
        "importance": 5,
        "topics": {
            "Divisibility & Remainders": [
                "Divisibility rules 2 through 13", "HCF/LCM word problems",
                "Remainder theorems (Fermat, Euler, Chinese Remainder)",
                "Cyclicity of unit digits"
            ],
            "Number Properties": [
                "Trailing zeros in n!", "Number of factors",
                "Sum of factors", "Perfect squares/cubes identification"
            ]
        }
    },
    "Permutations & Combinations": {
        "phase": 8,
        "weight": 9.0,
        "importance": 4,
        "topics": {
            "Arrangements": [
                "Linear arrangements with restrictions",
                "Circular permutations", "Necklace problems",
                "Arrangements of words with repeated letters"
            ],
            "Selections": [
                "Combination with identical items",
                "Committees with conditions (at least / at most)",
                "Distribution problems", "Derangements"
            ]
        }
    },
    "Probability": {
        "phase": 9,
        "weight": 9.0,
        "importance": 4,
        "topics": {
            "Classical Probability": [
                "Dice, coins, cards problems",
                "Conditional probability", "Independent events",
                "Mutually exclusive events"
            ],
            "Advanced Probability": [
                "Bayes' theorem applications",
                "At-least-one type (complementary counting)",
                "Expected value", "Geometric probability"
            ]
        }
    },
    "Logical Reasoning": {
        "phase": 10,
        "weight": 10.0,
        "importance": 5,
        "topics": {
            "Puzzles & Arrangements": [
                "Seating arrangements (linear/circular)",
                "Blood relations (3-generation)",
                "Direction sense with multiple turns",
                "Ranking and ordering"
            ],
            "Coding & Series": [
                "Letter/number coding-decoding",
                "Number series completion (differences, ratios, primes)",
                "Alpha-numeric series", "Input-Output shift patterns"
            ],
            "Statements & Conclusions": [
                "Syllogism (Venn diagram method)",
                "Statement-assumption type",
                "Statement-conclusion validity",
                "Cause and effect"
            ]
        }
    },
    "Data Interpretation": {
        "phase": 11,
        "weight": 10.0,
        "importance": 5,
        "topics": {
            "Tabular DI": [
                "Percentage calculations from table",
                "Growth rate computation",
                "Ratio and proportion from data"
            ],
            "Graphical DI": [
                "Bar chart comparison (absolute and relative)",
                "Pie chart (degrees to values)",
                "Line graph trend analysis",
                "Mixed graph (bar + line)"
            ]
        }
    },
    "Verbal Ability": {
        "phase": 12,
        "weight": 9.0,
        "importance": 4,
        "topics": {
            "Grammar & Sentence Correction": [
                "Parallelism errors", "Dangling modifiers",
                "Subject-verb agreement", "Tense consistency"
            ],
            "Vocabulary in Context": [
                "Fill in the blank (contextual meaning)",
                "Idioms and phrases", "Synonym/antonym in context",
                "One-word substitution"
            ],
            "Reading & Para Skills": [
                "RC — inference type", "RC — tone/purpose of passage",
                "Para-jumbles (5-sentence reordering)",
                "Para completion"
            ]
        }
    },
    "Spatial Reasoning": {
        "phase": 13,
        "weight": 7.0,
        "importance": 3,
        "topics": {
            "Clocks & Calendars": [
                "Angle between clock hands",
                "Times when hands coincide/perpendicular/opposite",
                "Day of week calculation (odd days)",
                "Leap year calendar problems"
            ],
            "Venn Diagrams": [
                "3-set intersection problems",
                "Finding members in exactly 2 sets",
                "Only/at-least conditions"
            ],
            "Shapes & Images": [
                "Mirror/water image of letters and figures",
                "Paper folding and cutting outcomes",
                "Matrix pattern completion (described)"
            ]
        }
    },
    "Mixed Aptitude": {
        "phase": 11,  # mixed placement-level
        "weight": 9.5,
        "importance": 5,
        "topics": {
            "Multi-Concept Problems": [
                "Time-Work + Profit combined",
                "Percentage + TSD combined",
                "Interest + Ratio combined",
                "3-step reasoning chains"
            ]
        }
    }
}

# Phase rotation order for session selection
APTITUDE_PHASE_ORDER = [
    1,  # Percentages & Ratios
    7,  # Number System
    4,  # Time & Work
    5,  # Time Speed Distance
    8,  # Permutations & Combinations
    3,  # Profit & Loss
    9,  # Probability
    2,  # Averages & Mixtures
    10, # Logical Reasoning
    11, # DI + Mixed
    6,  # Interest
    12, # Verbal Ability
    13, # Spatial Reasoning
]

# Topic to phase mapping for quick lookup
TOPIC_PHASE_MAP = {
    topic: data["phase"]
    for topic, data in APTITUDE_SYLLABUS.items()
}
