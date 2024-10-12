from django.test import TestCase
from .models import ReferenceObject, ReferenceRobot
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError

FILE_STORAGE_DIRECTORS = '../object_files/'

class AbstractReferenceTestCase(TestCase):
    def setUp(self):
        # Create test file
        self.test_file = SimpleUploadedFile("test.obj", b"file_content", content_type="text/plain")


    def test_file_upload_path(self):
        """
        Tests whether the file is saved in the correct directory
        """
        obj = ReferenceObject.objects.create(
            name="Test Object", file=self.test_file
        )
        self.assertTrue(obj.file.name.startswith(FILE_STORAGE_DIRECTORS))



    def test_file_type_is_set(self):
        """
        Ensures the file_type field is correctly set based on the file extension
        """
        # Test for ReferenceObject
        obj = ReferenceObject.objects.create(
            name="Test Object", file=self.test_file, color="red"
        )
        self.assertEqual(obj.file_type, 'obj')

        # Test for ReferenceRobot
        robot = ReferenceRobot.objects.create(
            name="Test Robot", file=self.test_file, num_joints=6
        )
        self.assertEqual(robot.file_type, 'obj')



    def test_name_is_required(self):
        """
        Tests that trying to create an instance without a name raises an IntegrityError
        """
        with self.assertRaises(IntegrityError):
            ReferenceObject.objects.create(file=self.test_file, color="red")



    def test_str_method_reference_object(self):
        """
        Validates that the string representation methods return the expected format
        """
        obj = ReferenceObject.objects.create(
            name="Test Object", file=self.test_file, color="red"
        )
        self.assertEqual(str(obj), "ReferenceObject: Test Object of type obj")



    def test_str_method_reference_robot(self):
        """
        Validates that the string representation methods return the expected format
        """
        robot = ReferenceRobot.objects.create(
            name="Test Robot", file=self.test_file, num_joints=6
        )
        self.assertEqual(str(robot), "ReferenceRobot: Test Robot of type obj")



    def test_optional_fields(self):
        """
        Ensures that optional fields can be left blank or null
        """
        # Test optional color field for ReferenceObject
        obj = ReferenceObject.objects.create(
            name="Test Object", file=self.test_file
        )
        self.assertIsNone(obj.color)

        # Test optional description field for AbstractReference
        obj = ReferenceObject.objects.create(
            name="Test Object", file=self.test_file
        )
        self.assertIsNone(obj.description)



    def test_description_can_be_blank(self):
        """
        Verifies that the description field can be left blank without causing errors
        """
        obj = ReferenceObject.objects.create(
            name="Test Object", file=self.test_file, description=""
        )
        self.assertEqual(obj.description, "")



    def test_updated_at_auto_updates(self):
        """
        Confirms that the updated_at field changes when an object is updated
        """
        obj = ReferenceObject.objects.create(
            name="Test Object", file=self.test_file, color="blue"
        )
        updated_at_initial = obj.updated_at
        obj.color = "green"
        obj.save()

        obj.refresh_from_db()
        self.assertNotEqual(updated_at_initial, obj.updated_at)



    def test_max_length_constraints(self):
        """
        Ensures fields with max_length respect the constraint.
        """
        long_name = "a" * 256
        with self.assertRaises(ValueError):
            ReferenceObject.objects.create(name=long_name, file=self.test_file)

        long_color = "a" * 17
        with self.assertRaises(ValueError):
            ReferenceObject.objects.create(name="Test", file=self.test_file, color=long_color)



    def test_num_joints_positive(self):
        """
        Ensures num_joints is a positive number
        """
        with self.assertRaises(ValueError):
            ReferenceRobot.objects.create(name="Test Robot", file=self.test_file, num_joints=-1)
        
        with self.assertRaises(ValueError):
            ReferenceRobot.objects.create(name="Test Robot", file=self.test_file, num_joints=0)


