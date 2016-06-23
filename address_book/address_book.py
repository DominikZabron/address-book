import re

address_book = set()


class Person(object):
    def __init__(self, first_name, last_name, addresses, emails, phone_numbers):
        global address_book
        address_book.add(self)
        self.first_name = first_name
        self.last_name = last_name
        self.addresses = set(addresses)
        self.emails = set(emails)
        self.phone_numbers = set(phone_numbers)
        self.groups = set()

    def join_group(self, group):
        if isinstance(group, Group):
            group.members.add(self)
            self.groups.add(group)
        else:
            raise ValueError('There should be valid instance of Group class.')

    def display_groups(self):
        # Human readable form in __repr__()
        return list(self.groups)

    # We might use __str__(), but __repr__() is more readable inside ie. lists
    def __repr__(self):
        return self.first_name + ' ' + self.last_name


class Group(object):
    def __init__(self, name, members=()):
        global address_book
        address_book.add(self)
        self.name = name
        self.members = set()
        for member in members:
            self.add_member(member)

    def add_member(self, person):
        if isinstance(person, Person):
            person.groups.add(self)
            self.members.add(person)
        else:
            raise ValueError('There should be valid instance of Person class.')

    def display_members(self):
        return list(self.members)

    def filter_members_by_full_name(self, full_name):
        # More persons could have exactly the same names
        # In that case we should consider either to change __repr__() and use
        # __str__() instead, or raise ValueError during class initialization
        # if that name currently exists in address_book
        # This time we allow same names, they do not break anything
        return [m for m in self.members if m.__repr__() == full_name]

    def filter_members_by_email(self, pattern):
        filtered = []
        for member in self.members:
            for email in member.emails:
                if re.search(pattern, email):
                    filtered.append(member)
                    # Members should not be added twice
                    break
        return filtered

    def __repr__(self):
        return self.name
