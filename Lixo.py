
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

# TODO debugging table
    #in_table=[[['t','x'],['t','y'],['t','z'],['f','x'],['f','y'],['f','z']],[0.9,0.3,0.4,0.1,0.7,0.6]]

# TODO table[0] has the variable instance strings; table[1] corresponds to the probability values
# TODO define: table_product(), find_dependent(), find_equal(), marginalize()
# TODO find_equal() must be able to accept both inputs as lists of strings, not just one list and a string