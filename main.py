flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"question": "What is 12 x 12?", "answer": "144"},
    {"question": "What language runs in a web browser?", "answer": "JavaScript"},
    {"question": "What does RAM stand for?", "answer": "Random Access Memory"},
]

def run_app(cards):
	total = len(cards)
	understand = []
	still_learning = []
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
			sort = input("Did you get it right? y/n:").strip().lower()
			if sort == "y":
				understand.append(card)
			if sort == "n":
				still_learning.append(card)
		if option == "quit":
			break

		print("-" * 40)
	print(understand)
	print(still_learning)
if __name__ == '__main__':
	run_app(flashcards)










# # Flashcard App - Week 1
# # A simple CLI flashcard quiz

# flashcards = [
#     {"question": "What is the capital of France?", "answer": "Paris"},
#     {"question": "What does CPU stand for?", "answer": "Central Processing Unit"},
#     {"question": "What is 12 x 12?", "answer": "144"},
#     {"question": "What language runs in a web browser?", "answer": "JavaScript"},
#     {"question": "What does RAM stand for?", "answer": "Random Access Memory"},
# ]

# def run_quiz(cards):
#     score = 0
#     total = len(cards)

#     print("\n🃏 Welcome to Flashcard Quiz!")
#     print(f"   {total} cards to go. Type your answer and press Enter.\n")
#     print("-" * 40)

#     for i, card in enumerate(cards, start=1):
#         print(f"\nCard {i} of {total}")
#         print(f"Q: {card['question']}")
#         input("   (Press Enter to see the answer...)")
#         print(f"A: {card['answer']}")

#         response = input("   Did you get it right? (y/n): ").strip().lower()
#         if response == "y":
#             score += 1
#             print("   ✅ Nice!")
#         else:
#             print("   ❌ Better luck next time.")

#         print("-" * 40)

#     print(f"\n📊 Quiz complete! You got {score}/{total} correct.")
#     if score == total:
#         print("   🏆 Perfect score!")
#     elif score >= total * 0.7:
#         print("   👍 Good job!")
#     else:
#         print("   📚 Keep studying — you'll get there!")

# if __name__ == "__main__":
#     run_quiz(flashcards)
