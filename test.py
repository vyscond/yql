from yql import YQL
from yql import Filter

f1 = Filter('symbol', 'in', ['YHOO', 'GOOG', 'AAPL'])
f2 = Filter('symbol', 'eq', 'YHOO')
f3 = Filter('startDate', 'eq', '2014-02-11')
f4 = Filter('endDate', 'eq', '2014-02-18')

f1_expected = 'symbol IN ("YHOO", "GOOG", "AAPL")'
f2_expected = 'symbol = "YHOO"'
f3_expected = 'startDate = "2014-02-11"'
f4_expected = 'endDate = "2014-02-18"'

assert str(f1) == f1_expected
assert str(f2) == f2_expected
assert str(f1 + f2) == '{} and {}'.format(f1_expected, f2_expected)
assert str(f1 * f2) == '{} or {}'.format(f1_expected, f2_expected)
assert str(f1 + f2 + f1 + f2) == '{} and {} and {} and {}'.format(
    f1_expected, f2_expected, f1_expected, f2_expected)
assert str(f1 + f2 * f1) == '{} and {} or {}'.format(
    f1_expected, f2_expected, f1_expected)
assert str(f2 + f3 + f4) == '{} and {} and {}'.format(
    f2_expected, f3_expected, f4_expected)

resp1 = YQL('yahoo.finance.quote').select().where(f1).run()
resp2 = YQL('yahoo.finance.historicaldata').select().where(str(f2+f3+f4)).run()

assert resp1['query']['count'] == 3
assert resp2['query']['count'] == 5
