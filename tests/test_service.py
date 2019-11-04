# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from unittest import TestCase

from pydsf.exceptions import DSFServiceError
from pydsf.service.response import parse_response
from pydsf.service.translations import translate_input_fields, translate_output_fields


class MockMessage(object):
    SUMMARY = "Error summary"

    def __init__(self, error_code):
        self.CODE = error_code


class MockError(object):
    feilmelding = "Error message here."


class MockErrorDetail(object):
    feil = MockError()


class MockResponseOK(object):

    def __init__(self, error_code=None, result=True):
        if result:
            self.RESULT = "Results"
        else:
            self.MESSAGE = MockMessage(error_code)


class MockResponseError(object):

    faultstring = "Fault string"
    detail = MockErrorDetail()

    def __init__(self):
        pass


class MockResponseParsed(object):
    HOV = list()

    def __init__(self):
        self.HOV.append(("FODT", "010107"))
        self.HOV.append(("PERS", "50160"))
        self.HOV.append(("NAVN-F", "TOMAS"))
        self.HOV.append(("NAVN-M", ""))
        self.HOV.append(("UKJENTFELT", "something"))


class PersonTests(TestCase):

    def test_bad_search_fields(self):
        pass

    def test_error_response(self):
        pass

    def tets_empty_response(self):
        pass

    def test_result(self):
        pass


class ResponseTests(TestCase):

    def test_has_result(self):
        result = MockResponseOK()
        parsed = parse_response((200, result))

        self.assertEqual(parsed, "Results")

    def test_no_result(self):
        result = MockResponseOK(error_code="1", result=False)

        parsed = parse_response((200, result))

        self.assertIsNone(parsed)

    @staticmethod
    def test_result_with_error():
        result = MockResponseOK(error_code="2", result=False)

        with pytest.raises(DSFServiceError):
            parse_response((200, result))

    @staticmethod
    def test_uknown_error():
        result = MockResponseError()

        with pytest.raises(DSFServiceError):
            parse_response((500, result))


class TranslationTests(TestCase):

    def test_output_translation(self):
        response = MockResponseParsed()
        translated = translate_output_fields(response)

        self.assertIsInstance(translated, dict)
        self.assertTrue("date_of_birth" in translated)
        self.assertTrue("person_number" in translated)
        self.assertTrue("first_name" in translated)
        self.assertTrue("middle_name" in translated)

        # Verify capitalisation and None
        self.assertEqual(translated["first_name"], "Tomas")
        self.assertEqual(translated["UKJENTFELT"], "Something")

        # Verify that empty strings are translated to None
        self.assertIsNone(translated["middle_name"])

    def test_input_translation(self):
        valid_input = {
            "end_user": "unicornis-test",
            "first_name": "tomas",
            "last_name": "topstad"
        }
        invalid_input_invalid_field = {
            "end_user": "unicornis_test",
            "invalidfield": "somevalue"
        }

        with pytest.raises(ValueError):
            translate_input_fields(**invalid_input_invalid_field)

        translated = translate_input_fields(**valid_input)
        self.assertTrue("saksref" in translated)
        self.assertTrue("fornavn" in translated)
        self.assertTrue("etternavn" in translated)
