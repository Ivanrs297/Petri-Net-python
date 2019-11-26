import numpy as np
from Node import Node
import queue
from graphviz import Digraph
from tarjan import tarjan


class PN:
    pre = None  # The pre Matrix
    post = None  # The post Matrix
    M = list()  # The list of marks, m[0] = initial mark
    A = None

    # Properties
    bounded = True
    liveness = True
    cyclic = True
    triggered_t = list()
    aux_tarjan = {}

    def set_from_file(self):
        f = open("data.txt", "r")
        data = f.readlines()
        self.M.append(np.mat(data[0]))
        self.pre = np.mat(data[1])
        self.post = np.mat(data[2])
        self.A = self.post - self.pre
        f.close()

    def get_available_transitions(self):
        t = list()
        for j in range(self.pre.shape[1]):
            # Mark - column j from P
            result = self.M[len(self.M) - 1].transpose() - self.pre[:, j]

            # If Mark is greater o equal than the column then:
            if np.all((result == 0) | (result == 1)):
                t.append(1)
            else:
                t.append(0)
        print("Available Ts: ", t)
        return t

    def select_transition(self, transitions):
        print("Las siguientes transiciones han sido habilitadas:")
        for i, t in enumerate(transitions):
            if t > 0:
                temp = str(i + 1) + ": T" + str(i + 1)
                print(temp)

        print("¿Qué transición quieres disparar?")
        transition = int(input())
        transition = transition - 1
        if transition >= 0:
            vector = transitions.copy()
            for i in range(len(vector)):
                if i != transition:
                    vector[i] = 0
            return np.transpose(np.matrix(vector))
        else:
            return None

    def trigger_transition(self, transition):
        m_prev = np.transpose(self.M[len(self.M) - 1])
        mult = self.A * transition
        mk = np.add(m_prev, mult)
        self.M.append(np.transpose(mk))
        print("Marcado:", np.transpose(mk))


PN = PN()
PN.set_from_file()

Node = Node(PN.M[0], PN.pre, PN.A)


def is_node_in_pendent(node, queue):
    while not queue.empty():
        aux = queue.get()
        aux = str(aux.marker.A1)
        node_marker = str(node.marker.A1)
        if node_marker == aux:
            return True
    return False


def is_node_in_visited(node, visited):
    for i in range(len(visited)):
        node_marker = str(node.marker.A1)
        visited_marker = str(visited[i].marker.A1)

        if node_marker == visited_marker:
            return True
    return False


def get_transition_from_vector(counter, vector):
    for t, x in enumerate(vector):
        if x == 1:
            if counter == 0:
                if t not in PN.triggered_t:
                    PN.triggered_t.append(t)
                return t + 1
            else:
                counter -= 1


def node_is_greater_to_visited(node, visited):
    for elem in visited:
        result = node.marker.transpose() - elem.marker.transpose()
        if np.all((result >= 0)):
            for i, x in enumerate(result):
                if x == 1:
                    node.marker[0, i] = 999
    return node.marker


def replace_w(marker):
    marker = marker.replace('999', 'w')
    if 'w' in marker:
        PN.bounded = False
    return marker


dot = Digraph(comment='Reach Graph', strict=True)
dot.attr(size='8,5')

visited = list()
pendent = queue.Queue()
pendent.put(Node)
while not pendent.empty():
    aux = pendent.get()

    aux.marker = node_is_greater_to_visited(aux, visited)
    aux.expand_node(PN.pre, PN.A)
    visited.append(aux)
    if len(aux.childs) == 0:
        PN.liveness = False

    dot.node(replace_w(str(aux.marker.A1)), replace_w(str(aux.marker.A1)))

    child_marker = list()

    for i, child in enumerate(aux.childs):
        if not is_node_in_visited(child, visited):
            pendent.put(child)
        child.marker = node_is_greater_to_visited(child, visited)
        dot.node(replace_w(str(child.marker.A1)), replace_w(str(child.marker.A1)))
        dot.edge(replace_w(str(aux.marker.A1)), replace_w(str(child.marker.A1)),
                 label='T' + str(get_transition_from_vector(i, aux.transitions)))

        child_marker.append(replace_w(str(child.marker.A1)))

    PN.aux_tarjan[replace_w(str(aux.marker.A1))] = child_marker

dot.view()

# Properties
if PN.liveness and len(PN.triggered_t) == PN.pre.shape[1]:
    print("Viva: ", True)
else:
    print("Viva: ", False)

print("Acotada: ", PN.bounded)

tarjan = tarjan(PN.aux_tarjan)

if len(tarjan) == 1:
    print("Reversible/Cíclica: ", True)
else:
    print("Reversible/Cíclica: ", False)
#
# transitions = PN.get_available_transitions()
#
# while transitions is not None:
#     vector = PN.select_transition(transitions)
#     if vector is not None:
#         print(PN.trigger_transition(vector))
#         del transitions
#         del vector
#         transitions = PN.get_available_transitions()
#     else:
#         transitions = None
