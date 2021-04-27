# Utilities
import requests
import time
import urllib


class SourceAPI:
    """
    Bonobo extractor from API
    """
    def __init__(self, url, pagination_param, increase_by, starts_at, stop_at, list_path=None, object_path=None):
        """
        Create a service that will work for any HTTP API
        :param url: service url
        :param pagination_param: keyword use for pagination. For example "page", "offset", "p". String
        :param starts_at: The starting value of pagination_param. Integer
        :param increase_by: The increasing value of pagination_param. Integer
        :param stop_at: The pagination_param value at which extraction should stop. Integer
        :param list_path (optional): Key of the list object in case the API does not return a list. If there are
        multiple steps split it by >. String
        :param object_path (optional): Path to the object key that has the information to be obtained. If there are
        multiple steps split it by >. String
        """
        self.url = urllib.parse.unquote(url)
        self.pagination_param = pagination_param
        self.increase_by = int(increase_by)
        self.starts_at = int(starts_at)
        self.stop_at = int(stop_at)
        self.list_path = list_path.split('>') if list_path else []
        self.object_path = object_path.split('>') if object_path else []
        self.schema = {}

    def __call__(self):
        """
        Perform request to API
        :return: yield an API row element
        """

        # Loop around all pages of API
        for page in range(self.starts_at, self.stop_at + 1, self.increase_by):
            separator = '?' if '?' not in self.url else '&'
            url_ = f'{self.url}{separator}{self.pagination_param}={page}'  # Define page url
            try:
                result = requests.get(url_, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'})  # Perform HTTP GET request
            except Exception as e:
                print("Error with API request:", str(e))
                break
            if result:  # If the request is successful
                result = result.json()  # Obtain API JSON result (Expecting a list)
                for field in self.list_path:
                    result = result[field]
                if result:
                    for row in result:
                        for field in self.object_path:
                            row = row[field]
                        row = {k: row.get(k) for k in self.schema.keys()}
                        yield (row, )
                else:
                    break  # Exit node
            else:
                break  # Exit node
            time.sleep(1)

    def get_schema(self):
        separator = '?' if '?' not in self.url else '&'
        url_ = f'{self.url}{separator}{self.pagination_param}={self.starts_at}'  # Define page url
        result = requests.get(url_, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'})  # Perform HTTP GET request

        result = result.json()  # Obtain API JSON result (Expecting a list)
        for field in self.list_path:
            result = result[field]
        if result:
            for row in result:
                for field in self.object_path:
                    row = row[field]
                    for name, value in row.items():
                        self.schema[name] = str(type(value))
                    return self.schema