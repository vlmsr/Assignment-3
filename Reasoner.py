
from copy import deepcopy


def propagate_evidence(factors, evidence):
    evidence_names = []
    for node in evidence[0]:
        evidence_names.append(node.get_name())
    for factor in factors:
        equal = find_equal(factor.get_vars(), evidence_names, 'ind')
        if equal[0]:
            temp_table = [[], []]
            for var0, var1 in zip(equal[0], equal[1]):
                    for line, line2 in zip(factor.get_table()[0], factor.get_table()[1]):
                        if line[var0] == evidence[1][var1]:
                            temp_table[0].append(line)
                            temp_table[1].append(line2)
            factor.fill_table(temp_table)
    return factors


def variable_elimination(factors, elim_vars):
    """
    Variable Elimination algorithm
    :param factors: initial factors (list of Factor objects)
    :param elim_vars: ordering of variables to eliminate (list of Node objects)
    :return: final factor with query probability (Factor object)
    """
    for i in range(len(elim_vars)):
        factors = sum_prod_elim(factors, elim_vars[i])
    final_prob = join_normalize(factors)
    return final_prob


def join_normalize(factors):
    new_factor = deepcopy(factors[0])
    factor = []
    if len(factors)>1:
        for factor in factors[1:]:  # product of factors to join
            new_factor = table_product(new_factor, factor)
    new_factor = table_product(new_factor, factor)
    table = new_factor.get_table()
    total = sum(table[1])
    for i in range(len(table[1])):
        table[1][i] = table[1][i]/total
    new_factor.fill_table(table)
    return new_factor


def sum_prod_elim(factors, elim_var):
    [elim_factors, indices] = find_dependent(factors, elim_var.get_name())
    if elim_factors:
        indices.sort(reverse=True)  # sort in descending order
        for i in indices:
            factors.pop(i)  # eliminate factors to join
        new_factor = elim_factors[0]
        if len(elim_factors) > 1:
            for factor in elim_factors[1:]:  # product of factors to eliminate
                new_factor = table_product(new_factor, factor)
        new_factor = marginalize(new_factor, elim_var)
        factors.append(new_factor)
    return factors


def find_dependent(factors, var):
    """
    Finds factors that depend on the specified variable
    :param factors: list of Factor-type objects to search
    :param var: variable to search for
    :return: dependent factors (Factor objects list) and indices of dependent factors (list) from the 'factors' list
    """
    dep_factors = []
    dep_indices = []
    for i in range(len(factors)):
        ind = find_equal(factors[i].get_vars(), [var], 'ind')  # return matching indices
        if ind[0]:
            dep_factors.append(factors[i])  # concatenate matching factors
            dep_indices.append(i)
    return [dep_factors, dep_indices]


def no_rep(list_in):
    # remove repeated entries in list
    list_out = []
    for i in list_in:
        if i not in list_out:
            list_out.append(i)
    return list_out


def find_equal(list1, list2, out_type):
    """
    Finds matching elements in both lists and returns either a list of matched elements or a list of indices
    :param list1: first list to compare
    :param list2: second list to compare
    :param out_type: if ind='ind' is specified, the function returns matched indices instead of matched elements
    :return: list of matched elements or list of indices, depending on the 'ind' parameter
    """
    if out_type == 'ind':
        indices = [[], []]
        for i in range(len(list1)):
            for j in range(len(list2)):
                if list1[i] == list2[j]:
                    indices[0].append(i)
                    indices[1].append(j)
        return indices
    else:
        list_out = []
        for i in range(len(list1)):
            for j in range(len(list2)):
                if list1[i] == list2[j]:
                    list_out.append(list1[i])
        return list_out


def table_product(factor_1, factor_2):
    """
    Computes the product between the probability tables of 2 factors and returns a new factor with that table
    :param factor_1: 1st factor (Factor object)
    :param factor_2: 2nd factor (Factor object)
    :return: resulting factor (Factor object)
    """
    dependent = find_equal(factor_1.get_vars(), factor_2.get_vars(), 'ind')  # return matched indices
    new_factor = Factor('prod', no_rep(factor_1.get_vars() + factor_2.get_vars()))
    table_1 = factor_1.get_table()
    table_2 = factor_2.get_table()
    new_table = [[],[]]
    for line1 in range(len(table_1[1])):
        assign1 = deepcopy(table_1[0][line1])
        prob1 = deepcopy(table_1[1][line1])
        for line2 in range(len(table_2[1])):
            assign2 = deepcopy(table_2[0][line2])
            prob2 = deepcopy(table_2[1][line2])
            if [assign1[i] for i in dependent[0]] == [assign2[j] for j in dependent[1]]:  # if equal assignments found
                erase = sorted(dependent[1], reverse=True)  # dependent elements to erase from one of the tables
                for elem in erase:
                    assign2.pop(elem)
                new_table[0].append(assign1+assign2)
                new_table[1].append(prob1*prob2)
    new_factor.fill_table(new_table)
    return new_factor



def marginalize(factor, elim_var):
    """
    Marginalizes specified variable
    :param factor: factor from which the variable will be eliminated (Factor object)
    :param elim_var: name of the variable to eliminate (string)
    :return: updated factor (Factor object)
    """
    factor.eliminate(elim_var.get_name())
    new_table = [[], []]
    table = factor.get_table()
    tabu = [False for i in range(len(table[0]))]
    new_line = 0
    for line in range(len(table[0])):
        if not tabu[line]:
            tabu[line] = True
            for line1 in range(len(table[0])):
                if not tabu[line1]:
                    if table[0][line] == table[0][line1]:
                        tabu[line1] = True
                        if len(new_table[0]) == new_line:
                            new_table[0].append(table[0][line])
                            new_table[1].append(table[1][line]+table[1][line1])
                        else:
                            new_table[1][new_line] += new_table[1][line1]  # sum the matched values
            new_line += 1  # increment new_table index
    factor.fill_table(new_table)
    return factor


def order(query, evidences, nodes):
    """
    Finds hidden variables (not query or evidence), finds an elimination order according to a heuristic
     and returns a list of nodes to eliminate, sorted in the chosen order.
    :param query: query variable (Node object)
    :param evidences: list of evidence variables (list of Node objects)
    :param nodes: list of all nodes (list of Node objects)
    :return: sorted list with an ordering of nodes to eliminate (list of Node objects)
    """
    elim_vars = []
    hidden_vars = []
    # create list elim_vars of Hidden Vars (not Query or Evidence)
    evidence_name=[]
    for evidence in evidences:
        evidence_name.append(evidence.get_name())  # list with names of evidence variables
    for node in nodes:
        if not find_equal([query.get_name()], [node.get_name()], 'val'):
            if not find_equal(evidence_name, [node.get_name()], 'val'):
                hidden_vars.append(node)  # add node to list of variables to sort for elimination
    evaluation = heuristic(hidden_vars, query, evidence_name)
    #[[elim_var(i),cost(i)],...]=heuristic(hidden_vars)
    evaluation.sort(key=lambda x: x[1])
    if len(evaluation) > 1:
        evaluation_range = list(range(len(evaluation)))  # auxiliary variable
        for i in evaluation_range:
            elim_vars.append(evaluation.pop(0)[0])  # add best-rated var to the elimination list
            if evaluation:
                evaluation = heuristic(get_2nd_elem(evaluation, 0), query, evidences)  # evaluate heuristic for the new situation
                evaluation.sort(key=lambda x: x[1])
    return elim_vars


def get_2nd_elem(in_list, index):
    out_list = []
    for entry in in_list:
        out_list.append(entry[index])
    return out_list


def heuristic(hidden_vars, query, evidence_name):
    """
    Computes heuristic costs
    :param hidden_vars: hidden variables (list of Node objects)
    :param query: query variable (Node object)
    :param evidence_name: names of evidence variables (list of strings)
    :return: list with hidden variables and respective costs
    """
    evaluation = []
    for variable in hidden_vars:
        parents_ev = find_equal(variable.get_parents(), evidence_name, 'val')  # parents of 'variable' that are evidence
        children_ev = find_equal(variable.get_children(), evidence_name, 'val')  # children of 'variable' that are evidence
        child_parents = []
        for child in variable.get_children():
            for h_var in hidden_vars:
                if find_equal([child], [h_var.get_name()], 'var'):  # search the hidden variables for the child node
                    child_parents += h_var.get_parents()  # add parents of children node to list
            if find_equal([child], [query.get_name()], 'var'):    # check it h_var matches the query var
                child_parents += query.get_parents()
            child_parents = list(set(child_parents))  # remove repeated values
        equal = find_equal(child_parents, parents_ev+children_ev,'ind')  # check for equal values in both lists
        if equal[0]:
            equal[0].sort(reverse=True)
            for index in equal[0]:  # this assumes a parent can never be also a child of the current node
                child_parents.pop(index)
        equal = find_equal(child_parents, [variable.get_name()], 'ind')  # check if the current variable is included in the list
        if equal[0]:
            child_parents.pop(equal[0][0])  # eliminate the variable that shouldn't be in the list
        valid_neighbors = list(set(variable.get_parents()+variable.get_children()+child_parents))
        cost = len(valid_neighbors)-len(parents_ev+children_ev)
        evaluation.append([variable, cost])
    return evaluation


class BN(object):
    def __init__(self):
        self.__name='default'
        self.__num_nodes=0
        self.__node=[]
    def addNode(self,node_id,name,values,alias,parents):
        self.__node.append(Node(name,values,alias,parents))
        self.__node[-1].node_id=node_id


class Node(object):
    def __init__(self, name, values, alias, parents, children):
        self.__name = name
        self.__values = values
        self.__alias = alias
        self.__parents = parents  # parents' alias
        self.__children = children
        self.__id = -1
        self.__prob_table = [[], []]  # initialize empty table
        self.__vars = []

    def create_table(self, raw_table):
        """for i in range(len(raw_table)):
            if i%2 > 0:
                self.__prob_table[0].append=raw_table[i]
            else:
                self.__prob_table[1].append=raw_table[i]"""
    def add_vars(self, vars):
        self.__vars = vars

    def add_child(self, child):
        self.__children.append(child)

    def add_children(self, children):
        self.__children += children

    def fill_table(self, in_table):
        self.__prob_table = deepcopy(in_table)

    def def_id(self, new_id):
        self.__id = new_id

    def get_vars(self):
        return self.__vars

    def get_name(self):
        return self.__name

    def get_parents(self):
        return self.__parents

    def get_children(self):
        return self.__children

    def get_id(self):
        return self.__id

    def get_table(self):
        return self.__prob_table

    def get_alias(self):
        return self.__alias


def nodes2factors(nodes):
    """
    Creates a list of Factor objects from a list of Node objects
    :param nodes: list of Node objects
    :return: list of Factor objects
    """
    factors = [[] for j in range(len(nodes))]
    i = 0
    for node in nodes:
        factor = Factor('initial', node.get_vars())
        factor.fill_table(node.get_table())
        factors[i] = factor
        i += 1
    return factors


class Factor(object):
    def __init__(self, description, var_list):
        self.__description = description
        self.__vars = var_list
        self.__prob_table = [[], []]  # initialize empty table

    def fill_table(self, in_table):
        self.__prob_table = deepcopy(in_table)

    def eliminate(self, var):
        var_ind = self.__vars.index(var)
        self.__vars.pop(var_ind)
        for i in range(len(self.__prob_table[0])):
            self.__prob_table[0][i].pop(var_ind)

    def get_description(self):
        return self.__description

    def get_vars(self):
        return self.__vars

    def get_table(self):
        return self.__prob_table


