from datetime import datetime, timedelta
from collections import UserDict

class Field:
    """
    Base class for fields in a record. Stores a value and provides a string representation.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """
    Represents a name field. Ensures the name is not empty.
    """
    def __init__(self, value):
        if not value:
            raise ValueError("The name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    """
    Represents a phone field. Ensures the phone number contains exactly 10 digits.
    """
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("The phone number must contain exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    """
    Represents a birthday field. Ensures the date is in the format DD.MM.YYYY.
    """
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    """
    Represents a contact record with a name, phone numbers, and an optional birthday.
    Provides methods to add, remove, and edit phone numbers, as well as add a birthday.
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """
        Adds a phone number to the record.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Removes a phone number from the record.
        Returns True if the phone number was found and removed, otherwise False.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        """
        Edits an existing phone number in the record.
        Replaces old_phone with new_phone. Returns True if successful, otherwise False.
        """
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def add_birthday(self, birthday):
        """
        Adds a birthday to the record.
        """
        self.birthday = Birthday(birthday)

    def __str__(self):
        """
        Returns a string representation of the record, including name, phones, and birthday.
        """
        phone_str = ', '.join([p.value for p in self.phones])
        birthday_str = f", Birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_str}{birthday_str}"

class AddressBook(UserDict):
    """
    Represents an address book that stores multiple records.
    Provides methods to add, find, delete records, and get upcoming birthdays.
    """
    def add_record(self, record):
        """
        Adds a record to the address book.
        """
        self.data[record.name.value] = record

    def find(self, name):
        """
        Finds a record by name. Returns the record if found, otherwise None.
        """
        return self.data.get(name)

    def delete(self, name):
        """
        Deletes a record by name from the address book.
        """
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        """
        Returns a list of records with birthdays in the next 7 days.
        """
        upcoming_birthdays = []
        today = datetime.now()
        next_week = today + timedelta(days=7)
        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                if today <= birthday <= next_week:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays


book = AddressBook()


john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_birthday("10.04.1990")
book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("05.04.1992")
book.add_record(jane_record)


john = book.find("John")
john.edit_phone("1234567890", "1112223333")


for record in book.data.values():
    print(record)


upcoming = book.get_upcoming_birthdays()
print("Upcoming birthdays:")
for record in upcoming:
    print(record)