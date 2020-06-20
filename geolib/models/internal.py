from enum import IntEnum


class Bool(IntEnum):
    FALSE = 0
    TRUE = 1

    # TODO Commented out because debugging crashes on this
    # def __getattribute__(self, name):
    #     if isinstance(name, bool):
    #         if name:
    #             name = "TRUE"
    #         else:
    #             name = "FALSE"
    #     return super().__getattribute__(name)
