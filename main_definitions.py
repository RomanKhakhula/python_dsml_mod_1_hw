import re
from datetime import datetime, timedelta
from collections import UserDict

class PhoneFormatError(Exception):
    def __init__(self, message="Phone must be 10 digits number!"):
        self.message = message
        super().__init__(self.message)

class PhoneExistingError(Exception):
    def __init__(self, message="No such phone in phone list!"):
        self.message = message
        super().__init__(self.message)

class RecordExistingError(Exception):
    def __init__(self, message="No record with such name in address book!"):
        self.message = message
        super().__init__(self.message)

class DateFormatError(Exception):
    def __init__(self, message="Invalid date format. Use DD.MM.YYYY!"):
        self.message = message
        super().__init__(self.message)

def input_errors(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PhoneFormatError as e:
            print(f"{e}")
        except PhoneExistingError as e:
            print(f"{e}")
        except RecordExistingError as e:
            print(f"{e}")
        except DateFormatError as e:
            print(f"{e}")
        except Exception as e:
            print(f"{e}")
    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise PhoneFormatError

class Birthday(Field):
    def __init__(self, value: str):
        if re.search(r"\d{2}\.\d{2}\.\d{4}", value):
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        else:
            raise DateFormatError

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __phone_existing_check__(self, value):
        self.value = value
        if not self.value in [p.value for p in self.phones]:
            raise PhoneExistingError
              
    @input_errors
    def add_phone(self, phone):
        self.phone = Phone(phone)
        self.phones.append(self.phone)
        return "Phone added."

    @input_errors
    def remove_phone(self, phone):
        self.phone = Phone(phone)
        self.__phone_existing_check__(self.phone.value)
        self.phones.pop([p.value for p in self.phones].index(self.phone.value))

    @input_errors    
    def edit_phone(self, phone_to_edit, new_phone):
        self.phone_to_edit = Phone(phone_to_edit)
        self.new_phone = Phone(new_phone)
        self.__phone_existing_check__(self.phone_to_edit.value)
        self.phones.append(self.new_phone)
        self.phones.pop([p.value for p in self.phones].index(self.phone_to_edit.value))
        return "Phone changed."

    @input_errors
    def find_phone(self, phone):
        self.phone = Phone(phone)
        self.__phone_existing_check__(self.phone.value)
        return self.phone.value
    
    @input_errors
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return "Birtday added."

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {datetime.strftime(self.birthday.value, "%d.%m.%Y") if self.birthday else None}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = [[phone.value for phone in record.phones], record.birthday.value if record.birthday else None]
    
    def __record_existing_check__(self, key):
        self.key = key
        if not self.key in self.data.keys():
            raise RecordExistingError

    @input_errors
    def update(self, record):
        self.__record_existing_check__(record.name.value)
        self.data.update({record.name.value: [[phone.value for phone in record.phones], record.birthday.value if record.birthday else None]})
           
    @input_errors
    def find(self, key):
        self.__record_existing_check__(key)
        record = Record(key)
        for el in self.data[key][0]:
            record.add_phone(el)
        record.add_birthday(datetime.strftime(self.data[key][1], "%d.%m.%Y")) if self.data[key][1] else None
        return record
    
    @input_errors
    def delete(self, key):
        self.__record_existing_check__(key)
        self.data.pop(key)

    @input_errors
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        for key, value in self.data.items():
            if value[1]:
                this_year_bd = datetime(datetime.now().year, value[1].month, value[1].day).date()
                if 0 <= (this_year_bd - datetime.now().date()).days <= 7:
                    if this_year_bd.isoweekday() == 6: 
                        congratulation_date = this_year_bd + timedelta(days=2) 
                    elif this_year_bd.isoweekday() == 7:
                        congratulation_date = this_year_bd + timedelta(days=1)
                    else:
                        congratulation_date = this_year_bd
                    upcoming_birthdays.append({key: f"this year birth date: {datetime.strftime(this_year_bd, "%d.%m.%Y")} >>> congratulation date: {datetime.strftime(congratulation_date, "%d.%m.%Y")}"})
                else: 
                    continue
            else: 
                continue
        return upcoming_birthdays

if __name__ == "__main__":

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_phone("s555555555")
    john_record.add_phone("555555555")
    john_record.add_birthday("27.02.2024")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    # jane_record.add_birthday("28.02.2024")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(f"{name}: {record[0]}, {record[1]}")

    print(book.get_upcoming_birthdays())

    # Знаходження та редагування телефону для John
    john = book.find("Jhon")
    john = book.find("John")
    john.edit_phone("1234567890", "l112223333")
    john.edit_phone("1234567890"[::-1], "1112223333")
    john.edit_phone("1234567890", "1112223333")
    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
    book.update(john)

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("s555555555")
    found_phone = john.find_phone("6666666666")
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jnae")
    book.delete("Jane")

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(f"{name}: {record[0]}, {record[1]}")