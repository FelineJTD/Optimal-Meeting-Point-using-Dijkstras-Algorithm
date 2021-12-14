def CFGtoCNF(CFG):
    # KAMUS
    # CFG: dict of CFG rules
    terminals = CFG.keys()
    # ALGORITMA
    CNF = {}
    counter = 1
    for key in CFG.keys():
        term = []
        nonterm = []

        for i in CFG[key]:
            if (type(i)!=list):
                if (i in terminals):
                    term.append(i)
                else:
                    nonterm.append(i)
        
        if (len(term)==0 and len(nonterm)>=1): #only nonterminals in one production rule
            CNF[key] = [" ".join(map(str, nonterm))]
        
        if (len(nonterm) == 0): #only terminals in one production rule
            if (len(term)>=1 and len(term)<=2): #2 or less terminals
                CNF[key] = CFG[key]
            else: #more than 2 terminals
                CNF[key] = []
                temp = []
                while(len(term)>1):
                    temp.append([term[0], term[1]])
                    CNF[key].append(f"A{counter}")
                    term.pop(0)
                    term.pop(1)
                    counter += 1
                


        if (len(term)>0 and len(nonterm)>0): #terminals and nonterminals in one production rule
            for j in term:
                CNF[f"A{counter}"] = j
                counter += 1


        if (type(i[0])==list):
            print(i)
    
    return(CNF)

def divideByTwos(l, counter):
    temp = []
    result = {}

    

    if (len(temp)<=2): #basis
        result[f"A{counter}"] = l
        counter += 1
    else:
        while (len(l)>1):
            temp.append([l[0],l[1]])
            temp.pop(0)
            temp.pop(1)
        if (len(l)==1): #sisa 1
            temp.append(l(0))

    while (len(l)>1):
        result[f"A{counter}"] = 
    return (result, counter)

R = { 
    "TEST": ["Hello", "World"],
    "TEST2": ["Testing"],
    "S" : ["IF", "ELIF", "ELSE"],
    "IF": ["if", "BOOL", ":", "DO"],
    "ELIF": [["elif", "BOOL", ":", "DO", "ELIF"], 
            [""]],
    "ELSE": [["else", "BOOL", ":", "DO"],
            [""]],
    "BOOL": [["True"],["False"]],
    "DO": ["Do smth"]
    } 

print(CFGtoCNF(R))