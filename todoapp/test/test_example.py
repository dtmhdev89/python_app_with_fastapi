import pytest


def test_equal_or_not_equal():
    assert 3 == 3


def test_is_instances():
    assert isinstance('hello', str)
    assert isinstance(10, int)


def test_boolean():
    validated = True
    
    assert validated is True
    assert ('heelo' == 'world') is False


def test_type():
    assert type("hello" is str)
    assert type("world" is not int)


def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]

    assert 1 in num_list
    assert 8 not in num_list
    assert all(num_list)
    assert not any(any_list)


class Student():
    def __init__(
        self,
        first_name: str,
        last_name: str,
        major: str,
        years: int
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student("John", "Doe", "Computer Science", 3)

def test_person_intialization(default_employee):
    assert default_employee.first_name == "John", "First name should be John"
    assert default_employee.last_name == "Doe", "Last name shoulb be Doe"
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3



