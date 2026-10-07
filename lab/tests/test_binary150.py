"""Optional fixture tests: set MOO2_ENGINE to your exact owned ORION150.EXE."""
import hashlib,os,struct,unittest
from pathlib import Path
from prsl.binary150 import Image150,UnsupportedBinary,CODE_BASE,DATA_BASE,EXT_PAYLOAD_BASE
ENGINE=os.environ.get('MOO2_ENGINE')

class BinaryRefusal(unittest.TestCase):
    def test_wrong_engine_refused_before_parsing(self):
        with self.assertRaises(UnsupportedBinary):Image150(b'MZ'+bytes(100))

@unittest.skipUnless(ENGINE,'Set MOO2_ENGINE for owned-executable structural tests')
class ExactBinaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.image=Image150.read(Path(ENGINE))
    def test_actual_symbol_record(self):
        s=self.image.symbol('Human_Hit_Next_Turn_')
        self.assertEqual((s['object'],s['offset'],s['file_offset']),(1,0xea5a3,0x17fc37))
    def test_actual_getter_instructions(self):self.assertEqual(self.image.code(0xea5a3,7).hex(),'8a807e2f0300c3')
    def test_manual_gate_original_instruction(self):self.assertEqual(self.image.code(0x76d78,5).hex(),'e8407b0700')
    def test_no_relocation_overwrites_gate(self):
        a,b=0x76d78,0x76d7d
        for r in self.image.le_relocations:
            self.assertFalse(r['source_object']==1 and r['source_offset']<b and r['source_offset']+4>a)
        for r in self.image.extension_relocations:
            self.assertFalse(r['source_segment']==2 and r['source_offset']<b and r['source_offset']+4>a)
    def test_manual_and_automatic_call_sites(self):
        for site in [0x76d99,0x7af19]:
            code=self.image.code(site,5)
            self.assertEqual(code[0],0xe8)
            self.assertEqual(site+5+struct.unpack('<i',code[1:])[0],0x73411)
    def test_relocation_counts(self):
        self.assertEqual(len(self.image.le_relocations),51363)
        self.assertEqual(len(self.image.extension_relocations),24655)
    def test_wrapper_preserved_not_bypassed(self):
        c,d,x=self.image.lab_images(True)
        target=CODE_BASE+0x758+struct.unpack_from('<i',c,0x754)[0]
        self.assertEqual(target,EXT_PAYLOAD_BASE+self.image.extension_code_start+0x4ef2)
        tail=self.image.extension_code_start+0x4efe
        self.assertEqual(x[tail],0xe9)
        destination=EXT_PAYLOAD_BASE+tail+5+struct.unpack_from('<i',x,tail+1)[0]
        self.assertEqual(destination,CODE_BASE+0xec470)
    def test_native_done_flag_is_data_object_reference(self):
        c,d,x=self.image.lab_images(True)
        self.assertEqual(struct.unpack_from('<I',c,0xea5a5)[0],DATA_BASE+0x32f7e)
    def test_no_certified_capability(self):
        self.assertFalse(self.image.target_map()['capabilities']['native_game_integration'])
