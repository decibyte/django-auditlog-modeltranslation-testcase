from django.test import TestCase

from . import models

class MyModelTestCase(TestCase):
    """Tests for MyModel."""

    def setUp(self):
        """Set up initial data."""
        self.instance1 = models.MyModel.objects.create(
            title='Title of Instance 1',
            text='Text of Instance 1'
        )
        self.instance2 = models.MyModel.objects.create(
            title='Title of Instance 2',
            text='Text of Instance 2'
        )

    def test_my_model(self):
        """Test the model."""
        self.assertEqual(self.instance1.title, 'Title of Instance 1')
        self.assertEqual(self.instance2.text, 'Text of Instance 2')
