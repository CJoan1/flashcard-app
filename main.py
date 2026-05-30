flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"question": "What is 12 x 12?", "answer": "144"},
    {"question": "What language runs in a web browser?", "answer": "JavaScript"},
    {"question": "What does RAM stand for?", "answer": "Random Access Memory"},
]

def run_app(cards):
	total = len(cards)
	# introduction
	print("\n Welcome to Flashcard Quiz!")
	print(f"   {total} cards to go. \n")
	print("Press Enter to see answer.")
	print("Type quit to exit.")
	print("-" * 40)

	for idx, card in enumerate(cards, start=1):
		# list what number we are on
		print(f" {idx} of total")
		question = card['question']
		answer = card['answer']
		print(question)
		option = input("").strip()
		if option == "":
			print(answer)
		if option == "quit":
			break

		print("-" * 40)

if __name__ == '__main__':
	run_app(flashcards)
# if __name__ == "__main__":
#     run_quiz(flashcards)
