#-*-coding:UTF-8-*-
#!/bin/python
from hamal.db import models as db_models


def create_all_table(eng):
    db_models.Base.metadata.create_all(eng)


def drop_all_table(eng):
    db_models.Base.metadata.drop_all(eng)

