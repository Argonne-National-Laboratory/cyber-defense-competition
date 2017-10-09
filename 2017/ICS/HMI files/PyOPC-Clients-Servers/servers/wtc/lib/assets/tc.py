#Test Tags to see if this is actually working
#Syntax (name, failValue, cmp_op, [previous_nodes], [next_nodes], startValue)
tags = [('WTC_0', 0, '==', None, ['WTC_1','WTC_2','WTC_3'], 30),
        ('WTC_1', 0, '==', ['WTC_0'], ['WTC_4'], 30),
        ('WTC_2', 10, '>', ['WTC_0'], ['WTC_4'], 30),
        ('WTC_3', 0, '==', ['WTC_0'], ['WTC_4'], 30),
        ('WTC_4', 0, '==', ['WTC_1','WTC_2','WTC_3'], ['WTC_5'],30),
        ('WTC_5', 4, '>=', ['WTC_4'], None, 10)]
