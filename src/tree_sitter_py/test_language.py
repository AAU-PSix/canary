import string
from . import *

from importlib.resources import path
from tree_sitter.binding import Query as _Query
from tree_sitter import Language as _Language
import unittest
from os import path

class TestLanguageLibrary(unittest.TestCase):
    def test_vendor_path(self):
        self.assertEqual(LanguageLibrary.vendor_path(), './vendor')
        self.assertIsInstance(LanguageLibrary.vendor_path(), str)

    def test_build_path(self):
        self.assertEqual(LanguageLibrary.build_path(), './build')
        self.assertIsInstance(LanguageLibrary.build_path(), str)

    def test_build_file(self):
        self.assertEqual(LanguageLibrary.build_file(), 'my-languages.so')
        self.assertIsInstance(LanguageLibrary.build_file(), str)

    def test_full_build_path(self):
        self.assertEqual(LanguageLibrary.full_build_path(), './build/my-languages.so')
        self.assertIsInstance(LanguageLibrary.full_build_path(), str)

    def test_build(self):
        LanguageLibrary.build()
        self.assertTrue(path.exists(LanguageLibrary.full_build_path()))
        js = LanguageLibrary.js()
        self.assertIsNotNone(js)
        self.assertIsInstance(js, Language)
        self.assertIsInstance(js._language, _Language)

class TestLanguage(unittest.TestCase):
    _js_language: Language = None

    def setUp(self) -> None:
        LanguageLibrary.build()
        self._js_language = LanguageLibrary.js()
        return super().setUp()

    def test_id(self):
        self.assertIsNotNone(self._js_language.id)
        self.assertIsInstance(self._js_language.id, int)

    def test_name(self):
        self.assertIsNotNone(self._js_language.name)
        self.assertEqual(self._js_language.name, 'javascript')
        self.assertIsInstance(self._js_language.name, str)

    def test_field_id_for_name(self):
        self.assertIsInstance(self._js_language.field_id_for_name('kind'), int)
        self.assertEqual(self._js_language.field_id_for_name('kind'), 21)
        self.assertIsInstance(self._js_language.field_id_for_name('name'), int)
        self.assertEqual(self._js_language.field_id_for_name('name'), 25)
        self.assertIsInstance(self._js_language.field_id_for_name('source'), int)
        self.assertEqual(self._js_language.field_id_for_name('source'), 34)
        self.assertIsInstance(self._js_language.field_id_for_name('condition'), int)
        self.assertEqual(self._js_language.field_id_for_name('condition'), 8)
        self.assertIsInstance(self._js_language.field_id_for_name('consequence'), int)
        self.assertEqual(self._js_language.field_id_for_name('consequence'), 9)
        self.assertIsInstance(self._js_language.field_id_for_name('alternative'), int)
        self.assertEqual(self._js_language.field_id_for_name('alternative'), 2)

    def test_query(self):
        query = self._js_language.query('(binary_expression (number) (number))')
        self.assertIsInstance(query, Query)
        self.assertIsInstance(query._query, _Query)
        pass