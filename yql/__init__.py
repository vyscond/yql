import requests

class Filter(object):
    
    '''
    =	Equal.
    !=	Not equal.
    >	Greater than.
    <	Less than.
    >=	Greater than or equal to.
    <=	Less than or equal to.
    --------------------------------------------------------------------------
    [NOT] IN	Tests whether a value is contained in a set of values. 
                This operator can be followed by either a sub-select or by a 
                comma-delimited set of values within parentheses.
    --------------------------------------------------------------------------
    IS [NOT] NULL	Tests for the existence of the field in the results. 
                    An IS NULL expression is true if the field is not in the 
                    results.
    --------------------------------------------------------------------------
    [NOT] LIKE	Tests for a string pattern match. The comparison is 
                case-insensitive. The "%" character in the literal indicates 
                zero or more characters. For example, Sys% matches any string 
                starting with Sys.
    --------------------------------------------------------------------------
    [NOT] MATCHES	Tests for a string pattern match, allowing regular 
                    expressions. The comparison is case sensitive.
    '''
    
    def __init__(self, field, operator, value, on_quotes=True):
        self.on_quotes = on_quotes
        self.sql = ''
        self.field = field
        self.operator = operator
        self.value = value
        getattr(self, '_Filter__{}'.format(self.operator))()

    def __in(self):
        if type(self.value) == list:
            if self.on_quotes:
                self.value = ['"{}"'.format(val) for val in self.value]
            self.value = ', '.join(self.value)
            self.value = '({})'.format(self.value)
            self.operator = 'IN'
        else:
            raise Exception('Wrong type of value for IN operator')

    def __not_in(self):
        self.__in()
        self.operator = 'not in'

    def __gt(self):
        if self.on_quotes:
            self.value = '"{}"'.format(self.value)
        self.operator = '>'

    def __gte(self):
        if self.on_quotes:
            self.value = '"{}"'.format(self.value)
        self.operator = '>='

    def __lt(self):
        if self.on_quotes:
            self.value = '"{}"'.format(self.value)
        self.operator = '<'
        
    def __lte(self):
        if self.on_quotes:
            self.value = '"{}"'.format(self.value)
        self.operator = '<='

    def __not_eq(self):
        if self.on_quotes:
            self.value = '"{}"'.format(self.value)
        self.operator = '!='

    def __eq(self):
        if self.on_quotes:
            self.value = '"{}"'.format(self.value)
        self.operator = '='

    def __concat__(self, other):
        return '{} and {}'.format(str(self), other)

    def __add__(self, other):
        return '{} and {}'.format(str(self), str(other))

    def __radd__(self, other):
        return '{} and {}'.format(str(other), str(self))

    def __mul__(self, other):
        return  '{} or {}'.format(str(self), str(other))

    def __str__(self):
        return '{} {} {}'.format(self.field, self.operator, self.value)


class YQL(object):
    
    def __init__(self, table):
        self.url = 'https://query.yahooapis.com/v1/public/yql'
        self.env = 'store://datatables.org/alltableswithkeys'
        self.table = table
        
    def select(self, columns=['*']):
        self.columns = ', '.join(columns)
        return self

    def where(self, conditions=''):
        if conditions:
            self.conditions = 'where {}'.format(str(conditions))
        return self

    def encode_url(self):
        self.query = '{}?q=select {} from {} {}'.format(self.url, self.columns,
            self.table, self.conditions)
        self.query = self.query.replace(' ','%20')\
                               .replace('"', '%22')\
                               .replace(',', '%2C')

    def run(self, format_='json', callback=''):
        self.encode_url()
        params = {'format': format_, 'callback': callback, 'env': self.env}
        return requests.get(self.query, params=params).json()
