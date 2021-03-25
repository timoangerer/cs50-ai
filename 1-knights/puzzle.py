from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A person can't be a Knave and a Knight at the same time
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), # XOR

    Biconditional(AKnight, And(AKnight, AKnave)),

    # We can also use one or both of the following statements
    # Implication(AKnight, And(AKnight, AKnave)),  # Knights say the truth
    # Implication(AKnave, Not(And(AKnight, AKnave)))  # Knaves lie
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A person can't be a Knave and a Knight at the same time
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), # XOR
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))), # XOR

    Biconditional(AKnight, And(AKnave, BKnave)),

    # Without Biconditional
    # Implication(AKnight, And(AKnave, BKnave)),
    # Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

ABKnight = And(AKnight, BKnight)
ABKnave = And(AKnave, BKnave)

knowledge2 = And(
    # A person can't be a Knave and a Knight at the same time
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), # XOR
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))), # XOR

    Biconditional(AKnight, Or(ABKnight, ABKnave)),  # A is a Knight if and only if Both are Knights or if Both are Knaves
    Biconditional(BKnight, Or( # B is a Knight if and only if they are the different from eachother
            And(AKnight, Not(BKnight)),
            And(AKnave, Not(BKnave))
        )
    )

    # Without Biconditionals:

    # Implication(AKnight, Or(ABKnight, ABKnave)), # A is a Knight if Either A and B are Knights, or A and B are Knaves
    # Implication(AKnave, Or( # A is a Knave if They are different
    #         And(AKnight, Not(BKnight)),
    #         And(AKnave, Not(BKnave))
    #     )),

    # Implication(BKnight,  Or( # B is a Knight if they are the different
    #         And(AKnight, Not(BKnight)),
    #         And(AKnave, Not(BKnave))
    #     )
    # ),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A person can't be a Knave and a Knight at the same time
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), # XOR
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))), # XOR
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))), # XOR

    # We don't know more about A

    # B says
    Implication(BKnight, AKnight),
    Biconditional(BKnight, CKnave),

    # C says
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
