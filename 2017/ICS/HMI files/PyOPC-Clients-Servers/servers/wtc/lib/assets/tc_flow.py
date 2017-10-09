#Test Tags to see if this is actually working
#Syntax (name, failValue, cmp_op, [previous_nodes], [next_nodes], startValue)
tags = [('PS0_DEST_NET', '0', '==', None, ['TC0_PUMP_0'], '1'),
		('TC0_PUMP_0', '0', '==', ['PS0_DEST_NET'], ['TC0_PUMP_1'], '1'),
        ('TC0_PUMP_1', '0', '==', ['TC0_PUMP_0'], ['TC0_VALVE_0', 'TC0_VALVE_1'], '1'),
        ('TC0_VALVE_0', '0', '==', ['TC0_PUMP_1'], ['TC0_VALVE_2'], '1'),
        ('TC0_VALVE_1', '0', '==', ['TC0_PUMP_1'], ['TC0_VALVE_3'], '1'),
        ('TC0_VALVE_2', '0', '==', ['TC0_VALVE_0'], ['TC0_PUMP_2'], '1'),
        ('TC0_VALVE_3', '0', '==', ['TC0_VALVE_1'], ['TC0_PUMP_2'], '1'),
        ('TC0_PUMP_2', '0', '==', ['TC0_VALVE_2', 'TC0_VALVE_3'], ['TC0_VALVE_4', 'TC0_VALVE_5', 'TC0_VALVE_6'], '1'),
        ('TC0_VALVE_4', '0', '==', ['TC0_PUMP_2'], ['TC0_DEST_NET'], '1'),
        ('TC0_VALVE_5', '0', '==', ['TC0_PUMP_2'], ['TC0_DEST_NET'], '1'),
        ('TC0_VALVE_6', '0', '==', ['TC0_PUMP_2'], ['TC0_DEST_NET'], '1'),
        ('TC0_DEST_NET', '0', '==', ['TC0_VALVE_4', 'TC0_VALVE_5', 'TC0_VALVE_6'], None, '1')]
