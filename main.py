import random

flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"question": "What is 12 x 12?", "answer": "144"},
    {"question": "What language runs in a web browser?", "answer": "JavaScript"},
    {"question": "What does RAM stand for?", "answer": "Random Access Memory"},
]


def game_logic(cards):
    """
    Runs the quiz loop over a list of flashcards.

    Shows each card one at a time, reveals the answer on Enter,
    and sorts each card based on the user's response.
    Exits early if the user types 'quit'.

    Args:
        cards (list): list of dicts with 'question' and 'answer' keys

    Returns:
        understand (list): cards the user got right
        still_learning (list): cards the user got wrong
    """
    total = len(cards)
    understand = []
    still_learning = []
    # Shuffle cards
    shuffle = input("Do you want to shuffle cards? y/n:").strip().lower()
    if shuffle == "y":
        shuffle_cards(cards)

    for idx, card in enumerate(cards, start=1):
        # show progress — e.g. "2 of 5"
        print(f" {idx} of {total}")

        question = card['question']
        answer = card['answer']
        print(question)

        # wait for user to press Enter or type a command
        option = input("").strip()

        if option == "":
            print(answer)
            # ask user if they got it right and sort accordingly
            sort = input("Did you get it right? y/n:").strip().lower()
            sort_card(card, understand, still_learning, sort)

        # exit the quiz early, returning whatever was sorted so far
        if option == "quit":
            return understand, still_learning

        print("-" * 40)

    return understand, still_learning

def shuffle_cards(cards):
    random.shuffle(cards)

def sort_card(card, understand, still_learning, sort):
    """
    Sorts a single card into the understand or still_learning list.

    Args:
        card (dict): the flashcard being sorted
        understand (list): cards the user got right
        still_learning (list): cards the user got wrong
        sort (str): user input — 'y' for correct, 'n' for incorrect
    """
    if sort == "y":
        understand.append(card)  # user got it right
    if sort == "n":
        still_learning.append(card)  # user got it wrong


def offer_practice(cards):
    """
    Offers the user a chance to practice cards they got wrong.

    Loops until the user declines or all cards are moved
    to understand.

    Args:
        cards (list): cards the user got wrong
    """
    while cards:
        # keep offering practice as long as there are wrong cards
        response = input("Do you want to practice the questions you got wrong? y/n:").strip().lower()

        if response == "y":
            # run another quiz round with only the wrong cards
            # cards is reassigned to the new still_learning each round
            understand, cards = game_logic(cards)

        if response == "n":
            break  # user chose to stop — exit the loop


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
    print("Press Enter to see answer.")
    print("Type quit to exit.")
    print("-" * 40)

    # run the main quiz and capture results
    understand, still_learning = game_logic(cards)

    # offer a practice round for wrong answers if there are any
    offer_practice(still_learning)


if __name__ == '__main__':
    run_app(flashcards)