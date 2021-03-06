import os
import sys
import shutil
import tarfile
import unittest

from oct.utilities.commands import main


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class UtilitiesTest(unittest.TestCase):

    def setUp(self):
        self.valid_dir = '/tmp/create-test'
        self.invalid_dir = '/create-test'
        self.test_dir = '/tmp/utiles_tests'
        self.template_path = os.path.join(BASE_DIR, 'fixtures', 'armory_sample_project.tar.gz')

        sys.argv = sys.argv[:1]
        sys.argv += ["new-project", self.test_dir]
        main()

    def test_create_success(self):
        """The newproject utility should be able to create a project
        """
        sys.argv = sys.argv[:1]
        sys.argv += ["new-project", self.valid_dir]
        main()

    def test_create_error(self):
        """The new project utility should corretly raise errors
        """
        sys.argv = sys.argv[:1]
        sys.argv += ["new-project", self.invalid_dir]
        with self.assertRaises(OSError):
            main()

    def test_create_from_template(self):
        """The new project utility should be able to create project from template
        """
        sys.argv = sys.argv[:1]
        sys.argv += ["new-project", self.valid_dir, "-t", self.template_path]
        main()

    def test_pack_success(self):
        """Should be able to generate turrets archives from project folder
        """
        sys.argv = sys.argv[:1]
        sys.argv += ["pack-turrets", self.test_dir]
        main()

        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'navigation.tar.gz')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'random.tar.gz')))

    def test_pack_python(self):
        """Pack command with --python args should create setup.py file
        """
        sys.argv = sys.argv[:1]
        sys.argv += ["pack-turrets", "--python", self.test_dir]
        main()

        tar = tarfile.open(self.test_dir + "/navigation.tar.gz", "r")
        self.assertIn('setup.py', tar.getnames())

    def test_pack_errors(self):
        """Pack function should correctly raise errors
        """
        with self.assertRaises(SystemExit):
            sys.argv = sys.argv[:1]
            sys.argv += ["pack-turrets", self.invalid_dir]
            main()

        sys.argv = sys.argv[:1]
        sys.argv += ["pack-turrets", self.test_dir]
        open(os.path.join(self.test_dir, 'navigation.tar.gz'), 'a').close()
        os.chmod(os.path.join(self.test_dir, 'navigation.tar.gz'), 0o444)

        with self.assertRaises(IOError):
            main()

        sys.argv = sys.argv[:1]
        sys.argv += ["pack-turrets", self.test_dir]
        os.chmod(self.test_dir, 0o444)

        with self.assertRaises(IOError):
            main()

        os.chmod(self.test_dir, 0o777)

    def tearDown(self):
        if os.path.exists(self.valid_dir):
            shutil.rmtree(self.valid_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
