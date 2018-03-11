# import sqlalchemy as db
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Model(Base):

#     pk = db.Column('pk', db.Integer, primary_key=True, nullable=False)


# class TestModel(Model):

#     __tablename__ = 'test'

#     test_field = db.Column('testfield', db.String(40), nullable=False)
#     test_field2 = db.Column('testfield2', db.String(40), nullable=False)

#     def __str__(self):
#         return 'testing'

# TestModel.__table__.create(engine)

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

class Model(object):

    def __init__(self):
        super().__init__()
        self = declarative_base(name=self.name, metaclass=DeclarativeMeta)


class MyModel(Model):

    __tablename__ = 'test'
    name = 'test'

    test_field = db.Column('testfield', db.String(40), nullable=False)
    test_field2 = db.Column('testfield2', db.String(40), nullable=False)


# mymodel = MyModel()
# print(mymodel)


    # class Model(db.Model):

    #     pk = db.Column('pk', db.Integer, primary_key=True, nullable=False)
    # model = declarative_base(
    #                 cls=model,
    #                 name='Model',
    #                 metadata=metadata,
    #                 metaclass=DefaultMeta
    #             )

    #  self.Model = self.make_declarative_base(model_class, metadata)