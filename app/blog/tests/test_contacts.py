from django.test import TestCase, override_settings
from django.core.cache import cache
from blog.models import Contacts, ContactsTranslation
from django.conf import settings

class ContactsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a base contact
        cls.contact = Contacts.objects.create(
            title="Main Office",
            val="123-456-7890"
        )

        # Create a translation for the contact
        cls.translation = ContactsTranslation.objects.create(
            item=cls.contact,
            lang="fr",
            title="Bureau Principal",
            val="098-765-4321"
        )

    def test_contact_creation(self):
        """Test that a Contacts object is created correctly."""
        self.assertEqual(self.contact.title, "Main Office")
        self.assertEqual(self.contact.val, "123-456-7890")

    def test_get_translated_primary_language(self):
        """Test get_translated method with the primary language."""
        contacts = Contacts.get_translated(settings.LANGUAGE_CODE)
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]['title'], "Main Office")
        self.assertEqual(contacts[0]['val'], "123-456-7890")

    def test_get_translated_secondary_language(self):
        """Test get_translated method with a translated language."""
        contacts = Contacts.get_translated("fr")
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]['title'], "Bureau Principal")
        self.assertEqual(contacts[0]['val'], "098-765-4321")

    def test_get_translated_no_translation(self):
        """Test get_translated method when no translation exists for the specified language."""
        contacts = Contacts.get_translated("es")
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]['title'], "Main Office")  # Fallback to the base language
        self.assertEqual(contacts[0]['val'], "123-456-7890")

    def test_cache_usage(self):
        """Test that the get_translated method uses caching correctly."""
        cache_key = f'contacts_tr_{settings.LANGUAGE_CODE}'
        cache.clear()  # Clear cache before testing

        # First call should populate the cache
        Contacts.get_translated(settings.LANGUAGE_CODE)
        cached_data = cache.get(cache_key)
        self.assertIsNotNone(cached_data)

        # Second call should retrieve data from the cache
        cached_contacts = Contacts.get_translated(settings.LANGUAGE_CODE)
        self.assertEqual(len(cached_contacts), 1)
        self.assertEqual(cached_contacts[0]['title'], "Main Office")

    @override_settings(LANGUAGE_CODE='es')
    def test_language_code_override(self):
        """Test behavior when the LANGUAGE_CODE setting is overridden."""
        contacts = Contacts.get_translated("es")
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]['title'], "Main Office")  # No translation exists for 'es'

    def test_unique_together_constraint(self):
        """Test the unique_together constraint for ContactsTranslation."""
        # Attempt to create a duplicate translation
        duplicate_translation = ContactsTranslation(
            item=self.contact,
            lang="fr",
            title="Duplicate Translation",
            val="Duplicate Value"
        )
        with self.assertRaises(Exception):  # IntegrityError expected
            duplicate_translation.save()