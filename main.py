import random
UNDERSTAND = "understand"
STILL_LEARNING = "still_learning"
QUIT_COMMAND = "quit"

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

    for idx, card in enumerate(cards, start=1):
        # show progress — e.g. "2 of 5"
        print(f" {idx} of {total}")

        question = card['question']
        answer = card['answer']
        print(question)
        hints_used = 0
        print(mask_answer(answer))

        while True:
            # wait for user to type in answer or type a command
            option = input("Answer (or 'hint'): ").strip().lower()

            # exit the quiz early, returning whatever was sorted so far
            if option == QUIT_COMMAND:
                return understand, still_learning
            
            elif option == "hint":
                hints_used += 1
                print(reveal_hint(hints_used, answer))
            
            # if answer is correct
            elif option == answer.lower():
                print("Correct!")
                # ask user if they got it right and sort accordingly
                sort = UNDERSTAND
                sort_card(card, understand, still_learning, sort)
                break

            elif option == "" or option != answer.lower():
                print(f"You missed it: {answer}")
                # ask user if they got it right and sort accordingly
                sort = STILL_LEARNING
                sort_card(card, understand, still_learning, sort)
                break
        
        print("-" * 40)

    return understand, still_learning

def shuffle_cards(cards):
    """
    Shuffles the list of cards in place using random.shuffle.
 
    Args:
        cards (list): the list of flashcards to shuffle
    """
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
    if sort == UNDERSTAND:
        understand.append(card)  # user got it right
    if sort == STILL_LEARNING:
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
        
        if response== QUIT_COMMAND:
            break  # done — exit the loop

        if response == "y":
            # run another quiz round with only the wrong cards
            # cards is reassigned to the new still_learning each round
            shuffle = input("Do you want to shuffle cards? y/n:").strip().lower()
            if shuffle == "y":
                shuffle_cards(cards)
                understand, cards = game_logic(cards)
            elif shuffle == "n":
                understand, cards = game_logic(cards)

        if response == "n":
            return # user chose to stop — exit the loop

def mask_answer(answer):
    """
    Replaces every character in the answer with an underscore,
    preserving spaces so multi-word answers stay readable.
 
    Args:
        answer (str): the correct answer to mask
 
    Returns:
        str: the masked answer — e.g. "Paris" becomes "_ _ _ _ _"
    """
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
    revealed = 0
    for char in answer:
        if char == " ":
            result.append(" ")
        elif revealed < hints_used:
            result.append(char)   # reveal this letter
            revealed += 1
        else:
            result.append("_")    # still hidden
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
    print("Press Enter to see answer.")
    print("Type quit to exit.")
    print("-" * 40)

    # Shuffle cards
    shuffle = input("Do you want to shuffle cards? y/n:").strip().lower()
    # exit the quiz early, returning whatever was sorted so far
    while True:
        if shuffle == QUIT_COMMAND:
            break  # done — exit the loop
        elif shuffle in ("y", "n"):
            if shuffle == "y":
                shuffle_cards(cards)
            # run the main quiz and capture results
            understand, still_learning = game_logic(cards)
            # offer a practice round for wrong answers if there are any
            offer_practice(still_learning)
            break
        else:
            print("Invalid response")
            shuffle = input("Do you want to shuffle cards? y/n:").strip().lower()
        


if __name__ == '__main__':
    run_app(flashcards)
