from Reader import*
burgl = Node('Burglary', ['t', 'f'], 'B', [], ['Alarm'])
burgl.fill_table([[['t'], ['f']], [0.001, 0.999]])
earthq = Node('Earthquake', ['t', 'f'], 'E', [], ['Alarm'])
earthq.fill_table([[['t'], ['f']], [0.002, 0.998]])
alarm = Node('Alarm', ['t', 'f'], 'A', ['Earthquake', 'Burglary'], ['JohnCalls', 'MaryCalls'])
alarm.fill_table([[['t', 't'], ['t', 'f'], ['f', 't'], ['f', 'f']], [0.95, 0.94, 0.29, 0.001]])
johncalls = Node('JohnCalls', ['t', 'f'], 'J', ['Alarm'], [])
johncalls.fill_table([[['t'], ['f']], [0.90, 0.05]])
marycalls = Node('MaryCalls', ['t', 'f'], 'M', ['Alarm'], [])
marycalls.fill_table([[['t'], ['f']], [0.70, 0.01]])

nodes = [burgl, earthq, alarm, johncalls, marycalls]
factors = nodes2factors(nodes)

# TODO debugging table
    #in_table=[[['t','x'],['t','y'],['t','z'],['f','x'],['f','y'],['f','z']],[0.9,0.3,0.4,0.1,0.7,0.6]]