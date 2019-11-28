import queue
import math
import numpy as np


class Node:
    marker = None
    transitions = list()
    childs = list()
    parent = None

    def __init__(self, marker, pre, A):
        self.childs = list()
        self.transitions = [0] * pre.shape[1]
        self.marker = np.mat(marker)
        self.set_transitions(pre)

    # Set the available transitions of the marker
    def set_transitions(self, pre):
        for j in range(pre.shape[1]):
            result = self.marker.transpose() - pre[:, j]
            if np.all((result >= 0)):
                self.transitions[j] = 1

    def trigger_transition(self, transition, marker, A):
        m_prev = np.transpose(marker)
        mult = A * transition.transpose()
        mk = np.add(m_prev, mult)
        return mk

    def update_marker_w(self, child_marker):
        for i, x in enumerate(self.marker.transpose()):
            if x == 999:
                child_marker[i, 0] = 999
        return child_marker

    def check_for_w_in_parents(self, marker):
        pendent = queue.Queue()
        pendent.put(self)
        while not pendent.empty():
            aux = pendent.get()
            result = marker - aux.marker.transpose()

            for i, x in enumerate(aux.marker.transpose()):
                if x >= 999:
                    result[i] = 999

            if np.all((result >= 0)):
                for i, x in enumerate(result):
                    if x >= 1:
                        marker[i] = 999

            if aux.parent:
                pendent.put(aux.parent)
        return marker

    def expand_node(self, pre, A):
        for index, transition in enumerate(self.transitions):
            if transition == 1:
                transitions_vector = [0] * len(self.transitions)
                transitions_vector[index] = 1
                transitions_vector = np.mat(transitions_vector)
                child_marker = self.trigger_transition(transitions_vector, self.marker, A)
                # child_marker = self.update_marker_w(child_marker)
                self.check_for_w_in_parents(child_marker)
                child = Node(child_marker.transpose(), pre, A)
                child.parent = (self)
                self.childs.append(child)
