"""Fail-closed structural mapper for the exact uploaded English 1.50.26 binary.

Object offsets are NOT runtime addresses. The laboratory relocation model does
not execute DOS/4GW, the community extension's initializer, or a game session.
"""
from __future__ import annotations
import hashlib
import re
import struct
from dataclasses import dataclass
from pathlib import Path

ENGINE_SHA256 = "2db296e052419250d21866f7c23ac2978a33b3c05b451a9516f06599b91c3f5c"
PATCH_SHA256 = "0ac9151e9cf752ec34b6db998d8b390f48e492d8443e8f1658112b93c7f6a921"
BASE_ZIP_SHA256 = "87e657bc2e8b02714856f13c3c63066cd58549f33a9c2e917d1bca6936142d2b"
BASE_ENGINE_SHA256 = "4e11be14217b4aafa1839f333bf5eba037f98b0c44e9e4752c96c464c260419f"
EXT_HEADER = 0x285B6A
CODE_BASE, DATA_BASE, EXT_PAYLOAD_BASE = 0x10000000, 0x20000000, 0x30000000

class UnsupportedBinary(ValueError):
    pass

@dataclass(frozen=True)
class Object:
    size: int
    base: int
    flags: int
    first_page: int
    page_count: int
    reserved: int

class Image150:
    def __init__(self, data: bytes):
        if hashlib.sha256(data).hexdigest() != ENGINE_SHA256:
            raise UnsupportedBinary("Not the pinned 1.50.26 executable; no patch permitted")
        self.raw = data
        candidates = []
        for m in re.finditer(b"MZ", data[:0x30000]):
            p = m.start()
            q = p + struct.unpack_from("<I", data, p + 0x3c)[0]
            if data[q:q+4] == b"LE\0\0":
                candidates.append((p, q))
        if len(candidates) != 1:
            raise UnsupportedBinary("Ambiguous bound LE image")
        self.bound_mz, self.le = candidates[0]
        self.page_size = self.u32(0x28)
        self.page_count = self.u32(0x14)
        self.page_origin = self.bound_mz + self.u32(0x80)
        self.objects = [Object(*struct.unpack_from("<6I", data, self.le + self.u32(0x40) + i*24))
                        for i in range(self.u32(0x44))]
        if self.page_size != 4096 or len(self.objects) != 2:
            raise UnsupportedBinary("Unexpected object layout")
        pm = self.le + self.u32(0x48)
        self.pages = [(int.from_bytes(data[pm+i*4:pm+i*4+3], "big"), data[pm+i*4+3])
                      for i in range(self.page_count)]
        if any(flag != 0 for _, flag in self.pages):
            raise UnsupportedBinary("Unsupported LE page encoding")
        self.extension_size, self.relocation_start, self.extension_code_start = struct.unpack_from("<III", data, EXT_HEADER)
        self.extension = data[EXT_HEADER+12:]
        if len(self.extension) != self.extension_size:
            raise UnsupportedBinary("Extension length mismatch")
        if (self.extension_code_start-self.relocation_start) % 11:
            raise UnsupportedBinary("Extension relocation table misaligned")
        self.le_relocations = self._le_relocations()
        self.extension_relocations = self._extension_relocations()

    @classmethod
    def read(cls, path: str | Path) -> "Image150":
        return cls(Path(path).read_bytes())

    def u32(self, offset: int) -> int:
        return struct.unpack_from("<I", self.raw, self.le+offset)[0]

    def file_offset(self, object_number: int, offset: int) -> int:
        obj = self.objects[object_number-1]
        if offset < 0 or offset >= obj.size:
            raise ValueError("Outside object")
        page = offset // self.page_size
        if page >= obj.page_count:
            raise ValueError("Uninitialized memory has no file offset")
        physical, flag = self.pages[obj.first_page-1+page]
        if flag or physical == 0:
            raise ValueError("Non-file-backed page")
        return self.page_origin+(physical-1)*self.page_size+offset % self.page_size

    def object_bytes(self, object_number: int) -> bytearray:
        obj = self.objects[object_number-1]
        result = bytearray(max(obj.size, obj.page_count*self.page_size))
        for p in range(obj.page_count):
            physical, flag = self.pages[obj.first_page-1+p]
            if flag:
                raise ValueError("Unsupported page flag")
            n = self.page_size
            # LE's final physical page is short; never import adjacent debug bytes.
            if physical == self.page_count:
                n = self.u32(0x2c) or self.page_size
            source = self.page_origin+(physical-1)*self.page_size
            result[p*self.page_size:p*self.page_size+n] = self.raw[source:source+n]
        return result

    def code(self, offset: int, length: int) -> bytes:
        p = self.file_offset(1, offset)
        return self.raw[p:p+length]

    def symbol(self, name: str) -> dict:
        needle = name.encode("ascii")
        records = []
        for m in re.finditer(re.escape(needle), self.raw):
            i = m.start()
            if i < 10:
                continue
            a, obj, module, kind, n = struct.unpack_from("<IHHBB", self.raw, i-10)
            if obj in (1, 2) and n == len(needle) and kind in (2, 3, 4, 5):
                records.append(dict(name=name, object=obj, offset=a, module=module,
                                    kind=kind, debug_record_file_offset=i-10))
        if len(records) != 1:
            raise ValueError(f"Expected one exact debug record for {name}: {len(records)}")
        record = records[0]
        try:
            record["file_offset"] = self.file_offset(record["object"], record["offset"])
        except ValueError:
            record["file_offset"] = None
        return record

    def _le_relocations(self) -> list[dict]:
        fpt = self.le+self.u32(0x68)
        frt = self.le+self.u32(0x6c)
        result = []
        for page in range(self.page_count):
            lo, hi = struct.unpack_from("<II", self.raw, fpt+page*4)
            cursor, end = frt+lo, frt+hi
            while cursor < end:
                origin = cursor
                st, flags = self.raw[cursor:cursor+2]
                if st != 7 or flags not in (0, 16):
                    raise UnsupportedBinary("Unrecognized LE relocation; refusing partial parse")
                source = struct.unpack_from("<h", self.raw, cursor+2)[0]
                target_object = self.raw[cursor+4]
                width = 4 if flags == 16 else 2
                target = int.from_bytes(self.raw[cursor+5:cursor+5+width], "little")
                source_page = page*self.page_size+source
                owner = next((i for i, o in enumerate(self.objects, 1)
                              if (o.first_page-1)*self.page_size <= source_page <
                              (o.first_page-1+o.page_count)*self.page_size), None)
                if owner is None or target_object not in (1, 2):
                    raise UnsupportedBinary("Relocation outside known objects")
                source_offset = source_page-(self.objects[owner-1].first_page-1)*self.page_size
                result.append(dict(source_object=owner, source_offset=source_offset,
                                   target_object=target_object, target_offset=target,
                                   record_file_offset=origin))
                cursor += 5+width
            if cursor != end:
                raise UnsupportedBinary("LE relocation block length mismatch")
        return result

    def _extension_relocations(self) -> list[dict]:
        result = []
        for off in range(self.relocation_start, self.extension_code_start, 11):
            relative, source_segment, target_segment, source, target = struct.unpack_from("<BBBII", self.extension, off)
            if relative not in (0, 1) or source_segment not in range(3) or target_segment not in range(3):
                raise UnsupportedBinary("Unsupported community extension relocation")
            result.append(dict(relative=relative, source_segment=source_segment,
                               target_segment=target_segment, source_offset=source,
                               target_offset=target, record_file_offset=EXT_HEADER+12+off))
        return result

    def lab_images(self, apply_extension: bool = True) -> tuple[bytearray, bytearray, bytearray]:
        """Synthetic flat-address test images, NOT runnable DOS installations."""
        code, data, extension = self.object_bytes(1), self.object_bytes(2), bytearray(self.extension)
        objects = {1: code, 2: data}
        bases = {1: CODE_BASE, 2: DATA_BASE}
        for r in self.le_relocations:
            struct.pack_into("<I", objects[r["source_object"]], r["source_offset"],
                             bases[r["target_object"]]+r["target_offset"])
        if apply_extension:
            segment_images = {0: extension, 1: data, 2: code}
            origins = {0: self.extension_code_start, 1: 0, 2: 0}
            bases = {0: EXT_PAYLOAD_BASE+self.extension_code_start, 1: DATA_BASE, 2: CODE_BASE}
            for r in self.extension_relocations:
                s, t, off = r["source_segment"], r["target_segment"], r["source_offset"]
                value = bases[t]+r["target_offset"]
                if r["relative"]:
                    value -= bases[s]+off
                struct.pack_into("<I", segment_images[s], origins[s]+off, value & 0xffffffff)
        return code, data, extension

    def target_map(self) -> dict:
        names = ["Human_Hit_Next_Turn_", "Do_Next_Turn_", "Main_Screen_", "Net_Next_Turn_",
                 "Host_Next_Turn_", "Client_Next_Turn_", "Chat_Box_Input_Loop_",
                 "Screen_Control_", "Assert_Settings_", "_current_screen", "_game_type", "_next_turn_hit",
                 "_next_button", "_skip_fields", "_random_seed"]
        symbols = [self.symbol(n) for n in names]
        return dict(schema=1, engine_sha256=ENGINE_SHA256, bound_mz=self.bound_mz, le_header=self.le,
                    code_file_origin=self.page_origin, le_relocation_count=len(self.le_relocations),
                    extension_relocation_count=len(self.extension_relocations),
                    symbols=symbols,
                    reader=dict(object=1, offset=0xea5a3, file_offset=self.file_offset(1,0xea5a3),
                                bytes=self.code(0xea5a3,7).hex(), flag_object=2, flag_offset=0x32f7e,
                                input="EAX player index", output="AL; upper EAX unchanged"),
                    candidate=dict(object=1, offset=0x76d78, file_offset=self.file_offset(1,0x76d78),
                                   original_bytes=self.code(0x76d78,5).hex(), defer_to=0x76d9e,
                                   allow_call=0xee8bd, allow_resume=0x76d7d,
                                   status="isolated-machine-code-tested; NOT full-game-certified"),
                    secondary_candidate=dict(offset=0x73411, file_offset=self.file_offset(1,0x73411),
                                             bytes=self.code(0x73411,5).hex(),
                                             limitation="Manual caller has already written native UI/turn-intent flags"),
                    main_event=dict(condition_block=0x76d62, turn_field=self.symbol("_next_button"),
                                    guard=self.symbol("_skip_fields"), native_call=0x76d99,
                                    other_direct_call=0x7af19,
                                    caller_exit_flag="16-bit stack local passed via EAX; do not persist its address"),
                    native_submission=dict(function=0xec470, done_flag_write=0xec51e,
                                           network_message_send_call=0xec584, dispatch_call=0x753,
                                           extension_wrapper_offset=0x4ef2,
                                           wrapper_preserves=dict(symbol=self.symbol("_random_seed"),
                                                                  extension_snapshot_offset=0x4eee)),
                    capabilities=dict(native_game_integration=False, all_input_paths=False,
                                      locked_pre_ready_ui=False, automatic_commit_in_game=False))
