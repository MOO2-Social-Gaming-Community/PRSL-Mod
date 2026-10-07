import io,stat,tempfile,unittest,zipfile
from pathlib import Path
from prsl.packages import safe_relative,safe_extract,dosbox_config,launch,PackageError

class PackageTests(unittest.TestCase):
    def setUp(self):self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name)
    def tearDown(self):self.t.cleanup()
    def archive(self,entries):
        p=self.root/'input.zip'
        with zipfile.ZipFile(p,'w') as z:
            for name,data in entries:z.writestr(name,data)
        return p
    def test_unsafe_paths_rejected(self):
        for s in ['../a','/a','a/../b','a\\b','C:/a','a\nb','a/./b','a//b','NUL','x.','x ','COM1.txt']:
            with self.subTest(s=s),self.assertRaises(PackageError):safe_relative(s)
    def test_case_collision_rejected(self):
        z=self.archive([('p/A.EXE',b'a'),('p/a.exe',b'b')])
        with self.assertRaises(PackageError):safe_extract(z,self.root/'out','p/')
    def test_symlink_rejected(self):
        i=zipfile.ZipInfo('p/link');i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16
        z=self.archive([(i,b'/tmp')])
        with self.assertRaises(PackageError):safe_extract(z,self.root/'out','p/')
    def test_size_limit(self):
        z=self.archive([('p/file',b'abcd')])
        with self.assertRaises(PackageError):safe_extract(z,self.root/'out','p/',max_bytes=3)
    def test_overwrite_refused(self):
        z=self.archive([('p/file',b'abcd')]);out=self.root/'out';out.mkdir();(out/'file').write_text('keep')
        with self.assertRaises(PackageError):safe_extract(z,out,'p/')
        self.assertEqual((out/'file').read_text(),'keep')
    def test_safe_extraction(self):
        z=self.archive([('p/dir/file',b'abcd')]);out=self.root/'out'
        self.assertEqual(safe_extract(z,out,'p/'),['dir/file']);self.assertEqual((out/'dir/file').read_bytes(),b'abcd')
    def test_host_configuration(self):
        s=dosbox_config(self.root/'game',role='host');self.assertIn('IPXNET STARTSERVER 21300',s)
        self.assertIn('ORION150.EXE',s);self.assertNotIn('PRSL.CFG',s)
    def test_join_configuration(self):
        self.assertIn('IPXNET CONNECT 192.168.1.2 21300',dosbox_config(self.root,role='join',host='192.168.1.2'))
    def test_join_injection_rejected(self):
        with self.assertRaises(PackageError):dosbox_config(self.root,role='join',host='1.2.3.4\nexit')
    def test_bad_port_rejected(self):
        for x in [1,65536,True]:
            with self.assertRaises(PackageError):dosbox_config(self.root,port=x)
    def test_prsl_launch_fails_closed_even_without_manifest(self):
        with self.assertRaisesRegex(PackageError,'not certified'):launch(self.root,Path('/fake/dosbox'),mode='prsl')
