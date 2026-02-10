import unittest
from my_class_basics import Person


class TestPerson(unittest.TestCase):
    def test_birthday_increments_age(self):
        p = Person("Test", 30)
        p.birthday()
        self.assertEqual(p.age, 31)

    def test_negative_age_raises(self):
        p = Person("Test", 30)
        with self.assertRaises(ValueError):
            p.age = -1

    def test_say_hello_contains_name_and_age(self):
        p = Person("Test", 25)
        msg = p.say_hello()
        self.assertIn("Test", msg)
        self.assertIn("25", msg)


if __name__ == "__main__":
    unittest.main()
