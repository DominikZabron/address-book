from faker import Factory

import unittest

from address_book import Person, Group, address_book

fake = Factory.create()


class PersonTestCase(unittest.TestCase):
    def setUp(self):
        self.person_params = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'addresses': [fake.address()],
            'emails': [fake.email()],
            'phone_numbers': [fake.phone_number()],
        }
        self.person = Person(**self.person_params)

        self.group_name = fake.word()
        self.group = Group(name=self.group_name)

        self.group_name_2 = fake.word()
        self.group_2 = Group(name=self.group_name_2)

    def test_create_person(self):
        self.assertTrue(isinstance(self.person, Person))

    def test_person_attrs(self):
        self.assertEqual(self.person_params['first_name'], self.person.first_name)
        self.assertEqual(self.person_params['last_name'], self.person.last_name)
        self.assertIn(self.person_params['addresses'][0], self.person.addresses)
        self.assertIn(self.person_params['emails'][0], self.person.emails)
        self.assertIn(self.person_params['phone_numbers'][0], self.person.phone_numbers)

    def test_person_in_address_book(self):
        self.assertIn(self.person, address_book)

    def test_many_addresses(self):
        new_address = fake.address()
        self.person.addresses.add(new_address)
        self.assertIn(new_address, self.person.addresses)
        self.assertEqual(len(self.person.addresses), 2)

    def test_many_emails(self):
        new_email = fake.email()
        self.person.emails.add(new_email)
        self.assertIn(new_email, self.person.emails)
        self.assertEqual(len(self.person.emails), 2)

    def test_many_phone_numbers(self):
        new_phone = fake.phone_number()
        self.person.phone_numbers.add(new_phone)
        self.assertIn(new_phone, self.person.phone_numbers)
        self.assertEqual(len(self.person.phone_numbers), 2)

    # Test if sets do not return the same objects twice
    def test_emails_contain_no_doubles(self):
        old_email = self.person_params['emails'][0]

        # We insert existing email to person again
        self.person.emails.add(old_email)
        self.assertIn(old_email, self.person.emails)

        # Should contain only 1 email address
        self.assertEqual(len(self.person.emails), 1)

    def test_joining_groups(self):
        self.person.join_group(self.group)
        self.assertEqual(len(self.group.members), 1)
        self.assertEqual(len(self.person.groups), 1)

        self.person.join_group(self.group_2)
        self.assertEqual(len(self.group_2.members), 1)
        self.assertEqual(len(self.person.groups), 2)

    def test_joining_groups_wrong_input(self):
        with self.assertRaises(ValueError):
            self.group.add_member('group')

    def test_display_groups(self):
        self.person.join_group(self.group)
        self.person.join_group(self.group_2)

        groups = self.person.display_groups()
        self.assertIn(self.group, groups)
        self.assertIn(self.group_2, groups)


class GroupTestCase(unittest.TestCase):
    def setUp(self):
        self.person_params = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'addresses': fake.address(),
            'emails': [fake.email()],
            'phone_numbers': [fake.phone_number()],
        }
        self.person = Person(**self.person_params)

        self.group_name = fake.word()
        self.group = Group(name=self.group_name)

        self.group_name_2 = fake.word()
        self.group_2 = Group(name=self.group_name_2)

    def test_create_group(self):
        self.assertTrue(isinstance(self.group, Group))

    def test_group_attrs(self):
        self.assertEqual(self.group_name, self.group.name)
        self.assertEqual(len(self.group.members), 0)

    def test_group_in_address_book(self):
        self.assertIn(self.group, address_book)

    def test_adding_membership(self):
        self.group.add_member(self.person)
        self.assertEqual(len(self.group.members), 1)
        self.assertEqual(len(self.person.groups), 1)

        self.group_2.add_member(self.person)
        self.assertEqual(len(self.group_2.members), 1)
        self.assertEqual(len(self.person.groups), 2)

    def test_adding_membership_wrong_input(self):
        with self.assertRaises(ValueError):
            self.group.add_member('person')

    def test_find_group_members(self):
        person_params_2 = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'addresses': fake.address(),
            'emails': [fake.email()],
            'phone_numbers': [fake.phone_number()],
        }
        person_2 = Person(**person_params_2)

        person_params_3 = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'addresses': fake.address(),
            'emails': [fake.email()],
            'phone_numbers': [fake.phone_number()],
        }
        person_3 = Person(**person_params_3)

        # We create new group with 2 persons as members
        group_name_3 = fake.word()
        group_3 = Group(name=group_name_3, members=(self.person, person_2))

        # Only person_3 should not be a member of group_3
        # We should be able to find user-friendly
        # string representation of members in results
        members_3 = group_3.display_members()
        self.assertIn(self.person, members_3)
        self.assertIn(person_2, members_3)
        self.assertNotIn(person_3, members_3)

    def test_filter_members_by_name(self):
        # We need to create names by hand to be sure about search results
        person_params_2 = {
            'first_name': 'Vincent',
            'last_name': 'van Gogh',
            'addresses': fake.address(),
            'emails': [fake.email()],
            'phone_numbers': [fake.phone_number()],
        }
        person_2 = Person(**person_params_2)

        person_params_3 = {
            'first_name': 'Rembrandt',
            'last_name': 'van Rijn',
            'addresses': fake.address(),
            'emails': [fake.email()],
            'phone_numbers': [fake.phone_number()],
        }
        person_3 = Person(**person_params_3)

        group_name_3 = fake.word()
        group_3 = Group(name=group_name_3, members=(person_2, person_3))

        results = group_3.filter_members_by_full_name('Vincent van Gogh')
        self.assertIn(person_2, results)
        self.assertNotIn(person_3, results)

        results = group_3.filter_members_by_full_name('Peter Paul Rubens')
        self.assertNotIn(person_2, results)
        self.assertNotIn(person_3, results)

    def test_filter_members_by_email(self):
        # We need to create email addresses by hand to be sure about search results
        person_params_2 = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'addresses': fake.address(),
            'emails': ['alexander@company.com'],
            'phone_numbers': [fake.phone_number()],
        }
        person_2 = Person(**person_params_2)

        person_params_3 = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'addresses': fake.address(),
            'emails': ['julia@mail.com'],
            'phone_numbers': [fake.phone_number()],
        }
        person_3 = Person(**person_params_3)

        group_name_3 = fake.word()
        group_3 = Group(name=group_name_3, members=(person_2, person_3))

        results = group_3.filter_members_by_email('alexander@company.com')
        self.assertIn(person_2, results)
        self.assertNotIn(person_3, results)

        results = group_3.filter_members_by_email('alex')
        self.assertIn(person_2, results)
        self.assertNotIn(person_3, results)

        results = group_3.filter_members_by_email('.com')
        self.assertIn(person_2, results)
        self.assertIn(person_3, results)

    def test_two_email_addresses_of_one_user_match(self):
        # We need to create email addresses by hand to be sure about search results
        person_params_2 = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'addresses': fake.address(),
            'emails': ['alexander@company.com'],
            'phone_numbers': [fake.phone_number()],
        }
        person_2 = Person(**person_params_2)

        person_params_3 = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'addresses': fake.address(),
            'emails': ['julia@mail.com', 'julia@jensen.nl'],
            'phone_numbers': [fake.phone_number()],
        }
        person_3 = Person(**person_params_3)

        group_name_3 = fake.word()
        group_3 = Group(name=group_name_3, members=(person_2, person_3))

        # There should be only 1 result
        results = group_3.filter_members_by_email('julia')
        self.assertNotIn(person_2, results)
        self.assertIn(person_3, results)
        self.assertEqual(len(results), 1)
