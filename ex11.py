import itertools

class Node:
    def __init__(self, data, pos=None, neg=None):
        self.data = data
        self.positive_child = pos
        self.negative_child = neg

    def get_data(self):
        return self.data

    def get_pos(self):
        return self.positive_child

    def get_neg(self):
        return self.negative_child

    def set_data(self,data):
        self.data = data

    def set_neg(self,node):
        self.negative_child = node

    def set_pos(self,node):
        self.positive_child = node


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms

    def get_symp(self):
        return self.symptoms

    def get_illness(self):
        return self.illness

def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        self.root = root

    def diagnose(self, symptoms):
        """
        Diagnose which illness fit to your symptoms
        :param symptoms:
        :return:
        """
        if (self.root.get_neg() == None and
                self.root.get_pos() == None):
            return self.root.get_data()
        if self.root.get_data() in symptoms:
            return Diagnoser(self.root.get_pos()).diagnose(symptoms)
        return Diagnoser(self.root.get_neg()).diagnose(symptoms)

    def calculate_success_rate(self, records):
        """
        Calculate success rate of the tree
        :param records:
        :return:
        """
        success = 0
        fail = 0
        for record in records:
            if self.diagnose(record.get_symp()) == record.get_illness():
                success += 1
            else:
                fail += 1
        return success / (success + fail)

    def all_illnesses(self):
        """
        :returns a list of all illnesses at the three
        """
        return self.illnesses_arrange_lst(self.all_illnesses_core([]))

    def all_illnesses_core(self, lst):
        """
        Running recursivly, if getting into a leaf,
        adding his data to the list
        :param lst:
        :return:
        """
        if (self.root.get_neg() == None and
                self.root.get_pos() == None):
            lst.append(self.root.get_data())
            return
        Diagnoser(self.root.get_pos()).all_illnesses_core(lst)
        Diagnoser(self.root.get_neg()).all_illnesses_core(lst)
        return lst

    def illnesses_arrange_lst(self, illnesses_lst):
        """
        Arranging the illness list by frequncy,
        doing it by converting to dict and check
        value of each illness,
        return the max value illness
        :param illnesses_lst:
        :return:
        """
        illness_dict = {}  # Creating a dict to have order with the values
        for ilness in illnesses_lst:
            if ilness not in illness_dict:
                illness_dict.update({ilness: illnesses_lst.count(ilness)})
        illnesses_lst = [(k, v) for k, v in illness_dict.items()]
        #turning it back to a list
        illnesses_lst = (sorted(illnesses_lst, key=lambda x: (x[1])))[::-1]
        # sorting by frq
        illnesses_lst = [i[0] for i in illnesses_lst]
        return illnesses_lst

    def most_rare_illness(self, records):
        """
        Checking for the most rare illness in the tree
        if we follow after the symptoms on the records,
        doing it by using dict, adding value to each
        illness we got during the diagnos,
        returning the min value illness
        :param records:
        :return:
        """
        illness_dict = {}
        illnesses = self.all_illnesses()
        for illness in illnesses:
            illness_dict.update({illness: 0})
        for record in records:
            illness_dict[self.diagnose(record.get_symp())] += 1
        illnesses_lst = [(k, v) for k, v in illness_dict.items()]
        return min(illnesses_lst, key=lambda x: x[1])[0]

    def paths_to_illness(self, illness):
        """
        returns all the paths to the illness
        :param illness:
        :return:
        """
        if (self.root.get_pos() is None and
                self.root.get_neg() is None):
            return []
        return self.paths_to_illness_core(illness, [],[])


    def paths_to_illness_core(self, illness, lst,final):
        """
        checking all paths recursivly, if path is valid
        adds it to final list,
        after it finishs with all possible paths,
        returns the final list
        :param illness:
        :param lst:
        :param final:
        :return:
        """
        if (self.root.get_pos() == None and
                self.root.get_neg() == None):
            if illness == self.root.get_data():
                final.append(lst)
                return
            else:
                while lst and lst[len(lst)-1]==False:
                    lst.pop()
                return
        Diagnoser(self.root.get_pos()).paths_to_illness_core(illness,
                                                        lst + [True],final)
        Diagnoser(self.root.get_neg()).paths_to_illness_core(illness,
                                                       lst + [False],final)
        return final


def build_tree(records, symptoms):
    """
    Builds a tree using the symptoms list inserted,
    while getting to leafs, will try to match illness
    at records to symptoms got.
    :param records:
    :param symptoms:
    :return:
    """
    root = Node(None, None, None)
    tree_building(root, symptoms, [], records)
    return root


def tree_building(root, symptoms, lst, record):
    """
    Building the actual tree, after getting to a leaf
    using the func illness_adding to find the best
    candidate to be the illness
    :param root:
    :param symptoms:
    :param lst:
    :param record:
    :return:
    """
    if len(symptoms) == len(lst):
        root.data = illnesses_adding(symptoms, lst, record)
        return
    root.set_data(symptoms[len(lst)])
    root.set_neg(Node(None, None, None))
    root.set_pos(Node(None, None, None))
    lst.append(False)
    tree_building(root.get_neg(), symptoms, lst, record)
    while lst[len(lst) - 1] == True:
        lst.pop()
    if len(lst) > 0:
        lst.pop()
    lst.append(True)
    tree_building(root.get_pos(), symptoms, lst, record)


def illnesses_adding(symptoms, lst, records):
    """
    filtering records,
    doing so by no_symp criteria and yes_symp, after
    the filtering, using dict to count most appered illness
    the winner gets to be on the leaf
    :param symptoms:
    :param lst:
    :param records:
    :return:
    """
    yes_symptoms_lst = []
    no_symptoms_lst = []
    illness_dict = {}
    for i in range(len(lst)):
        if lst[i]:
            yes_symptoms_lst.append(symptoms[i])
        else:
            no_symptoms_lst.append(symptoms[i])
    records_updated1 = update_records(records[:], no_symptoms_lst)
    records_updated2 = update_records2(records_updated1, yes_symptoms_lst)
    for record in records_updated2:
        if record.get_illness() not in illness_dict:
            illness_dict.update({record.get_illness(): 1})
        else:
            illness_dict[record.get_illness()] += 1
    if len(illness_dict) == 0:
        return "N/A"
    return max(illness_dict, key=illness_dict.get)


def update_records(records, no_symptoms_lst):
    """
    first filtering,
    using no_symp, removing records who got
    those symps.
    :param records:
    :param no_symptoms_lst:
    :return:
    """
    records_return = []
    for record in records:
        for k in range(len(no_symptoms_lst)):
            if no_symptoms_lst[k] in record.get_symp():
                break
            if k == len(no_symptoms_lst) - 1:
                records_return.append(record)
    if records_return:
        return records_return
    return records


def update_records2(records, yes_symptoms_lst):
    """
    Second filtering, using yes_symp lst,
    if record got those symps, hes added
    to most_relevant list.
    if no one got to most relevant,
    returning records.
    :param records:
    :param yes_symptoms_lst:
    :return:
    """
    most_relevant = []
    max = 0
    for record in records:
        for j in range(len(yes_symptoms_lst)):
            if yes_symptoms_lst[j] in record.get_symp():
                max += 1
            if max == len(yes_symptoms_lst):
                most_relevant.append(record)
        max = 0
    if most_relevant:
        return most_relevant
    return records


def optimal_tree(records, symptoms, depth):
    """
    Trying to build a perfect tree. with
    highest succsess rate.
    making a dict with tree we build, and their
    success rate,
    return the max success rate tree
    :param records:
    :param symptoms:
    :param depth:
    :return:
    """
    dict_of_trees = {}
    for sub_smp in list(itertools.combinations(symptoms, depth)):
        root = build_tree(records, sub_smp)
        diagnoser = Diagnoser(root)
        dict_of_trees[root] = diagnoser.calculate_success_rate(records)
    return max(dict_of_trees, key=dict_of_trees.get)

