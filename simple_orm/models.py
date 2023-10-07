import json
import sqlite3

db_name = 'db.sqlite3'


def simple_orm(class_:type):
    class_.objects.__createTable__()
    return class_


class ListOfObjects:
    def __init__(self, objects):
        self.objects = objects

    def filter(self, **kwargs):
        filtered_objects = []
        for obj in self.objects:
            # Check if all specified attributes and their values match
            if all(getattr(obj, attr, None) == value for attr, value in kwargs.items()):
                filtered_objects.append(obj)
        return ListOfObjects(filtered_objects)

    def delete(self):
        for obj in self.objects:
            obj.delete()

    def json(self):
        object_dicts = [obj.json() for obj in self.objects]
        return object_dicts


class Object:
    def __init__(self, object_type):
        self.object_type = object_type

    def add(self, obj):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        object_type_name = self.object_type.__name__
        insert_sql = f'INSERT INTO {object_type_name} ({", ".join(obj.__dict__.keys())}) VALUES ({", ".join(["?"] * len(obj.__dict__))});'

        values = tuple(obj.__dict__.values())

        cursor.execute(insert_sql, values)
        conn.commit()
        conn.close()

    def get(self, **kwargs):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        object_type_name = self.object_type.__name__

        attr_value_pairs = [(attr, value) for attr, value in kwargs.items()]

        where_clauses = [f'{attr} = ?' for attr, _ in attr_value_pairs]
        where_clause = ' AND '.join(where_clauses)
        select_by_attrs_sql = f'SELECT * FROM {object_type_name} WHERE {where_clause};'

        values = tuple(value for _, value in attr_value_pairs)

        cursor.execute(select_by_attrs_sql, values)
        row = cursor.fetchone()
        conn.close()

        if row:
            obj = self.object_type()
            for i, value in enumerate(row):
                setattr(obj, cursor.description[i][0], value)
            return obj
        else:
            return None

    def delete(self, **kwargs):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        object_type_name = self.object_type.__name__

        attr_value_pairs = [(attr, value) for attr, value in kwargs.items()]

        where_clauses = [f'{attr} = ?' for attr, _ in attr_value_pairs]
        where_clause = ' AND '.join(where_clauses)
        delete_by_attrs_sql = f'DELETE FROM {object_type_name} WHERE {where_clause};'
        values = tuple(value for _, value in attr_value_pairs)

        cursor.execute(delete_by_attrs_sql, values)
        conn.commit()
        conn.close()

    def filter(self, **kwargs):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        object_type_name = self.object_type.__name__

        attr_value_pairs = [(attr, value) for attr, value in kwargs.items()]

        where_clauses = [f'{attr} = ?' for attr, _ in attr_value_pairs]
        where_clause = ' AND '.join(where_clauses)
        select_by_attrs_sql = f'SELECT * FROM {object_type_name} WHERE {where_clause};'

        values = tuple(value for _, value in attr_value_pairs)

        cursor.execute(select_by_attrs_sql, values)
        rows = cursor.fetchall()
        conn.close()

        objects = []
        for row in rows:
            obj = self.object_type()
            for i, value in enumerate(row):
                setattr(obj, cursor.description[i][0], value)
            objects.append(obj)

        return ListOfObjects(objects)

    def all(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        object_type_name = self.object_type.__name__
        select_all_sql = f'SELECT * FROM {object_type_name};'

        cursor.execute(select_all_sql)
        rows = cursor.fetchall()
        conn.close()

        objects = []
        for row in rows:
            obj = self.object_type()
            for i, value in enumerate(row):
                setattr(obj, cursor.description[i][0], value)
            objects.append(obj)

        return ListOfObjects(objects)

    def __createTable__(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        custom_fields = []
        for key, value in vars(self.object_type).items():
            if not key.startswith("__") and not callable(value):
                field_name = key
                field_type = value.field_type
                is_unique = value.unique
                is_primary_key = value.primary_key
                is_null = value.null
                default_value = value.default

                field_declaration = [f'"{field_name}" {field_type}']

                if is_primary_key:
                    field_declaration.append('PRIMARY KEY')
                if is_unique:
                    field_declaration.append('UNIQUE')
                if not is_null:
                    field_declaration.append('NOT NULL')
                if default_value is not None:
                    field_declaration.append(f'DEFAULT {default_value}')

                custom_fields.append(' '.join(field_declaration))

        create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS {self.object_type.__name__} (
            {", ".join(custom_fields)}
        );
        '''

        cursor.execute(create_table_sql)

        conn.commit()
        conn.close()


class ProxyObjects:
    def __get__(self, instance, owner):
        return Object(owner)


class Model:
    objects = ProxyObjects()

    def __init__(self, *args, **kwargs):
        fields = [el for el in vars(self.__class__) if not el.startswith("__")]
        for i, value in enumerate(args):
            setattr(self, fields[i], value)

        for field, value in kwargs.items():
            setattr(self, field, value)

    def json(self):
        attributes = {}
        for key, value in vars(self).items():
            if not key.startswith("__") and not callable(value):
                attributes[key] = value

        return attributes


class IntegerField:
    field_type = 'INTEGER'

    def __init__(self, unique: bool = False, primary_key: bool = False, null: bool = True, default: int = None):
        self.unique = unique
        self.primary_key = primary_key
        self.null = null
        self.default = default


class TextField:
    field_type = 'TEXT'

    def __init__(self, unique: bool = False, primary_key: bool = False, null: bool = True, default: str = None):
        self.unique = unique
        self.primary_key = primary_key
        self.null = null
        self.default = default


class BlobField:
    field_type = 'BLOB'

    def __init__(self, unique: bool = False, primary_key: bool = False, null: bool = True, default: bool = None):
        self.unique = unique
        self.primary_key = primary_key
        self.null = null
        self.default = default


class RealField:
    field_type = 'REAL'

    def __init__(self, unique: bool = False, primary_key: bool = False, null: bool = True, default: float = None):
        self.unique = unique
        self.primary_key = primary_key
        self.null = null
        self.default = default


class NumericField:
    field_type = 'NUMERIC'

    def __init__(self, unique: bool = False, primary_key: bool = False, null: bool = True, default: float = None):
        self.unique = unique
        self.primary_key = primary_key
        self.null = null
        self.default = default
