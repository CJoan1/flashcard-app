import random
UNDERSTAND = "understand"
STILL_LEARNING = "still_learning"
QUIT_COMMAND = "quit"

# ── Constants ─────────────────────────────────────────────────────────────────
UNDERSTAND = "understand"       # label for cards the user got right
STILL_LEARNING = "still_learning"  # label for cards the user got wrong
QUIT_COMMAND = "quit"           # keyword to exit the app at any point
QUIT_EARLY = True               # returned by game_logic if user typed quit
FINISHED = False                # returned by game_logic if quiz completed normally
MAX_HINTS = 3                   # maximum number of hints allowed per card

# ── Flashcard data ────────────────────────────────────────────────────────────
# Each flashcard is a dictionary with a 'question' and an 'answer' key.
# Add, remove, or edit cards here to customise the quiz.
flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"question": "What is 12 x 12?", "answer": "144"},
    {"question": "What language runs in a web browser?", "answer": "JavaScript"},
    {"question": "What does RAM stand for?", "answer": "Random Access Memory"},
]


def get_valid_input(prompt, valid_options):
    """
    Repeatedly prompts the user until a valid input is received.

    Args:
        prompt (str): the question to display to the user
        valid_options (list): list of accepted responses

    Returns:
        str: the valid input from the user
    """
    while True:
        response = input(prompt).strip().lower()
        if response in valid_options:
            return response
        # inform the user what the accepted inputs are and try again
        print(f"Invalid input — please enter {' or '.join(valid_options)}")


def game_logic(cards):
    """
    Runs the quiz loop over a list of flashcards.

    Shows each card one at a time, masked as underscores.
    The user types their answer directly — it is checked automatically.
    Hints reveal one letter at a time up to MAX_HINTS.
    Using a hint marks the card as still_learning even if answered correctly.
    Exits early if the user types 'quit'.

    Args:
        cards (list): list of dicts with 'question' and 'answer' keys

    Returns:
        understand (list): cards the user got right without hints
        still_learning (list): cards the user got wrong or used hints on
        QUIT_EARLY/FINISHED (bool): whether the user quit early
    """
    total = len(cards)
    understand = []
    still_learning = []

    for idx, card in enumerate(cards, start=1):
        # show progress — e.g. "2 of 5"
        print(f" {idx} of {total}")

        question = card['question']
        answer = card['answer']
        print(question)

        # track hint usage per card — resets for each new card
        hints_used = 0
        hint_penalty = False  # becomes True if user requests any hint

        # calculate max hints for this card — never reveal the full answer
        letter_count = len(answer.replace(" ", ""))
        max_hints = min(MAX_HINTS, letter_count - 1)

        # show the answer masked as underscores e.g. "_ _ _ _ _"
        print(mask_answer(answer))

        while True:
            # wait for user to type an answer, 'hint', or 'quit'
            option = input("Answer (or 'hint'): ").strip().lower()

            # exit the quiz early, returning whatever was sorted so far
            if option == QUIT_COMMAND:
                return understand, still_learning, QUIT_EARLY

            elif option == "hint":
                if hints_used < max_hints:
                    hints_used += 1
                    hint_penalty = True  # flag that a hint was used this card
                    print(reveal_hint(hints_used, answer))
                    # warn user when they've used their last available hint
                    if hints_used == max_hints:
                        print("Last hint used — answer now or it will be marked wrong")
                else:
                    # hints are exhausted — block further requests
                    print("No more hints available — answer now or it will be marked wrong")

            # correct answer — sort based on whether hints were used
            elif option == answer.lower():
                if hint_penalty:
                    # penalise hint usage — correct but kept in still_learning
                    print("Correct! But you used a hint — keeping in still learning")
                    sort_card(card, understand, still_learning, STILL_LEARNING)
                else:
                    print("Correct!")
                    sort_card(card, understand, still_learning, UNDERSTAND)
                break

            else:
                # wrong answer or gave up after hints ran out
                if hints_used >= max_hints:
                    print(f"Out of hints. Missed: {answer}")
                else:
                    print(f"You missed it: {answer}")
                sort_card(card, understand, still_learning, STILL_LEARNING)
                break

        print("-" * 40)

    # quiz completed normally — all cards were attempted
    return understand, still_learning, FINISHED


def shuffle_cards(cards):
    """
    Shuffles the list of cards in place using random.shuffle.

    Args:
        cards (list): the list of flashcards to shuffle
    """
    # modifies the list directly — no return value needed
    random.shuffle(cards)


def sort_card(card, understand, still_learning, sort):
    """
    Sorts a single card into the understand or still_learning list.

    Args:
        card (dict): the flashcard being sorted
        understand (list): cards the user got right
        still_learning (list): cards the user got wrong
        sort (str): UNDERSTAND or STILL_LEARNING constant
    """
    if sort == UNDERSTAND:
        understand.append(card)  # user got it right without hints
    if sort == STILL_LEARNING:
        still_learning.append(card)  # user got it wrong or used hints


def offer_practice(cards, total_understand, total):
    """
    Offers the user a chance to practice cards they got wrong.

    Loops until the user declines, quits, or all cards are
    moved to understand.

    Args:
        cards (list): cards the user got wrong
        total_understand (list): cumulative list of mastered cards
                                 carried forward from previous rounds
        total (int): total number of cards in the original deck

    Returns:
        cards (list): remaining cards still not mastered after
        all practice rounds. Empty if user mastered everything.
    """
    while cards:
        # keep offering practice as long as there are wrong cards
        response = get_valid_input(
            "Do you want to practice the questions you got wrong? y/n: ",
            ["y", "n", QUIT_COMMAND]
        )

        if response == QUIT_COMMAND:
            return cards  # exit immediately, return current state

        if response == "y":
            # ask whether to shuffle before the next practice round
            shuffle = get_valid_input(
                "Do you want to shuffle cards? y/n: ",
                ["y", "n", QUIT_COMMAND]
            )
            if shuffle == QUIT_COMMAND:
                return cards  # exit immediately, return current state
            if shuffle == "y":
                shuffle_cards(cards)

            # run another quiz round with only the wrong cards
            # cards is reassigned to the new still_learning each round
            round_understand, cards, quit_early = game_logic(cards)

            if quit_early:
                return cards  # user quit mid-practice — stop immediately

            # accumulate correctly answered cards across all rounds
            total_understand += round_understand
            session_feedback(total_understand, total, cards)

        if response == "n":
            # user chose not to practice — show final summary and exit
            session_feedback(total_understand, total, cards)
            return cards

    return cards  # all cards mastered — while condition became False


def session_feedback(total_understand, total, cards):
    """
    Displays a summary of the user's progress after each round.

    Shows how many cards are understood, how many are still being
    learned, the percentage mastered, and which cards were missed.

    Args:
        total_understand (list): cumulative list of cards mastered
                                 across all rounds
        total (int): total number of cards in the original deck
        cards (list): cards still in still_learning after this round
    """
    # show raw counts
    print(f"Understand: {len(total_understand)}")
    print(f"Still learning: {len(cards)}")

    # calculate percentage of the full deck mastered
    mastered = (len(total_understand) / total) * 100

    if mastered == 100:
        print(f"You've mastered {mastered}% of the cards. Good Job!")
    elif mastered >= 50:
        print(f"You've mastered {mastered}% of the cards. Almost there. Keep practicing")
        # list the specific cards still being learned
        for card in cards:
            print(f"Missed: {card['question']}")
    else:
        print(f"You've mastered {mastered}% of the cards. You can do better. Keep practicing")
        # list the specific cards still being learned
        for card in cards:
            print(f"Missed: {card['question']}")


def mask_answer(answer):
    """
    Replaces every character in the answer with an underscore,
    preserving spaces so multi-word answers stay readable.

    Args:
        answer (str): the correct answer to mask

    Returns:
        str: the masked answer — e.g. "Paris" becomes "_ _ _ _ _"
    """
    # spaces are kept as spaces so word boundaries stay visible
    return " ".join("_" if char != " " else " " for char in answer)


def reveal_hint(hints_used, answer):
    """
    Reveals a given number of letters from the start of the answer,
    replacing the rest with underscores.

    Args:
        hints_used (int): how many letters to reveal from the left
        answer (str): the correct answer

    Returns:
        str: partially revealed answer — e.g. "P a _ _ _" for hints_used=2
    """
    result = []
    revealed = 0  # tracks how many letters have been shown so far

    for char in answer:
        if char == " ":
            result.append(" ")          # preserve spaces between words
        elif revealed < hints_used:
            result.append(char)         # reveal this letter
            revealed += 1
        else:
            result.append("_")          # hide remaining letters

    return " ".join(result)


def run_app(cards):
    """
    Entry point for the flashcard app.

    Prints the introduction, runs the main quiz, then
    offers a practice round for any cards answered incorrectly.

    Args:
        cards (list): the full list of flashcards to quiz
    """
    total = len(cards)

    # introduction
    print("\n Welcome to Flashcard Quiz!")
    print(f"   {total} cards to go. \n")
    print("Type your answer and press Enter.")
    print("Type 'hint' for a hint.")
    print("Type 'quit' to exit at any time.")
    print("-" * 40)

    # ask whether to shuffle before starting — loops until valid input
    shuffle = get_valid_input(
        "Do you want to shuffle cards? y/n: ",
        ["y", "n", QUIT_COMMAND]
    )

    if shuffle == QUIT_COMMAND:
        return  # user quit before the quiz started
    if shuffle == "y":
        shuffle_cards(cards)

    # run the main quiz and capture results
    understand, still_learning, quit_early = game_logic(cards)

    # show summary after the first round
    session_feedback(understand, total, still_learning)

    # only offer practice if the user finished the quiz naturally
    if not quit_early:
        still_learning = offer_practice(still_learning, understand, total)


if __name__ == '__main__':
    run_app(flashcards)
