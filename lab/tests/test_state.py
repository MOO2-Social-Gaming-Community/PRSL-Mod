import unittest
from prsl.state import Coordinator, Epoch, Phase


class TestPRSL(unittest.TestCase):
    def setUp(self):
        self.epoch = Epoch('session-A', 0, 87, 1)
        self.c = Coordinator(frozenset({'psyche', 'carl'}), self.epoch, grace_seconds=3)

    def test_ready_is_reversible_before_commit(self):
        self.assertTrue(self.c.ready('psyche', self.epoch, 1))
        self.assertEqual(self.c.phase, Phase.PLANNING)
        self.assertTrue(self.c.unready('psyche', self.epoch, 2))
        self.assertFalse(self.c.state['psyche'].ready)

    def test_all_ready_enters_prepare_not_native_commit(self):
        self.c.ready('psyche', self.epoch, 1)
        self.c.ready('carl', self.epoch, 1)
        self.assertEqual(self.c.phase, Phase.PREPARE)
        self.assertIsNotNone(self.c.barrier_id)
        self.assertIsNone(self.c.commit_id)

    def test_prepare_grace_commit(self):
        self.c.ready('psyche', self.epoch, 1)
        self.c.ready('carl', self.epoch, 1)
        b = self.c.barrier_id
        self.assertTrue(self.c.prepared('psyche', self.epoch, 2, b))
        self.assertTrue(self.c.prepared('carl', self.epoch, 2, b))
        self.assertTrue(self.c.start_grace(100.0))
        self.assertEqual(self.c.phase, Phase.GRACE)
        self.assertFalse(self.c.tick(102.99))
        self.assertTrue(self.c.tick(103.0))
        self.assertEqual(self.c.phase, Phase.COMMITTED)

    def test_unready_during_grace_cancels(self):
        self.c.ready('psyche', self.epoch, 1)
        self.c.ready('carl', self.epoch, 1)
        b = self.c.barrier_id
        self.c.prepared('psyche', self.epoch, 2, b)
        self.c.prepared('carl', self.epoch, 2, b)
        self.c.start_grace(10)
        self.assertTrue(self.c.unready('psyche', self.epoch, 3))
        self.assertEqual(self.c.phase, Phase.PLANNING)
        self.assertFalse(self.c.tick(999))

    def test_unready_after_commit_is_rejected(self):
        self.c.ready('psyche', self.epoch, 1)
        self.c.ready('carl', self.epoch, 1)
        b = self.c.barrier_id
        self.c.prepared('psyche', self.epoch, 2, b)
        self.c.prepared('carl', self.epoch, 2, b)
        self.c.start_grace(10)
        self.c.tick(13)
        self.assertFalse(self.c.unready('psyche', self.epoch, 3))

    def test_stale_epoch_rejected(self):
        stale = Epoch('session-A', 0, 86, 1)
        self.assertFalse(self.c.ready('psyche', stale, 1))

    def test_duplicate_sequence_rejected(self):
        self.assertTrue(self.c.ready('psyche', self.epoch, 5))
        self.assertFalse(self.c.unready('psyche', self.epoch, 5))
        self.assertFalse(self.c.ready('psyche', self.epoch, 4))

    def test_wrong_barrier_ack_rejected(self):
        self.c.ready('psyche', self.epoch, 1)
        self.c.ready('carl', self.epoch, 1)
        self.assertFalse(self.c.prepared('psyche', self.epoch, 2, 'old-barrier'))

    def test_native_submission_is_observed_not_assumed(self):
        self.c.ready('psyche', self.epoch, 1)
        self.c.ready('carl', self.epoch, 1)
        b = self.c.barrier_id
        self.c.prepared('psyche', self.epoch, 2, b)
        self.c.prepared('carl', self.epoch, 2, b)
        self.c.start_grace(10)
        self.c.tick(13)
        commit = self.c.commit_id
        self.assertTrue(self.c.native_submit_observed('psyche', commit))
        self.assertEqual(self.c.phase, Phase.COMMITTED)
        self.assertTrue(self.c.native_submit_observed('carl', commit))
        self.assertEqual(self.c.phase, Phase.NATIVE_SUBMITTED)

    def test_next_turn_resets_barrier_state(self):
        self.c.ready('psyche', self.epoch, 1)
        self.c.ready('carl', self.epoch, 1)
        b = self.c.barrier_id
        self.c.prepared('psyche', self.epoch, 2, b)
        self.c.prepared('carl', self.epoch, 2, b)
        self.c.start_grace(10)
        self.c.tick(13)
        k = self.c.commit_id
        self.c.native_submit_observed('psyche', k)
        self.c.native_submit_observed('carl', k)
        self.assertTrue(self.c.resolution_started())
        self.assertTrue(self.c.next_turn(88))
        self.assertEqual(self.c.phase, Phase.PLANNING)
        self.assertEqual(self.c.epoch.turn, 88)
        self.assertTrue(all(not s.ready for s in self.c.state.values()))

if __name__ == '__main__':
    unittest.main()
