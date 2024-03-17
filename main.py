import main_definitions as md, pickle
from functools import wraps

def parse_input_input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print(f"Neither command entered, please enter one of: {args[1]}")
            return "nothing"                                                             #return some iterable to continue
        except KeyError:
            print(f"Command '{args[0]}' unsupported, please enter one of: {args[1]}")
            return "nothing"                                                             #return some iterable to continue   
        except Exception as e:
            print(f"{e}")                                                                   
            return "nothing"                                                             #return some iterable to continue
    return inner

@parse_input_input_error
def parse_input(user_input, cmd_dict):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    cmd_dict[cmd]                           #check if entered command correct (exists in commands list)
    return cmd, *args

def add_contact_input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Contact info incorrect or does not entered. Expected: add [username] [phone (10 dig. number)]"
        except Exception as e:
             return f"{e}"
    return inner

@add_contact_input_error
def add_contact(args, contacts):
    name, phone = args
    msg = 'Phone not added.'
    if contacts.find(name):
        record = contacts.find(name)
        msg = record.add_phone(phone)
        contacts.update(record)
        return msg if msg != None else 'Phone not added.'
    else:
        record = md.Record(name)
        msg = record.add_phone(phone)
        contacts.add_record(record)
    return 'Contact added.' + ' ' + (msg if msg != None else 'Phone not added.')

def change_contact_input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Contact info incorrect or does not entered. Expected: change [username] [old_phone (10 dig. number)] [new_phone (10 dig. number)]"
        except Exception as e:
             return f"{e}"
    return inner

@change_contact_input_error
def change_contact(args, contacts):
    name, old_phone, new_phone = args
    if contacts.find(name):
        record = contacts.find(name)
        msg = record.edit_phone(old_phone, new_phone)
        contacts.update(record)
        return msg if msg != None else 'Phone not changed.'

def show_phone_input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Username does not entered. Expected: phone [username]"
        except Exception as e:
             return f"{e}"
    return inner

@show_phone_input_error  
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    return f"name: {record.name.value}, phones: {[phone.value for phone in record.phones]}" if record != None else "name: , phones: "

def show_all(contacts):
    contatct_records = [contacts.find(key) for key in contacts.keys()] if len(contacts.keys()) > 0 else ["Contact list is empty."]
    return contatct_records

def add_contact_input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Contact info incorrect or does not entered. Expected: add_birthday [username] [birthday (DD.MM.YYYY)]"
        except Exception as e:
             return f"{e}"
    return inner

@add_contact_input_error
def add_birthday(args, contacts):
    name, birthday = args
    msg = 'Birthday not added.'
    if contacts.find(name):
        record = contacts.find(name)
        msg = record.add_birthday(birthday)
        contacts.update(record)
    return msg if msg != None else 'Birthday not added.'

def show_birthday_input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Username does not entered. Expected: show_birthday [username]"
        except Exception as e:
             return f"{e}"
    return inner

@show_birthday_input_error  
def show_birthday(args, contacts):
    name = args[0]
    record = contacts.find(name)
    return f"name: {record.name.value}, birthday: {md.datetime.strftime(record.birthday.value, "%d.%m.%Y")}" if record != None else "name: , birthday: "

def show_upcoming_birthdays(contacts):
    up_birthdays_list = contacts.get_upcoming_birthdays() if len(contacts.get_upcoming_birthdays()) > 0 else ["Upcoming birthdays list is empty."]
    return up_birthdays_list

def save_data(contacts: md.AddressBook, filename="contacts.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(contacts, f)

def load_data(filename="contacts.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return md.AddressBook()  # if contactcts.pkl not found

def main():
    contacts = load_data()
    cmd_dict = {"close": "exit bot", "exit": "exit bot", "hello": "greeting - non functional command", 
                "add": "adding new contact >>> add [username] [phone (10 dig. number)]", 
                "change": "update contact if exists >>> change [username] [old_phone (10 dig. number)] [new_phone (10 dig. number)]", 
                "phone": "show contact if exists >>> phone [username]", "all": "show all contacts if exists",
                "add_birthday": "add birthday to contact >>> add_birthday [username] [birthday (DD.MM.YYYY)]",
                "show_birthday": "show contact's birthday >>> show_birthday [username]", "birthdays": "show upcoming birthdays"}   
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input, cmd_dict)
        if command in ["close", "exit"]:
            save_data(contacts)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            for el in show_all(contacts):
                print(el, end="\n")
        elif command == "add_birthday":
            print(add_birthday(args, contacts))
        elif command == "show_birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            for el in show_upcoming_birthdays(contacts):
                print(el, end="\n")

if __name__ == "__main__":
    main()