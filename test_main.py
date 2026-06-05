import unittest
from unittest.mock import patch
from main import sort_card, game_logic, offer_practice, UNDERSTAND, STILL_LEARNING


class TestSortCard(unittest.TestCase):
    """
    Tests for sort_card() — verifies cards are placed into the
    correct list based on the sort value passed in.
    """

    def test_correct_answer_goes_to_understand(self):
        # a card sorted with UNDERSTAND should appear in understand only
        card = {"question": "What is 2+2?", "answer": "4"}
        understand = []
        still_learning = []
        sort_card(card, understand, still_learning, UNDERSTAND)
        self.assertEqual(understand, [card])
        self.assertEqual(still_learning, [])

    def test_wrong_answer_goes_to_still_learning(self):
        # a card sorted with STILL_LEARNING should appear in still_learning only
        card = {"question": "What is 2+2?", "answer": "4"}
        understand = []
        still_learning = []
        sort_card(card, understand, still_learning, STILL_LEARNING)
        self.assertEqual(still_learning, [card])
        self.assertEqual(understand, [])

    def test_multiple_cards_accumulate(self):
        # cards should accumulate across multiple calls — lists should not reset
        card1 = {"question": "Q1", "answer": "A1"}
        card2 = {"question": "Q2", "answer": "A2"}
        understand = []
        still_learning = []
        sort_card(card1, understand, still_learning, UNDERSTAND)
        sort_card(card2, understand, still_learning, STILL_LEARNING)
        self.assertEqual(understand, [card1])
        self.assertEqual(still_learning, [card2])

    def test_invalid_input_sorts_nowhere(self):
        # an unrecognised sort value should leave both lists empty
        card = {"question": "Q1", "answer": "A1"}
        understand = []
        still_learning = []
        sort_card(card, understand, still_learning, "x")
        self.assertEqual(understand, [])
        self.assertEqual(still_learning, [])


class TestGameLogic(unittest.TestCase):
    """
    Tests for game_logic() — verifies the quiz loop correctly sorts
    cards, handles quit, and returns the right flags.

    game_logic() returns: (understand, still_learning, quit_early)
    All side_effect values simulate direct typed input from the user.
    """

    @patch("builtins.input")
    def test_correct_answer_goes_to_understand(self, mock_input):
        # typing the correct answer should sort the card to understand
        mock_input.side_effect = ["4"]
        cards = [{"question": "What is 2+2?", "answer": "4"}]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertEqual(understand, cards)
        self.assertEqual(still_learning, [])

    @patch("builtins.input")
    def test_wrong_answer_goes_to_still_learning(self, mock_input):
        # typing an incorrect answer should sort the card to still_learning
        mock_input.side_effect = ["wrong"]
        cards = [{"question": "What is 2+2?", "answer": "4"}]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertEqual(still_learning, cards)
        self.assertEqual(understand, [])

    @patch("builtins.input")
    def test_quit_exits_early(self, mock_input):
        # typing quit on the first card should exit with empty lists
        mock_input.side_effect = ["quit"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertEqual(understand, [])
        self.assertEqual(still_learning, [])

    @patch("builtins.input")
    def test_quit_after_sorting_some_cards(self, mock_input):
        # quitting after one card should preserve whatever was already sorted
        mock_input.side_effect = ["A1", "quit"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertEqual(understand, [cards[0]])
        self.assertEqual(still_learning, [])

    @patch("builtins.input")
    def test_two_cards_mixed_results(self, mock_input):
        # first card correct, second card wrong — one in each list
        mock_input.side_effect = ["A1", "wrong"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertEqual(understand, [cards[0]])
        self.assertEqual(still_learning, [cards[1]])

    @patch("builtins.input")
    def test_all_cards_correct(self, mock_input):
        # all correct answers should fill understand and leave still_learning empty
        mock_input.side_effect = ["A1", "A2", "A3", "A4", "A5"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
            {"question": "Q3", "answer": "A3"},
            {"question": "Q4", "answer": "A4"},
            {"question": "Q5", "answer": "A5"},
        ]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertEqual(understand, cards)
        self.assertEqual(still_learning, [])

    @patch("builtins.input")
    def test_all_cards_wrong(self, mock_input):
        # all wrong answers should fill still_learning and leave understand empty
        mock_input.side_effect = ["wrong", "wrong", "wrong", "wrong", "wrong"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
            {"question": "Q3", "answer": "A3"},
            {"question": "Q4", "answer": "A4"},
            {"question": "Q5", "answer": "A5"},
        ]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertEqual(still_learning, cards)
        self.assertEqual(understand, [])

    @patch("builtins.input")
    def test_quit_returns_quit_early_flag(self, mock_input):
        # quit_early flag should be True when user types quit
        mock_input.side_effect = ["quit"]
        cards = [{"question": "Q1", "answer": "A1"}]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertTrue(quit_early)

    @patch("builtins.input")
    def test_finish_returns_finished_flag(self, mock_input):
        # quit_early flag should be False when quiz completes normally
        mock_input.side_effect = ["A1"]
        cards = [{"question": "Q1", "answer": "A1"}]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertFalse(quit_early)

    @patch("builtins.input")
    def test_hint_penalty_sorts_to_still_learning(self, mock_input):
        # using a hint then answering correctly should still sort to still_learning
        # uses "Paris" (5 letters) so max_hints = min(3, 4) = 3 — hints are available
        mock_input.side_effect = ["hint", "paris"]
        cards = [{"question": "What is the capital of France?", "answer": "Paris"}]
        understand, still_learning, quit_early = game_logic(cards)
        self.assertEqual(still_learning, cards)
        self.assertEqual(understand, [])


class TestOfferPractice(unittest.TestCase):
    """
    Tests for offer_practice() — verifies practice rounds are offered
    correctly and the function handles all exit paths cleanly.

    offer_practice(cards, total_understand, total)
    - cards: wrong cards to practice
    - total_understand: cumulative correctly answered cards
    - total: total number of cards in the original deck
    """

    @patch("builtins.input")
    def test_user_declines_practice(self, mock_input):
        # saying "n" should exit cleanly without running game_logic
        mock_input.side_effect = ["n"]
        cards = [{"question": "Q1", "answer": "A1"}]
        offer_practice(cards, [], 5)

    @patch("builtins.input")
    def test_empty_cards_skips_prompt(self, mock_input):
        # if there are no wrong cards the prompt should never appear
        offer_practice([], [], 5)
        mock_input.assert_not_called()

    @patch("builtins.input")
    def test_user_accepts_then_gets_all_correct(self, mock_input):
        # say yes to practice, no to shuffle, then answer correctly
        # after all cards are mastered the loop should stop naturally
        mock_input.side_effect = ["y", "n", "A1"]
        cards = [{"question": "Q1", "answer": "A1"}]
        offer_practice(cards, [], 5)

if __name__ == "__main__":
    unittest.main()