from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from .models import Lecture
from .forms import LectureForm, LectureAdminForm
from conferences.models import Zosia, Place


User = get_user_model()


class LectureTestCase(TestCase):
    def setUp(self):
        place = Place.objects.create(name="Mieszko", address="foo")
        self.zosia = Zosia.objects.create(
            start_date=datetime.today() + timedelta(days=1),
            active=True, place=place)
        self.user = User.objects.create_user('john', 'john@thebeatles.com',
                                             'johnpassword')


class ModelTestCase(LectureTestCase):
    def test_must_have_zosia(self):
        lecture = Lecture(
            title="foo",
            abstract="foo",
            duration="5",
            lecture_type="1",
            person_type="0",
            author=self.user)
        with self.assertRaises(ValidationError):
            lecture.full_clean()

    def test_must_have_title(self):
        lecture = Lecture(
            zosia=self.zosia,
            abstract="foo",
            duration="5",
            lecture_type="1",
            person_type="0",
            author=self.user)
        with self.assertRaises(ValidationError):
            lecture.full_clean()

    def test_must_have_abstract(self):
        lecture = Lecture(
            zosia=self.zosia,
            title="foo",
            duration="5",
            lecture_type="1",
            person_type="0",
            author=self.user)
        with self.assertRaises(ValidationError):
            lecture.full_clean()

    def test_must_have_duration(self):
        lecture = Lecture(
            zosia=self.zosia,
            title="foo",
            abstract="5",
            lecture_type="1",
            person_type="0",
            author=self.user)
        with self.assertRaises(ValidationError):
            lecture.full_clean()

    def test_must_have_lecture_type(self):
        lecture = Lecture(
            zosia=self.zosia,
            title="foo",
            duration="5",
            abstract="1",
            person_type="0",
            author=self.user)
        with self.assertRaises(ValidationError):
            lecture.full_clean()

    def test_must_have_person_type(self):
        lecture = Lecture(
            zosia=self.zosia,
            title="foo",
            duration="5",
            lecture_type="1",
            abstract="0",
            author=self.user)
        with self.assertRaises(ValidationError):
            lecture.full_clean()

    def test_must_have_author(self):
        lecture = Lecture(
            zosia=self.zosia,
            title="foo",
            duration="5",
            lecture_type="1",
            person_type="0",
            abstract="foo")
        with self.assertRaises(ValidationError):
            lecture.full_clean()

    def test_create(self):
        lecture = Lecture(
            zosia=self.zosia,
            title="foo",
            abstract="bar",
            duration="5",
            lecture_type="1",
            person_type="0",
            author=self.user)

        count = Lecture.objects.count()
        try:
            lecture.full_clean()
        except ValidationError:
            self.fail("Full clean fail!")
        lecture.save()
        self.assertEqual(count + 1, Lecture.objects.count())

    def test_str(self):
        lecture = Lecture.objects.create(
            zosia=self.zosia,
            title="foo",
            abstract="bar",
            duration="5",
            lecture_type="1",
            person_type="0",
            author=self.user)
        self.assertEqual(str(lecture), "john - foo")


class FormTestCase(LectureTestCase):
    def test_user_form_no_data(self):
        form = LectureForm({})
        self.assertFalse(form.is_valid())

    def test_user_create_object(self):
        form = LectureForm({'title': 'foo', 'abstract': 'bar',
                            'duration': '5', 'lecture_type': '1',
                            'person_type': '0'})
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                form.save()
        count = Lecture.objects.count()
        obj = form.save(commit=False)
        obj.zosia = self.zosia
        obj.author = self.user
        obj.save()
        self.assertEqual(count + 1, Lecture.objects.count())

    def test_admin_form_no_data(self):
        form = LectureAdminForm({})
        self.assertFalse(form.is_valid())

    def test_admin_create_object(self):
        form = LectureAdminForm({'title': 'foo', 'abstract': 'bar',
                                'duration': '5', 'lecture_type': '1',
                                'person_type': '0', 'author': self.user.id})
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                form.save()
        count = Lecture.objects.count()
        obj = form.save(commit=False)
        obj.zosia = self.zosia
        obj.save()
        self.assertEqual(count + 1, Lecture.objects.count())