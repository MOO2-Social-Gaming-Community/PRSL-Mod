import unittest
from prsl.state import Coordinator, Epoch, Phase

class StateRegressions(unittest.TestCase):
    def setUp(self):
        self.e=Epoch('test',1,87,1)
        self.c=Coordinator(frozenset({'a','b'}),self.e,grace_seconds=1)
    def grace(self):
        for p in self.c.players: self.c.ready(p,self.e,1)
        for p in self.c.players: self.c.prepared(p,self.e,2,self.c.barrier_id)
        self.assertTrue(self.c.start_grace(10))
    def test_fresh_sequence_duplicate_ready_during_grace_is_idempotent(self):
        self.grace(); barrier=self.c.barrier_id
        self.assertTrue(self.c.ready('a',self.e,3))
        self.assertTrue(self.c.state['a'].safe_to_commit)
        self.assertEqual(barrier,self.c.barrier_id)
        self.assertTrue(self.c.tick(11))
    def test_tick_revalidates_safety(self):
        self.grace(); self.c.state['a'].safe_to_commit=False
        self.assertFalse(self.c.tick(11));self.assertEqual(self.c.phase,Phase.PLANNING)
    def test_disconnect_during_grace_cancels(self):
        self.grace();self.c.disconnected('a')
        self.assertFalse(self.c.tick(100));self.assertFalse(self.c.ready('a',self.e,3))
    def test_reconnect_requires_fresh_ready_and_prepare(self):
        self.grace();self.c.disconnected('a');self.c.reconnected('a')
        self.assertFalse(self.c.state['a'].ready)
        self.assertTrue(self.c.ready('a',self.e,3))
        self.assertEqual(self.c.phase,Phase.PREPARE)
        self.assertFalse(self.c.start_grace(100))
    def test_disconnect_after_commit_faults_instead_of_rollback(self):
        self.grace();self.c.tick(11);self.c.disconnected('a')
        self.assertEqual(self.c.phase,Phase.FAULT)
        self.assertFalse(self.c.unready('b',self.e,3))
        self.assertFalse(self.c.next_turn(88))
    def test_empty_roster_rejected(self):
        with self.assertRaises(ValueError): Coordinator(frozenset(),self.e)
    def test_invalid_grace_rejected(self):
        for n in [-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):Coordinator(frozenset({'a'}),self.e,grace_seconds=n)
    def test_invalid_clock_cannot_commit(self):
        self.grace()
        for n in [float('nan'),float('inf')]:self.assertFalse(self.c.tick(n))
    def test_reloaded_same_turn_rejects_old_epoch(self):
        old=Epoch('test',0,87,1)
        self.assertFalse(self.c.ready('a',old,999))
    def test_commit_is_not_native_observation(self):
        self.grace();self.c.tick(11)
        self.assertFalse(self.c.resolution_started())
        self.assertFalse(self.c.native_submit_observed('a','wrong-id'))
    def test_bad_sequence_rejected(self):
        for seq in [True,-1,'5',0.5]:self.assertFalse(self.c.ready('a',self.e,seq))
