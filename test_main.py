import unittest
from unittest.mock import patch
from main import sort_card, game_logic, offer_practice


class TestSortCard(unittest.TestCase):

    def test_correct_answer_goes_to_understand(self):
        card = {"question": "What is 2+2?", "answer": "4"}
        understand = []
        still_learning = []
        sort_card(card, understand, still_learning, "y")
        self.assertEqual(understand, [card])
        self.assertEqual(still_learning, [])

    def test_wrong_answer_goes_to_still_learning(self):
        card = {"question": "What is 2+2?", "answer": "4"}
        understand = []
        still_learning = []
        sort_card(card, understand, still_learning, "n")
        self.assertEqual(still_learning, [card])
        self.assertEqual(understand, [])

    def test_multiple_cards_accumulate(self):
        card1 = {"question": "Q1", "answer": "A1"}
        card2 = {"question": "Q2", "answer": "A2"}
        understand = []
        still_learning = []
        sort_card(card1, understand, still_learning, "y")
        sort_card(card2, understand, still_learning, "n")
        self.assertEqual(understand, [card1])
        self.assertEqual(still_learning, [card2])

    def test_invalid_input_sorts_nowhere(self):
        card = {"question": "Q1", "answer": "A1"}
        understand = []
        still_learning = []
        sort_card(card, understand, still_learning, "x")
        self.assertEqual(understand, [])
        self.assertEqual(still_learning, [])


class TestGameLogic(unittest.TestCase):

    @patch("builtins.input")
    def test_correct_answer_goes_to_understand(self, mock_input):
        # press enter, then "y"
        mock_input.side_effect = ["", "y"]
        cards = [{"question": "What is 2+2?", "answer": "4"}]
        understand, still_learning = game_logic(cards)
        self.assertEqual(understand, cards)
        self.assertEqual(still_learning, [])

    @patch("builtins.input")
    def test_wrong_answer_goes_to_still_learning(self, mock_input):
        # press enter, then "n"
        mock_input.side_effect = ["", "n"]
        cards = [{"question": "What is 2+2?", "answer": "4"}]
        understand, still_learning = game_logic(cards)
        self.assertEqual(still_learning, cards)
        self.assertEqual(understand, [])

    @patch("builtins.input")
    def test_quit_exits_early(self, mock_input):
        # type "quit" on first card
        mock_input.side_effect = ["quit"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ]
        understand, still_learning = game_logic(cards)
        self.assertEqual(understand, [])
        self.assertEqual(still_learning, [])

    @patch("builtins.input")
    def test_quit_after_sorting_some_cards(self, mock_input):
        # get first card right, quit on second
        mock_input.side_effect = ["", "y", "quit"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ]
        understand, still_learning = game_logic(cards)
        self.assertEqual(understand, [cards[0]])
        self.assertEqual(still_learning, [])

    @patch("builtins.input")
    def test_two_cards_mixed_results(self, mock_input):
        # first card right, second card wrong
        mock_input.side_effect = ["", "y", "", "n"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ]
        understand, still_learning = game_logic(cards)
        self.assertEqual(understand, [cards[0]])
        self.assertEqual(still_learning, [cards[1]])

    @patch("builtins.input")
    def test_all_cards_correct(self, mock_input):
        # press enter then "y" for each of 5 cards
        mock_input.side_effect = ["", "y", "", "y", "", "y", "", "y", "", "y"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
            {"question": "Q3", "answer": "A3"},
            {"question": "Q4", "answer": "A4"},
            {"question": "Q5", "answer": "A5"},
        ]
        understand, still_learning = game_logic(cards)
        self.assertEqual(understand, cards)
        self.assertEqual(still_learning, [])

    @patch("builtins.input")
    def test_all_cards_wrong(self, mock_input):
        # press enter then "n" for each of 5 cards
        mock_input.side_effect = ["", "n", "", "n", "", "n", "", "n", "", "n"]
        cards = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
            {"question": "Q3", "answer": "A3"},
            {"question": "Q4", "answer": "A4"},
            {"question": "Q5", "answer": "A5"},
        ]
        understand, still_learning = game_logic(cards)
        self.assertEqual(still_learning, cards)
        self.assertEqual(understand, [])


class TestOfferPractice(unittest.TestCase):

    @patch("builtins.input")
    def test_user_declines_practice(self, mock_input):
        # user says no
        mock_input.side_effect = ["n"]
        cards = [{"question": "Q1", "answer": "A1"}]
        # should return without error
        offer_practice(cards)

    @patch("builtins.input")
    def test_empty_cards_skips_prompt(self, mock_input):
        # no wrong cards — should never ask
        offer_practice([])
        mock_input.assert_not_called()

    @patch("builtins.input")
    def test_user_accepts_then_gets_all_correct(self, mock_input):
        # say yes, then get the card right in the practice round
        mock_input.side_effect = ["y", "", "y"]
        cards = [{"question": "Q1", "answer": "A1"}]
        # should complete without error and not loop again
        offer_practice(cards)


if __name__ == "__main__":
    unittest.main()