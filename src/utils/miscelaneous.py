from faker import Faker


def generate_fake_user():
    fake = Faker()
    name = fake.name()
    first_name = name.split()[0].lower()
    last_name = name.split()[1].lower()
    username = f"{first_name[0]}.{last_name}"
    email = f"{first_name}.{last_name}@fakemail.com"
    password = fake.password()

    return username, email, name, password
