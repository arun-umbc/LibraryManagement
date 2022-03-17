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


ROLE_TYPES = Konstants(
    K(super_admin='SUPER_ADMIN', label='Super Admin'),
    K(student='STUDENT', label='Student'),
    K(librarian='LIBRARIAN', label='Librarian'),
    )
