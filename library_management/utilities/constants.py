class K:
    def __init__(self, label=None, **kwargs):
        assert (len(kwargs) == 1)
        for k, v in kwargs.items():
            self.id = k
            self.v = v
        self.label = label or self.id


class Konstants:
    def __init__(self, *args):
        self.klist = args
        for k in self.klist:
            setattr(self, k.id, k.v)

    def choices(self):
        return [(k.v, k.label) for k in self.klist]

    def get_label(self, key):
        for k in self.klist:
            if k.v == key:
                return k.label
        return None


TRUE_VALUES = [True, 'TRUE', 'true', 'True', 1, '1']
FALSE_VALUES = [False, 'FALSE', 'false', 'False', 0, '0']
RETURN_RANGE = 15


ROLE_TYPES = Konstants(
    K(super_admin='SUPER_ADMIN', label='Super Admin'),
    K(student='STUDENT', label='Student'),
    K(librarian='LIBRARIAN', label='Librarian'),
    K(external_user='EXTERNAL_USER', label='External User')
    )


DEPARTMENTS = Konstants(
    K(dance='DANCE', label='Dance'),
    K(economics='ECONOMICS', label='Economics'),
    K(english='ENGLISH', label='English'),
    K(psychology='PSYCHOLOGY', label='Psychology'),
    K(computer_science='COMPUTER_SCIENCE', label='Computer Science'),
    K(political_science='POLITICAL_SCIENCE', label='Political Science'),
    K(statistics='STATISTICS', label='Statistics'),
    K(mathematics='MATHEMATICS', label='Mathematics')
    )

STUDY_LEVEL = Konstants(
    K(undergrad='UNDERGRAD', label='Undergraduate'),
    K(grad='GRAD', label='Graduate')
    )

REQUEST_STATUS = Konstants(
    K(pending='PENDING', label='Pending'),
    K(approved='APPROVED', label='Approved'),
    K(rejected='REJECTED', label='Rejected'),
    K(rejected='CANCELLED', label='Cancelled')
    )


REQUEST_FOR = Konstants(
    K(sale='SALE', label='Sale'),
    K(rent='RENT', label='Rent')
    )


RESERVE_STATUS = Konstants(
    K(open='OPEN', label='Open'),
    K(overdue='OVERDUE', label='Overdue'),
    K(close='CLOSE', label='Close')
    )
