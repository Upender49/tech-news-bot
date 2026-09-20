"""Engineering Mathematics (Linear Algebra, Calculus, Probability) GATE Question Bank."""

QUESTIONS = [
    {
        "id": "em_la_001",
        "subject": "Engineering Mathematics",
        "topic": "Linear Algebra",
        "subtopic": "Eigenvalues & Eigenvectors",
        "concept": "Eigenvalues properties and trace/determinant relations",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "Let A be a 3 x 3 real matrix with eigenvalues 1, 2, and -3. What is the value of the DETERMINANT of the matrix (A^2 - 2A + I)?",
        "options": None,
        "answer": "0",
        "msq_answers": None,
        "explanation": "If lambda is an eigenvalue of matrix A, then f(lambda) is an eigenvalue of matrix f(A).\nHere, polynomial f(x) = x^2 - 2x + 1 = (x - 1)^2.\nFor eigenvalue lambda1 = 1: f(1) = (1 - 1)^2 = 0.\nFor eigenvalue lambda2 = 2: f(2) = (2 - 1)^2 = 1.\nFor eigenvalue lambda3 = -3: f(-3) = (-3 - 1)^2 = 16.\nThe eigenvalues of (A^2 - 2A + I) are 0, 1, and 16.\nThe determinant of a matrix is the product of its eigenvalues:\ndet(A^2 - 2A + I) = 0 * 1 * 16 = 0.",
        "gate_trap": "Because one of the transformed eigenvalues f(1) is 0, the determinant (product of eigenvalues) is immediately 0 without needing full matrix computation.",
        "key_concept": "If lambda_i are eigenvalues of A, then f(lambda_i) are eigenvalues of f(A), and det(M) = product of eigenvalues.",
        "reference_url": "https://www.geeksforgeeks.org/eigen-values-properties/"
    },
    {
        "id": "em_prob_001",
        "subject": "Engineering Mathematics",
        "topic": "Probability & Statistics",
        "subtopic": "Conditional Probability & Bayes' Theorem",
        "concept": "Bayes Theorem for false positive probability calculations",
        "type": "NAT",
        "marks": 2,
        "difficulty": "gate",
        "source": "GATE-STYLE",
        "pyq_year": None,
        "q": "A medical test for a disease has a 99% true positive rate (sensitivity) and a 5% false positive rate (1 - specificity). The prevalence of the disease in the population is 0.1% (0.001). A randomly selected person tests POSITIVE. What is the probability (in percentage, rounded to 2 decimal places) that the person actually has the disease?",
        "options": None,
        "answer": "1.94",
        "msq_answers": None,
        "explanation": "Let D = has disease, T+ = tests positive.\n- P(D) = 0.001, P(~D) = 0.999.\n- P(T+|D) = 0.99 (sensitivity).\n- P(T+|~D) = 0.05 (false positive rate).\n\nBy Bayes' Theorem:\nP(D|T+) = (P(T+|D) * P(D)) / (P(T+|D)*P(D) + P(T+|~D)*P(~D))\nNumerator = 0.99 * 0.001 = 0.00099\nDenominator = 0.00099 + (0.05 * 0.999) = 0.00099 + 0.04995 = 0.05094\nP(D|T+) = 0.00099 / 0.05094 ≈ 0.0194346 = 1.94%.",
        "gate_trap": "Even with 99% accuracy, when disease prevalence is very low (0.1%), the vast majority of positive tests are false positives due to the base-rate fallacy.",
        "key_concept": "Bayes' Theorem: P(A|B) = [P(B|A) * P(A)] / P(B). Never ignore base rate prevalence P(A).",
        "reference_url": "https://www.geeksforgeeks.org/bayes-theorem-in-probability/"
    }
]
