from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from blog.models import Page, PageTranslation
from django.conf import settings

class PageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a base page
        cls.page = Page.objects.create(
            url="about-us",
            title="About Us",
            content="<p>This is the content of the About Us page.</p>"
        )

        # Create a translation for the page
        cls.translation = PageTranslation.objects.create(
            page=cls.page,
            lang="fr",
            title="À propos de nous",
            content="<p>C'est le contenu de la page À propos de nous.</p>"
        )

    def test_page_creation(self):
        """Test that a Page object is created correctly."""
        self.assertEqual(self.page.url, "about-us")
        self.assertEqual(self.page.title, "About Us")
        self.assertIn("This is the content", self.page.content)

    def test_url_validation(self):
        """Test URL validation with valid and invalid inputs."""
        # Valid URL
        valid_page = Page(url="valid-url", title="Valid Page", content="<p>Valid content</p>")
        valid_page.full_clean()  # Should not raise an error

        # Invalid URL (contains special characters)
        invalid_page = Page(url="invalid@url", title="Invalid Page", content="<p>Invalid content</p>")
        with self.assertRaises(ValidationError):
            invalid_page.full_clean()

    def test_get_by_url(self):
        """Test the get_by_url method for different scenarios."""
        # Test with a valid URL and primary language
        page = Page.get_by_url("about-us", settings.LANGUAGE_CODE)
        self.assertIsNotNone(page)
        self.assertEqual(page.title, "About Us")

        # Test with a valid URL and translated language
        translated_page = Page.get_by_url("about-us", "fr")
        self.assertIsNotNone(translated_page)
        self.assertEqual(translated_page.title, "À propos de nous")
        self.assertIn("C'est le contenu", translated_page.content)

        # Test with a non-existent URL
        non_existent_page = Page.get_by_url("non-existent", settings.LANGUAGE_CODE)
        self.assertIsNone(non_existent_page)

        # Test with an invalid URL input
        invalid_page = Page.get_by_url(None, settings.LANGUAGE_CODE)
        self.assertFalse(invalid_page)

    def test_translation_priority(self):
        """Test that translations take priority over the base page content."""
        # Fetch the page with a translated language
        translated_page = Page.get_by_url("about-us", "fr")
        self.assertEqual(translated_page.title, "À propos de nous")
        self.assertIn("C'est le contenu", translated_page.content)

        # Fetch the page with the primary language
        primary_page = Page.get_by_url("about-us", settings.LANGUAGE_CODE)
        self.assertEqual(primary_page.title, "About Us")
        self.assertIn("This is the content", primary_page.content)

    @override_settings(LANGUAGE_CODE='es')
    def test_language_code_override(self):
        """Test behavior when the LANGUAGE_CODE setting is overridden."""
        # Fetch the page with a non-primary language
        page = Page.get_by_url("about-us", "es")
        self.assertIsNotNone(page)
        self.assertEqual(page.title, "About Us")  # No translation exists for 'es'

    def test_unique_together_constraint(self):
        """Test the unique_together constraint for PageTranslation."""
        # Attempt to create a duplicate translation
        duplicate_translation = PageTranslation(
            page=self.page,
            lang="fr",
            title="Duplicate Translation",
            content="<p>Duplicate content</p>"
        )
        with self.assertRaises(Exception):  # IntegrityError expected
            duplicate_translation.save()