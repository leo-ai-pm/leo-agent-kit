import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('leo', ROOT / 'leo.py')
leo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(leo)


class KitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def test_project_isolation_and_no_overwrite(self):
        a = leo.initialize(self.base, 'alpha'); b = leo.initialize(self.base, 'beta')
        self.assertTrue((a / 'kit.sh').is_file())
        self.assertFalse((b / 'projects' / 'alpha').exists())
        with self.assertRaises(ValueError): leo.initialize(self.base, 'alpha')

    def test_path_escape(self):
        for name in ['../escape', '/tmp/escape', '.', 'a/b', '']:
            with self.assertRaises(ValueError): leo.initialize(self.base, name)

    def test_handoff_requires_complete_pair(self):
        target = leo.initialize(self.base, 'demo')
        source = self.base / 'input'; source.mkdir()
        (source / 'PRD.md').write_text('Product requirements')
        with self.assertRaises(ValueError): leo.handoff(self.base, 'demo', source)
        self.assertFalse((target / 'projects/demo/docs/PRD/PRD.md').exists())
        (source / '方案.md').write_text('Architecture')
        result = leo.handoff(self.base, 'demo', source)
        self.assertEqual((result / 'PRD.md').read_text(), 'Product requirements')
        with self.assertRaises(ValueError): leo.handoff(self.base, 'demo', source)

    def test_real_delivery_task_and_gate(self):
        target = leo.initialize(self.base, 'demo')
        task = subprocess.run(['python3', str(ROOT / 'leo.py'), '--workspace', str(self.base),
                               'delivery', 'demo', 'task'], capture_output=True)
        self.assertEqual(task.returncode, 0, task.stderr)
        self.assertTrue((target / 'projects/demo/docs/本阶段任务.md').is_file())
        check = subprocess.run(['python3', str(ROOT / 'leo.py'), '--workspace', str(self.base),
                                'delivery', 'demo', 'check'], capture_output=True)
        self.assertNotEqual(check.returncode, 0)
        accept = subprocess.run(['python3', str(ROOT / 'leo.py'), '--workspace', str(self.base),
                                 'delivery', 'demo', 'accept'], capture_output=True)
        self.assertEqual(accept.returncode, 2)
