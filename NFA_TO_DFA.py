import json
from collections import OrderedDict

def get_nfa_from_user():
    nfa = {}

    # Kullanıcıdan NFA'nın durum sayısını al
    nfa["states"] = int(input("Durum sayısını girin: "))

    # Kullanıcıdan NFA'nın alfabe harflerini al
    nfa["letters"] = input("Alfabe harflerini virgülle ayırarak girin: ").split(',')

    # Kullanıcıdan NFA'nın başlangıç durumunu al
    nfa["start"] = input("Başlangıç durumunu girin: ")

    # Kullanıcıdan NFA'nın geçiş fonksiyonlarını al
    nfa["t_func"] = []

    print("Geçiş fonksiyonlarını girin (format: durum,harf,durumlar). Bitirmek için 'q' girin.")

    while True:
        transition = input("Geçiş fonksiyonu: ")
        if transition.lower() == 'q':
            break
        from_state, symbol, to_states = transition.split(',')
        to_states = to_states.split()
        nfa["t_func"].append([from_state, symbol, to_states])

    # Kullanıcıdan NFA'nın son durumlarını al
    nfa["final"] = input("Son durumları virgülle ayırarak girin: ").split(',')
    return nfa

def nfa_to_dfa(data):
    dfa_states = 2 ** data["states"]
    dfa_letters = data["letters"]
    dfa_start = data["start"]
    dfa_t_func = []
    dfa_final = [] 
    q = []
    q.append((dfa_start,))
    nfa_transitions = {}
    dfa_transitions = {}

    for transition in data["t_func"]:
        nfa_transitions[(transition[0], transition[1])] = transition[2]

    for in_state in q:
        for symbol in dfa_letters:
            if len(in_state) == 1 and (in_state[0], symbol) in nfa_transitions:
                dfa_transitions[(in_state, symbol)] = nfa_transitions[(in_state[0], symbol)]
                if tuple(dfa_transitions[(in_state, symbol)]) not in q:
                    q.append(tuple(dfa_transitions[(in_state, symbol)]))
            else:
                dest = []
                f_dest = []
                for n_state in in_state:
                    if (n_state, symbol) in nfa_transitions and nfa_transitions[(n_state, symbol)] not in dest:
                        dest.append(nfa_transitions[(n_state, symbol)])
                if dest:
                    for d in dest:
                        for value in d:
                            if value not in f_dest:
                                f_dest.append(value)
                    dfa_transitions[(in_state, symbol)] = f_dest
                    if tuple(f_dest) not in q:
                        q.append(tuple(f_dest))

    for key, value in dfa_transitions.items():
        temp_list = [[(key[0]), key[1], value]]
        dfa_t_func.extend(temp_list)

    for q_state in q:
        for f_state in data["final"]:
            if f_state in q_state:
                dfa_final.append(q_state)

    dfa = OrderedDict()
    dfa["states"] = dfa_states 
    dfa["letters"] = dfa_letters
    dfa["t_func"] = dfa_t_func
    dfa["start"] = dfa_start
    dfa["final"] = dfa_final
    return dfa

nfa_data = get_nfa_from_user()
dfa_data = nfa_to_dfa(nfa_data)
with open('output.json', 'w') as output_file:
    json.dump(dfa_data, output_file, separators=(',', ':'))
print("DFA, output.json dosyasına yazıldı.")
