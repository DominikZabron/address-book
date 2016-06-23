ADDRESS BOOK
============

Simple address book library in Python
-------------------------------------

### Installation

```python
python setup.py install
```

### Importing

```python
from address_book import Person, Group, address_book
```
### Usage

You can create a contact:
```python
>>> alex = Person(
>>>     first_name='Alexander',
>>>     last_name='de Jong',
>>>     addresses=[],
>>>     emails=['alexander@company.com', 'alex@dejong.nl'],
>>>     phone_numbers=[]
>>> )
```

You can create a group with or without a contacts:
```python
>>> py_con = Group(name='python dojo', members=(alex,))
>>> french_literature = Group(name='Carpe diem', members=(alex,))
>>> chess_players = Group(name='blitz')
```

You can then attach a contact with a group, in both ways:
```python
>>> french_literature.add_member(alex)
>>> alex.join_group(chess_players)
```

You can check your address_book collection any time:
```python
>>> print address_book
set([Alexander de Jong, blitz, python dojo, Carpe diem])
```

You can easily find members of the group and manipulate on them:
```python
>>> py_con.members
set([Alexander de Jong])
>>> py_con.display_members()
['Alexander de Jong']
```

As well as groups the person belongs to:
```python
>>> alex.groups()
set(['Carpe diem', 'python dojo', 'blitz'])
>>> alex.display_groups()
['Carpe diem', 'python dojo', 'blitz']
```

Most importantly, you can search in your groups by exact name:
```python
>>> py_con.filter_members_by_full_name('Alexander de Jong')
[Alexander de Jong]
```

Or by partial email:
```python
>>> py_con.filter_members_by_email('alex')
[Alexander de Jong]
```

### Considerations

There could be better search for email addresses when more advanced regular
expressions would be implemented. For now, searches should also work properly
for domain name part like `comp`.