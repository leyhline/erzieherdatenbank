from django.test import TestCase
from django.core.exceptions import ValidationError

from .templatetags.activity_extras import hashtagger
from .models import Activity, Tag, Season
#from .migrations.0001_initial_data import Migration


class HashtagFilterTests(TestCase):

    def test_empty_hashtag(self):
        text = "# was geht # ab?!"
        result = hashtagger(text)
        self.assertEqual(result, text)

    def test_good_hashtag(self):
        text = "#Yo was #geht beidir?"
        result = hashtagger(text)
        expected = "<a href=\"yo\">#Yo</a> was <a href=\"geht\">#geht</a> beidir?"
        self.assertEqual(result, expected)

    def test_symbols_hashtag(self):
        text = "#! #krass?! ### #,. #heh=?\" #<b>"
        result = hashtagger(text)
        expected = "#! <a href=\"krass\">#krass</a>?! ### #,. <a href=\"heh\">#heh</a>=?&quot; #&lt;b&gt;"
        self.assertEqual(result, expected)


class ActivitySaveTests(TestCase):

    def test_simple_safe(self):
        a = Activity(title="Test", description="Was geht ab?")
        a.save()
        self.assertEqual(Activity.objects.first().title, "Test")

    def test_add_tags_from_description(self):
        a = Activity(title="Test", description="Was #geht ab, #Digger?")
        a.save()
        tags = tuple(tag.name for tag in a.tags.all())
        self.assertEqual(len(tags), 2)
        self.assertIn("geht", tags)
        self.assertIn("digger", tags)

    def test_delete_tags(self):
        a = Activity(title="Test", description="Was #geht ab, #Digger?")
        a.save()
        a.description = "Was geht ab, Digger?"
        a.save()
        self.assertEqual(len(a.tags.all()), 0)

    def test_some_tags_already_exist(self):
        existing_tag = Tag(name="digger")
        existing_tag.save()
        self.assertEqual(Tag.objects.first().name, "digger")
        a = Activity(title="Test", description="Was #geht ab, #Digger?")
        a.save()
        tags = tuple(tag.name for tag in a.tags.all())
        self.assertIn("geht", tags)
        self.assertIn("digger", tags)

    def test_so_you_dont_delete_tags_with_multiple_activities(self):
        a1 = Activity(title="Test1", description="Was #geht ab, #Digger?")
        a1.save()
        a2 = Activity(title="Test2", description="Was #geht ab, #Trigger?")
        a2.save()
        a3 = Activity(title="Test3", description="Was #geht ab, #Hipper?")
        a3.save()
        self.assertEqual(len(Tag.objects.all()), 4)
        a3.delete()
        self.assertEqual(len(Tag.objects.get(name="hipper").activity_set.all()), 0)
        a2.description = "Was #geht ab, #Digger?"
        a2.save()
        self.assertEqual(len(Tag.objects.get(name="geht").activity_set.all()), 2)


class InitialModelDataTest(TestCase):

    def test_initial_season_data(self):
        seasons = Season.objects.order_by("name")
        self.assertEqual(len(seasons), 4)
        self.assertEqual(seasons[0].name, "F")
        self.assertEqual(seasons[1].name, "H")
        self.assertEqual(seasons[2].name, "S")
        self.assertEqual(seasons[3].name, "W")


class ModelValidationTest(TestCase):

    def test_tag_regex_validator(self):
        Tag.tag_validator("atag")
        with self.assertRaises(ValidationError):
            Tag.tag_validator(" atag")
            Tag.tag_validator("atag%")
            Tag.tag_validator(" atag ")
            Tag.tag_validator("atag btag")
