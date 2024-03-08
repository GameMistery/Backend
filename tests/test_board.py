import unittest
from util.vector import Vector2d
from matches.match import Match
from users.user import User


class TestBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.match = Match('test_match', [User('user1'), User('user2')])

    def prepare_turn(self):
        dice_value = self.match.roll_dice()
        current_turn = self.match.current_turn()

        if current_turn.nickname != 'user1':
            self.match.move(self.match.board.get_player_position("user2"))
            self.match.next_turn()
            dice_value = self.match.roll_dice()

        return dice_value

    def skip_turn(self):
        self.match.roll_dice()
        self.match.move(self.match.board.get_player_position(self.match.current_turn().nickname))
        self.match.next_turn()

    def test_moves_right_distance(self):
        dice_value = self.prepare_turn()
        start_pos_p1 = Vector2d(0, 6)

        new_pos = Vector2d(start_pos_p1.x + dice_value, start_pos_p1.y)

        # Raises exception if something goes wrong
        self.match.move(new_pos)

    def test_cannot_move_more_than_dice_roll(self):
        self.prepare_turn()

        try:
            # Can't roll a 7
            self.match.move(Vector2d(7, 6))
        except Exception:
            return
        self.assertTrue(False, 'Player moved more than 6 spaces')

    def test_can_move_multiple_times_in_the_same_turn(self):
        self.prepare_turn()
        self.match._current_roll = 6

        try:
            self.match.move(Vector2d(1, 6))
            self.match.move(Vector2d(2, 6))
            self.match.move(Vector2d(3, 6))
            self.match.move(Vector2d(4, 6))
            self.match.move(Vector2d(5, 6))
            self.match.move(Vector2d(6, 6))
            self.match.next_turn()
        except Exception:
            self.assertTrue(False, 'Couldnt move multiple times in the same turn')

    def test_trap_skips_turn(self):
        self.prepare_turn()
        self.match._current_roll = 6

        self.match.move(Vector2d(6, 6))
        self.match.next_turn()
        self.skip_turn()

        self.assertEqual(self.match.current_turn().nickname, 'user2')

    def test_player_can_move_from_trap_to_trap(self):
        self.prepare_turn()
        self.match._current_roll = 6

        self.match.move(Vector2d(6, 6))
        self.match.next_turn()
        self.skip_turn()
        self.skip_turn()

        self.match.roll_dice()
        self.match.move(Vector2d(13, 13))

    def test_player_can_move_after_jumping_traps(self):
        self.prepare_turn()
        self.match._current_roll = 6

        self.match.move(Vector2d(6, 6))
        self.match.next_turn()
        self.skip_turn()
        self.skip_turn()

        self.match.roll_dice()
        self.match.move(Vector2d(13, 13))

        self.match.next_turn()
        self.skip_turn()

        self.match.roll_dice()
        self.match.move(Vector2d(14, 13))

    def test_cant_end_turn_if_not_moved(self):

        self.prepare_turn()

        try:
            self.match.roll_dice()
            self.match.next_turn()
            self.assertTrue(False, 'Player ended turn without moving')
        except:
            pass

    def test_cant_end_turn_if_not_rolled_dice_and_moved(self):

        self.prepare_turn()

        try:
            self.match.next_turn()
            self.assertTrue(False, 'Player ended turn without rolling the dice and moving')
        except:
            pass

    def test_cant_move_if_not_rolled_dice(self):

        self.prepare_turn()

        try:
            self.match.next_turn()
            self.assertTrue(False, 'Player moved without rolling the dice')
        except:
            pass

    def test_player_cant_move_more_than_roll(self):
        self.prepare_turn()
        self.match._current_roll = 6

        try:
            self.match.move(Vector2d(1, 6))
            self.match.move(Vector2d(2, 6))
            self.match.move(Vector2d(3, 6))
            self.match.move(Vector2d(4, 6))
            self.match.move(Vector2d(5, 6))
            self.match.move(Vector2d(6, 6))
            self.match.move(Vector2d(7, 6))
            self.match.next_turn()
        except Exception:
            return
        self.assertTrue(False, 'Player moved more than 6 times with a roll of 6')

    def test_player_can_jump_through_a_portal(self):
        self.prepare_turn()
        self.match._current_roll = 6

        try:
            self.match.move(Vector2d(4, 6))
            self.match.move(Vector2d(15, 6))
            self.assertEqual(self.match.board.get_player_position(self.match.current_turn().nickname), Vector2d(15, 6))
        except Exception:
            self.assertTrue(False, 'Exception raised while moving to a portal')

    def test_player_cant_jump_through_unmatching_portals(self):
        self.prepare_turn()
        self.match._current_roll = 6

        try:
            self.match.move(Vector2d(4, 6))
            self.match.move(Vector2d(3, 13))
            self.assertTrue(False)
        except AssertionError:
            self.assertTrue(False, 'Player moved through a portal of unmatching animals')
        except Exception:
            pass

