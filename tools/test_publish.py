import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('publisher', Path(__file__).with_name('publish_approved.py'))
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)

class PackageTests(unittest.TestCase):
    def package(self, extra=None, license=True):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / 'addon.zip'
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('addons/test/addon.json', json.dumps({'title': 'Test', 'version': '1.0.0'}))
            if license:
                archive.writestr('addons/test/LICENSE.txt', 'Test fixture only')
            archive.writestr('addons/test/lua/init.lua', '-- never executed')
            for name, content in (extra or {}).items():
                info = zipfile.ZipInfo()
                info.filename = name
                archive.writestr(info, content)
        return path

    def test_valid_package_and_catalog_hash(self):
        path = self.package({'models/test/model.mdl': b'fixture'})
        entry = publisher.validate(path)
        self.assertEqual(entry['id'], 'test')
        self.assertEqual(entry['size_bytes'], path.stat().st_size)
        self.assertEqual(entry['sha256'], publisher.hashlib.sha256(path.read_bytes()).hexdigest())

    def test_unsafe_paths(self):
        for name in ('../evil.lua', '/evil.lua', 'addons/test/../evil.lua', 'addons/test/./evil.lua',
                     'addons//test/evil.lua', 'addons/test/CON.txt', 'addons/test/bad. ',
                     'addons/test/a\\b.lua', 'addons/test/C:evil.lua'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                publisher.validate(self.package({name: 'bad'}))

    def test_native_payload_and_overwrite(self):
        for name in ('addons/test/plugin.dll', 'config.cfg', 'models/other/model.mdl',
                     'addons/test/LICENSE.TXT', 'addons/other/addon.json'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                publisher.validate(self.package({name: '{}'}))

    def test_license_required(self):
        with self.assertRaises(ValueError):
            publisher.validate(self.package(license=False))

    def test_symlink_refused(self):
        path = self.package()
        with zipfile.ZipFile(path, 'a') as archive:
            info = zipfile.ZipInfo('addons/test/link.lua')
            info.create_system = 3
            info.external_attr = (0o120777 << 16)
            archive.writestr(info, '/outside')
        with self.assertRaises(ValueError):
            publisher.validate(path)

if __name__ == '__main__':
    unittest.main()

