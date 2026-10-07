"""Laboratory-only x86 event gate; never an installable game patch.

Addresses belong to synthetic test images. There is no guest allocation,
engine-phase observer, UI lock, or live network adapter here.
"""
from __future__ import annotations
import struct
from .binary150 import CODE_BASE, DATA_BASE
GATE_BASE = 0x50000000
MAILBOX_BASE = 0x40000000
SITE, RESUME, DEFER, ASSERT = 0x76d78, 0x76d7d, 0x76d9e, 0xee8bd

def branch(opcode: bytes, address: int, target: int) -> bytes:
    return opcode + struct.pack('<i', target - (address + len(opcode) + 4))

def build_gate() -> bytes:
    out = bytearray()
    labels: dict[str, int] = {}
    fixups: list[tuple[int, str]] = []
    def emit(data: bytes) -> None: out.extend(data)
    def label(name: str) -> None: labels[name] = GATE_BASE + len(out)
    def jump(opcode: bytes, target: str) -> None:
        emit(opcode); fixups.append((len(out), target)); emit(b'\0'*4)
    def cmp_mem(address: int, value: int, byte: bool = False) -> None:
        emit((b'\x80\x3d' if byte else b'\x83\x3d') + struct.pack('<I', address) + bytes([value]))
    def store(address: int, value: int) -> None:
        emit(b'\xc7\x05' + struct.pack('<II', address, value))
    emit(b'\x9c') # PUSHFD; no general register is changed by the gate.
    cmp_mem(MAILBOX_BASE, 1); jump(b'\x0f\x85', 'bypass')
    cmp_mem(DATA_BASE + 0x21f3a, 2, True); jump(b'\x0f\x84', 'network')
    cmp_mem(DATA_BASE + 0x21f3a, 3, True); jump(b'\x0f\x85', 'bypass')
    label('network')
    cmp_mem(MAILBOX_BASE+8, 1); jump(b'\x0f\x85', 'defer')
    store(MAILBOX_BASE+8, 0) # Consume one laboratory permit.
    store(MAILBOX_BASE+4, 0)
    store(MAILBOX_BASE+12, 1)
    label('bypass')
    emit(b'\x9d')
    emit(branch(b'\xe8', GATE_BASE+len(out), CODE_BASE+ASSERT))
    emit(branch(b'\xe9', GATE_BASE+len(out), CODE_BASE+RESUME))
    label('defer')
    store(MAILBOX_BASE+4, 1)
    emit(b'\x9d')
    emit(branch(b'\xe9', GATE_BASE+len(out), CODE_BASE+DEFER))
    for offset, target in fixups:
        struct.pack_into('<i', out, offset, labels[target]-(GATE_BASE+offset+4))
    return bytes(out)
