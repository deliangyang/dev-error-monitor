# -*-- coding:utf-8 -*--
# https://docs.ponyorm.org/api_reference.html#attribute-types
from pony.orm import *


db = Database()


class ErrorLog(db.Entity):
    id = PrimaryKey(int, auto=True)
    md5 = Required(str, max_len=32)
    env = Required(str, max_len=10)
    error = Required(str, max_len=2048)
    times = Required(int)
    create_time = Required(int)
    composite_key(md5, env)


db.bind(provider='sqlite', filename='log.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
