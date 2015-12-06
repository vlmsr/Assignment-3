#  TODO use Python String find() method
from copy import deepcopy

def fileReader(fileName, extension):
    """
    Reads DIMACS formatted files and returns a knowledge base and its parameters
    :param fileName: name of the file to be read
    :param extension: extension of the file to be read
    :return: BN object with clauses, number of clauses and number of variables
    """

    fileName = fileName+extension
    input = open(fileName,'r')
    raw_data = input.readlines()
    input.close()
    print('Loading data...')

    err = 0  # error variable
    clause = []
    start = 0
    k = 0  # for iterations over the clauses
    l = 0  # for iterations over the symbols
    num_clauses = 0
    num_vars = 0
    for i in range(len(raw_data)):
        j = 0
        if raw_data[i][j] == '%':
            if k < num_clauses:
                print("Warning: Number of clauses does not match data!")
                for excess in range(k,num_clauses):
                    clause.pop()
            break  # finishes clause assignment task
        elif raw_data[i][j] != 'c':
            if raw_data[i][j] == 'p':
                first_ind = j  # saves first index
                first_ind = raw_data[i].find(' ', first_ind)  # finds a space
                last_ind = raw_data[i].find(' ', first_ind+1)  # finds another space
                if raw_data[i][first_ind+1:last_ind] == 'cnf':
                    start = 1
                    first_ind = last_ind  # finds a space
                    last_ind = raw_data[i].find(' ', first_ind+1)  # finds another space
                    num_vars = int(raw_data[i][first_ind+1:last_ind])  # saves number of symbols
                    while raw_data[i][last_ind] == ' ':
                        last_ind += 1
                    num_clauses = int(raw_data[i][last_ind:])  # saves number of clauses
                    # start assignment here!
                    clause=[[] for r in range(0,num_clauses)]  # preallocation of clauses
                else:
                    print("Invalid data type: 'cnf' not found!")
                    err = 1
            elif start == 1:
                word = findWord(raw_data[i], ' ', j)
                if k >= num_clauses:
                        print("Warning: Number of clauses does not match data!")
                        break
                while word != -1:
                    if word[0] == 1:  # supposedly the last number on current line will be 0 - this number is discarded
                        break
                    else:
                        clause[k].append(int(raw_data[i][word[1]:word[2]]))  # saves clause
                        j = word[2]  # last checked index
                    word = findWord(raw_data[i], ' ', j)
                k += 1
                if word == -1:
                    print('Error while parsing raw data!')
                    err = 1
    if err == 0:
        print('Data successfully loaded!')
        return KB(num_clauses, num_vars, clause)  # Returns KB object
    else:
        return KB(-1, -1, -1)  # return error sentence


def find_next(var, key, start):  # returns end_cond, w_start (inclusive) and w_end indices (exclusive); key is a string
    """
    Finds the indices where the next word is stored within var
    :param var: Input Variable with type str
    :param key: Specified symbol that separates words
    :param start: Starting Index
    :return: Tuple with status, first and last indices
    """
    endkey = '\n'  # line end character
    j = start
    while var[j] == key:
        j += 1
    w_start = j
    w_end = var.find(key, w_start)
    if w_end == -1:
        w_end = var.find(endkey, w_start)
        if w_end == -1:
            return -1
        elif w_end == w_start:
            return -1
        else:
            interval = (1, w_start, w_end)  # in case end of line is reached
            return interval
    else:
        interval = (0, w_start, w_end)
        return interval

def find_word(var, word, start):
    # Finds the specified word inside var and returns the start and end indices
    for i in range(len(var)):
        if var[i]==word[0]:
            if len(word)>1:
                letter=i+1
                found=1
                for j in range(1,len(word)):
                    if var[letter]!=word[j]
                        found=0
                        break
                if found==1
                    return [i,letter]
    return []


def write_file(filename, extension, algorithm, data):
    """
    Writes data to file using the DIMACS format
    :param filename: name of the file that wil be created
    :param extension: extension of the file that will be created
    :param algorithm: algorithm used to obtain the data
    :param data: Data object with parameters and results
    :return: none
    """
    filename = 'sol_'+filename+'_'+algorithm+extension
    output = open(filename, 'w')
    print('Saving data...')
    output.write('c\n')
    line = 'c Authors: Vasco Rodrigues, Joao Oliveira\n'
    output.write(line)
    output.write('c\n')
    line = 'c Algorithm: '+algorithm+'\n'
    output.write(line)
    output.write('c\n')
    line = 's cnf '+str(data.solution)+' '+str(data.nvars)+' '+str(data.nclauses)+'\n'
    output.write(line)
    line = 't cnf '+str(data.solution)+' '+str(data.nvars)+' '+str(data.nclauses)
    line += ' '+str(data.time)+'\n'
    output.write(line)
    if data.assignment:  # if there is a valid assignment, write it
        for symbol in range(len(data.assignment)):
            output.write('v '+str(data.assignment[symbol])+'\n')
    output.close()
    print(filename+' saved!')

def save_data(filename, extension, algor, data):
    filename = 'sol_'+filename+extension
    output = open(filename, 'a')  # open file for appending
    line = str(algor.name)+' '+str(data.nvars)+' '+str(data.nclauses)
    line += ' '+str(data.ratio)+' '+str(data.time)+' '+str(algor.mrestarts)+' '+str(algor.mflips)+' ' + \
        str(data.solution)+' '+str(algor.flips)
    output.write(line+'\n')  # end with 0
    output.close()
    print('File saved')

def load_data(filename, extension, algorithm):
    filename = filename+extension
    input = open(filename, 'r')  # open file for appending
    raw_data=input.readlines()
    input.close()
    loaddata=[[] for i in range(8)]
    l=0
    for line in range(len(raw_data)):
        if raw_data[line][0]!='c':
            last=0
            w=0
            word = findWord(raw_data[line], ' ', last)
            loaddata[l] = []  # to ensure it is empty
            loaddata[l].append(raw_data[line][word[1]:word[2]])
            last = word[2]
            w+=1
            if loaddata[l][0] == algorithm:
                word = findWord(raw_data[line], ' ', last)
                while word != -1:
                    if word == 1:
                        break
                    elif w == 7:
                        loaddata[l].append(bool(raw_data[line][word[1]:word[2]]))
                        last = word[2]
                        word = findWord(raw_data[line], ' ', last)
                    elif w == 3 or w == 4:
                        loaddata[l].append(float(raw_data[line][word[1]:word[2]]))
                        last = word[2]
                        word = findWord(raw_data[line], ' ', last)
                    else:
                        loaddata[l].append(int(raw_data[line][word[1]:word[2]]))
                        last = word[2]
                        word = findWord(raw_data[line], ' ', last)
                    w+=1
                l+=1
    print(filename+' loaded!')
    return loaddata


def variable_elimination(factors, elim_vars):
    #  TODO initial draft for the variable elimination function
    for i in range(len(elim_vars)):
        factors=sum_prod_elim(factors, elim_vars[i])
    """product=factors[0]
    if len(factors)>1:  # TODO shall we keep this condition? It will hide possible errors, difficult debugging!
        for factor in factors:  # TODO check
            product=table_product(product,factor)
    return product"""
    # TODO verify if elim_vars were eliminated
    return factors

def sum_prod_elim(factors, elim_var):
    [elim_factors, indices]=find_dependent(factors, elim_var)  # TODO define as a method of factors
    indices.sort(reverse=True)  # sort in descending order
    for i in indices:
        factors.pop(i)  # eliminate factors to join
    new_factor=elim_factors[0]
    if len(elim_factors)>1:
        for factor in elim_factors[1:]:  # product of factors to eliminate
            new_factor = table_product(new_factor, factor)
    new_factor = marginalize(new_factor, elim_var)
    return factors+new_factor  # TODO check concatenation method


def no_rep(list_in):
    # remove repeated entries in list
    return list(set(list_in))

def table_product(factor_1, factor_2):
    dependent = find_equal(factor_1.get_vars(), factor_2.get_vars(),'ind')  # TODO revise find_equal output
    # TODO indices=something
    new_factor = Factor('prod', no_rep(factor_1.get_vars() + factor_2.getvars()))
    table_1=factor_1.get_table()
    table_2=factor_2.get_table()
    found=True
    for line1 in range(len(table_1[1])):
        assign1=table_1[0][line1]
        prob1=table_1[1][line1]
        for line2 in range(len(table_2[1])):
            assign2=table_1[0][line2]
            prob2=table_1[1][line2]
            if [line1[i] for i in indices[0]] == [line2[j] for j in indices[1]]:
                new_table[0].append(no_rep(line1+line2))
                new_table[1].append(no_rep(line1+line2))


            for d in range(len(dependent)):
                if factor_1.get_vars()[dependent[d][0]]!=factor_2.get_vars()[dependent[d][1]]:
                    found=False
                else:


            if found:

                    new_table[0].append(no_rep(factor_1.get_table()[0][i] * factor_2.get_table()[0][j]))
                    new_table[1].append(factor_1.get_table()[1][i]*factor_2.get_table()[1][j])

                    # TODO CONTINUE HERE!!!!!!


            if factor_2.get_table()[0][j].find(factor_1.get_table()[0][i]):
                new_factor.table[1][i]=factor_1.table[1][i]*factor_2.table[1][j]  # TODO verify what to do with non-dependent vars during multiplication process!
                new_factor.table[0][i]=list(set(factor_1.table[1][i]+factor_2.table[1][j]))
    return factor_1
# TODO table[0] has the variable instance strings; table[1] corresponds to the probability values
# TODO define: table_product(), find_dependent(), find_equal(), marginalize()
# TODO find_equal() must be able to accept both inputs as lists of strings, not just one list and a string
class BN(object):
    def __init__(self):
        self.__name='default'
        self.__num_nodes=0
        self.__node=[]
    def addNode(self,node_id,name,values,alias,parents):
        self.__node.append(Node(name,values,alias,parents))
        self.__node[-1].node_id=node_id  # TODO check if necessary

class Node(object):
    def __init__(self,name,values,alias,parents):
        self.__name=name
        self.__values=values
        self.__alias=alias
        self.__parents=parents  # parents' alias
        self.__children=[]
        self.__id=-1
        self.__prob_table=[[], []]  # initialize empty table

    def create_table(self, raw_table):
        """for i in range(len(raw_table)):
            if i%2 > 0:
                self.__prob_table[0].append=raw_table[i]
            else:
                self.__prob_table[1].append=raw_table[i]"""

    def fill_table(self, in_table):
        self.__prob_table=deepcopy(in_table)

    def update(self,parents,children):
        # TODO update - still not sure how to do it
    def def_id(self, new_id):
        self.__id=new_id
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

class Factor(object):
    def __init__(self,description,var):
        self.__description=description
        self.__var=var
        self.__prob_table=[[], []]  # initialize empty table

    def fill_table(self, in_table):
        self.__prob_table=deepcopy(in_table)
    """def update(self,parents,children):
        # TODO update - still not sure how to do it"""
    def get_description(self):
        return self.__description
    def get_vars(self):
        return self.__var
    def get_table(self):
        return self.__prob_table

    # TODO debugging table
    #in_table=[[['t','t','t','f','f','f'],['x','y','z','x','y','z']],[0.9,0.3,0.4,0.1,0.7,0.6]]