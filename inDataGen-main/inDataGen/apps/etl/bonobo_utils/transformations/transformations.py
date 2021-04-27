# Utilities
import hashlib
import random
from faker import Faker


class Transformations:
    """
    Class used to apply any transformation over a row with an specific schema
    """

    # Transformations available
    HASH = 'Hash'
    FAKE = 'Fake'
    PASSTHROUGH = 'Passthrough'
    RANDOM = 'Random'
    LINK = 'Link'
    OPTIONS = 'Options'

    def __init__(self, trans_schema, random_val=1, max_val=100000):
        """
        Defines what transformation is going to be applied to each row
        """
        self.trans_schema = {}
        for field, transformation in trans_schema.items():
            if transformation['name'] == self.HASH:
                self.trans_schema[field] = {'function': self.hash, 'props': transformation}
            elif transformation['name'] == self.FAKE:
                self.trans_schema[field] = {'function': self.fake, 'props': transformation}
            elif transformation['name'] == self.PASSTHROUGH:
                self.trans_schema[field] = {'function': self.passthrough, 'props': transformation}
            elif transformation['name'] == self.RANDOM:
                self.trans_schema[field] = {'function': self.random, 'props': transformation}
            elif transformation['name'] == self.OPTIONS:
                self.trans_schema[field] = {'function': self.options, 'props': transformation}
            elif transformation['name'] == self.LINK:
                self.trans_schema[field] = {'function': self.link, 'props': transformation}

        self.fake = Faker()
        self.random_val = random_val
        self.max_val = max_val

    def __call__(self, *row, **kwargs):
        """
        Method call by bonobo for each row in ETL
        :param row: Tuple with a dict in first element
        :param kwargs:
        :return: Same row transformed
        """

        row = row[0]
        for field, transformation in self.trans_schema.items():
            row[field] = transformation['function'](row[field], **transformation['props'])

        return (row, )

    @staticmethod
    def passthrough(field, **kwargs):
        """
        Don't transform the row
        :param field: Field value
        :param kwargs:
        :return: Field value
        """
        return field

    @staticmethod
    def hash(field, **kwargs):
        """
        Hash field
        :param field: field value
        :param kwargs:
        :return: Field hashed
        """
        hash_object = hashlib.sha1(str(field).encode())
        return hash_object.hexdigest()

    @staticmethod
    def random(field, **kwargs):
        """
        Return a random number
        :param field: Original value
        :param kwargs: Type of the field (integer or float)
        :return: Return a random integer or float
        """
        if kwargs.get('type', '') == 'integer':
            return random.randint(1, 9999999)
        if kwargs.get('type', '') == 'float':
            return random.random() * random.randint(1, 9999999)
        else:
            return field

    @staticmethod
    def options(field, **kwargs):
        """
        Randomly select a value from a list
        :param field: original value
        :param kwargs: options list
        :return: random value from the list
        """
        return random.choice(kwargs.get('options', ['']))

    def link(self, field, **kwargs):
        """
        Return a new integer value based on random seeds
        :param field: Original value
        :param kwargs:
        :return: New integer value
        """

        random.seed(field + self.random_val)
        return self.max_val + random.randint(1, 999999) * self.random_val

    def fake(self, field, **kwargs):
        """
        Use Faker library to return a fake value
        :param field: Original value
        :param kwargs: Faker provider name
        :return: Fake value
        """
        if kwargs.get('faker_params'):
            return getattr(self.fake, kwargs.get('type', 'username'))(kwargs['faker_params'])
        else:
            return getattr(self.fake, kwargs.get('type', 'username'))()
