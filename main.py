flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"question": "What is 12 x 12?", "answer": "144"},
    {"question": "What language runs in a web browser?", "answer": "JavaScript"},
    {"question": "What does RAM stand for?", "answer": "Random Access Memory"},
]


understand = []
still_learning = []


def game_logic(cards):
    total = len(cards)
    for idx, card in enumerate(cards, start=1):
        # list what number we are on
        print(f" {idx} of {total}")
        question = card['question']
        answer = card['answer']
        print(question)
        # see answer
        option = input("").strip()
        if option == "":
            print(answer)
            # sort card into understand and still-learning
            sort = input("Did you get it right? y/n:").strip().lower()
            if sort == "y":
                understand.append(card)
            if sort == "n":
                still_learning.append(card)
        # quit app
        if option == "quit":
            return
        print("-" * 40)
    # Review hard questions
    if still_learning:
        response = input("Do you want to practice the quesionts you got wrong? y/n").strip().lower()
        if response == "y":
            practice(still_learning.copy())
        if response == "n":
            return
def practice(cards):
    still_learning.clear()
    game_logic(cards)


def run_app(cards):
    total = len(cards)
    # introduction
    print("\n Welcome to Flashcard Quiz!")
    print(f"   {total} cards to go. \n")
    print("Press Enter to see answer.")
    print("Type quit to exit.")
    print("-" * 40)


    game_logic(cards)


    print(understand)
    print(still_learning)


if __name__ == '__main__':
    run_app(flashcards)