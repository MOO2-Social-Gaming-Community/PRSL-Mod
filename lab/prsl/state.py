from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, FrozenSet, Optional, Set, Tuple
import uuid
import math


class Phase(Enum):
    PLANNING = auto()
    PREPARE = auto()
    GRACE = auto()
    COMMITTED = auto()
    NATIVE_SUBMITTED = auto()
    RESOLUTION = auto()
    FAULT = auto()


@dataclass(frozen=True)
class Epoch:
    session_id: str
    load_generation: int
    turn: int
    membership_revision: int


@dataclass
class PlayerState:
    connected: bool = True
    ready: bool = False
    safe_to_commit: bool = False
    last_sequence: int = -1


@dataclass
class Coordinator:
    players: FrozenSet[str]
    epoch: Epoch
    grace_seconds: float = 3.0
    phase: Phase = Phase.PLANNING
    barrier_id: Optional[str] = None
    commit_id: Optional[str] = None
    grace_deadline: Optional[float] = None
    state: Dict[str, PlayerState] = field(default_factory=dict)
    native_submitted: Set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.players or any(not isinstance(p, str) or not p for p in self.players):
            raise ValueError("A nonempty roster of named players is required")
        if not math.isfinite(self.grace_seconds) or self.grace_seconds < 0:
            raise ValueError("Grace must be finite and nonnegative")
        self.state = {p: PlayerState() for p in self.players}

    def _validate(self, player: str, epoch: Epoch, sequence: int) -> bool:
        if player not in self.players or epoch != self.epoch:
            return False
        st = self.state[player]
        if not st.connected or type(sequence) is not int or sequence < 0 or sequence <= st.last_sequence:
            return False
        st.last_sequence = sequence
        return True

    def ready(self, player: str, epoch: Epoch, sequence: int) -> bool:
        if self.phase not in (Phase.PLANNING, Phase.PREPARE, Phase.GRACE):
            return False
        if not self._validate(player, epoch, sequence):
            return False
        # A fresh-sequence duplicate READY is idempotent. It must not silently
        # invalidate a PREPARE acknowledgement while leaving GRACE active.
        if self.state[player].ready:
            return True
        self.state[player].ready = True
        self.state[player].safe_to_commit = False
        self._recompute_barrier()
        return True

    def unready(self, player: str, epoch: Epoch, sequence: int) -> bool:
        # The cancellation boundary is coordinator acceptance before COMMITTED.
        if self.phase not in (Phase.PLANNING, Phase.PREPARE, Phase.GRACE):
            return False
        if not self._validate(player, epoch, sequence):
            return False
        self.state[player].ready = False
        self.state[player].safe_to_commit = False
        self.phase = Phase.PLANNING
        self.barrier_id = None
        self.grace_deadline = None
        for st in self.state.values():
            st.safe_to_commit = False
        return True

    def _recompute_barrier(self) -> None:
        if all(s.connected and s.ready for s in self.state.values()):
            if self.phase is Phase.PLANNING:
                self.phase = Phase.PREPARE
                self.barrier_id = str(uuid.uuid4())
        else:
            if self.phase in (Phase.PREPARE, Phase.GRACE):
                self.phase = Phase.PLANNING
                self.barrier_id = None
                self.grace_deadline = None
                for st in self.state.values():
                    st.safe_to_commit = False

    def prepared(self, player: str, epoch: Epoch, sequence: int, barrier_id: str) -> bool:
        if self.phase is not Phase.PREPARE or barrier_id != self.barrier_id:
            return False
        if not self._validate(player, epoch, sequence):
            return False
        if not self.state[player].ready:
            return False
        self.state[player].safe_to_commit = True
        return True

    def start_grace(self, now: float) -> bool:
        if self.phase is not Phase.PREPARE or not math.isfinite(now):
            return False
        if not all(s.connected and s.ready and s.safe_to_commit for s in self.state.values()):
            return False
        self.phase = Phase.GRACE
        self.grace_deadline = now + self.grace_seconds
        return True

    def tick(self, now: float) -> bool:
        if not math.isfinite(now):
            return False
        if self.phase is Phase.GRACE and not all(
                s.connected and s.ready and s.safe_to_commit for s in self.state.values()):
            self._cancel_barrier()
            return False
        if self.phase is Phase.GRACE and self.grace_deadline is not None and now >= self.grace_deadline:
            self.phase = Phase.COMMITTED
            self.commit_id = str(uuid.uuid4())
            self.grace_deadline = None
            return True
        return False

    def _cancel_barrier(self) -> None:
        self.phase = Phase.PLANNING
        self.barrier_id = None
        self.grace_deadline = None
        for state in self.state.values():
            state.safe_to_commit = False

    def disconnected(self, player: str) -> bool:
        """Transport observer only; not an unauthenticated wire-message API."""
        if player not in self.players:
            return False
        st = self.state[player]
        st.connected = st.ready = st.safe_to_commit = False
        if self.phase in (Phase.PLANNING, Phase.PREPARE, Phase.GRACE):
            self._cancel_barrier()
        else:
            # Never infer that a committed native turn can be rolled back.
            self.phase = Phase.FAULT
        return True

    def reconnected(self, player: str) -> bool:
        if player not in self.players or self.phase is not Phase.PLANNING:
            return False
        self.state[player].connected = True
        return True

    def native_submit_observed(self, player: str, commit_id: str) -> bool:
        if self.phase not in (Phase.COMMITTED, Phase.NATIVE_SUBMITTED):
            return False
        if commit_id != self.commit_id or player not in self.players:
            return False
        self.native_submitted.add(player)
        if self.native_submitted == set(self.players):
            self.phase = Phase.NATIVE_SUBMITTED
        return True

    def resolution_started(self) -> bool:
        if self.phase is not Phase.NATIVE_SUBMITTED:
            return False
        self.phase = Phase.RESOLUTION
        return True

    def next_turn(self, turn: int) -> bool:
        if self.phase is not Phase.RESOLUTION or turn <= self.epoch.turn:
            return False
        self.epoch = Epoch(
            session_id=self.epoch.session_id,
            load_generation=self.epoch.load_generation,
            turn=turn,
            membership_revision=self.epoch.membership_revision,
        )
        self.phase = Phase.PLANNING
        self.barrier_id = None
        self.commit_id = None
        self.grace_deadline = None
        self.native_submitted.clear()
        for st in self.state.values():
            st.ready = False
            st.safe_to_commit = False
            st.last_sequence = -1
        return True
