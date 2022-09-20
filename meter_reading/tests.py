"""
Unit testing for file_processor management command
"""
import os
import django.test
import django.core.management


class CommandTestCase(django.test.TestCase):
    def test_corrupted_file_exit(self):
        """Ensure that corrupted file as singular input raises exception"""
        with self.assertRaises(SystemExit) as cm:
            django.core.management.call_command(
                "file_processor",
                os.path.join(
                    "meter_reading/resources/flow_files/", "corrupted_flow_file.uff"
                ),
            )
        self.assertEqual(cm.exception.code, 1)

    def test_corrupted_directory_exit(self):
        """Ensure that a corrupted file in a directory of uncorrupted files oes not exit execution but continues with processing"""
        with self.assertRaises(SystemExit) as cm:
            django.core.management.call_command(
                "file_processor", "meter_reading/resources/flow_files/"
            )
        self.assertEqual(cm.exception.code, 0)
