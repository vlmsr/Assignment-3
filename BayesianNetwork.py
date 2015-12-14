from Reasoner import*

# Sample Bayesian Network
burgl = Node('Burglary', ['t', 'f'], 'B', [], ['Alarm'])
burgl.add_vars(['Burglary'])
burgl.fill_table([[['t'], ['f']], [0.001, 0.999]])
earthq = Node('Earthquake', ['t', 'f'], 'E', [], ['Alarm'])
earthq.add_vars(['Earthquake'])
earthq.fill_table([[['t'], ['f']], [0.002, 0.998]])
alarm = Node('Alarm', ['t', 'f'], 'A', ['Earthquake', 'Burglary'], ['JohnCalls', 'MaryCalls'])
alarm.add_vars(['Alarm', 'Burglary', 'Earthquake'])
alarm.fill_table([[['t', 't', 't'], ['t', 't', 'f'], ['t', 'f', 't'], ['t', 'f', 'f'],\
                   ['f', 't', 't'], ['f', 't', 'f'], ['f', 'f', 't'], ['f', 'f', 'f']], [0.95, 0.94, 0.29, 0.001,\
                                                                                         0.05, 0.06, 0.71, 0.999]])
johncalls = Node('JohnCalls', ['t', 'f'], 'J', ['Alarm'], [])
johncalls.add_vars(['JohnCalls', 'Alarm'])
johncalls.fill_table([[['t', 't'], ['t', 'f'], ['f', 't'], ['f', 'f']], [0.90, 0.05, 0.10, 0.95]])
marycalls = Node('MaryCalls', ['t', 'f'], 'M', ['Alarm'], [])
marycalls.add_vars(['MaryCalls', 'Alarm'])
marycalls.fill_table([[['t', 't'], ['t', 'f'], ['f', 't'], ['f', 'f']], [0.70, 0.01, 0.30, 0.99]])
# (table[0] has the variable instance strings; table[1] corresponds to the probability values)

# Query and evidence definition
query_var = burgl
evidence = [[johncalls, marycalls], ['t', 't']]

nodes = [burgl, earthq, alarm, johncalls, marycalls]

print('== Probabilistic Reasoner based on Bayesian Networks ==')
print('\n(no input file parser available yet)')
print('\nQuery variable:')
print(query_var.get_name())
print('\nEvidence:')
evidence_names = []
for node in evidence[0]:
    evidence_names.append(node.get_name())
print(evidence_names)

factors = nodes2factors(nodes)
factors = propagate_evidence(factors, evidence)

ordering = order(query_var, evidence[0], nodes)
query_prob = variable_elimination(factors, ordering)
print('\n------------------')
print('Query | evidence probability table:')
for value_line, prob_line in zip(query_prob.get_table()[0], query_prob.get_table()[1]):
    print([value_line, [prob_line]])
