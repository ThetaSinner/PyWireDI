from unittest import TestCase

from caseTransform import CaseTransform


class TestCaseTransform(TestCase):
    def test_pascal_case_to_underscore(self):
        self.assertEquals("test_case", CaseTransform().pascal_case_to_underscore("TestCase"))
        self.assertEquals("test_case", CaseTransform().pascal_case_to_underscore("testCase"))

    def test_underscore_to_pascal_case(self):
        self.assertEquals("TestCase", CaseTransform().underscore_to_pascal_case("test_case"))
