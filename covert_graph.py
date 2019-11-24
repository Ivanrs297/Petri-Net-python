from PN import PN
from Node import Node
from Edge import Edge
import numpy as np

class covert_graph:
    frontier_stack = list()
    expanded_list = list()
    petri_net = None
    is_alive = True
    is_bounded = True
    is_reversible = True
    is_blocked_free = True

    def __init__(self, file_name):
        self.petri_net = PN(file_name)


    def create_graph(self):
        initial_node = Node(self.petri_net.M0)
        self.frontier_stack.append(initial_node)

        while len(self.frontier_stack) > 0:
            current_node = self.frontier_stack.pop()
            self.expanded_list.append(current_node)
            tail_edges = self.expand_node(current_node)

            if len(tail_edges) > 0:
                for tail in tail_edges: # Current_node's possible tails
                    current_edge = self.compare_edge(tail)

                    is_duplicated = False
                    for node in self.expanded_list:
                        if np.array_equal(node.marked,current_edge.head.marked):
                            current_edge.head = node
                            current_edge.tail = current_node
                            # Add child to parent
                            current_node.add_tail(current_edge)
                            # Create new parent edge for node
                            node.add_head(current_edge)
                            is_duplicated = True
                            break

                    if not is_duplicated:
                        current_edge.tail = current_node
                        current_node.add_tail(current_edge)
                        self.frontier_stack.append(current_edge.head)
                else:
                    self.is_blocked_free = False



    def compare_edge(self,edge):
        for node in self.expanded_list:
            for i,value in enumerate(node.marked):
                current_head_value = edge.head.marked[i,0]
                if value >= current_head_value:
                    if value > current_head_value:
                        node.marked[i,0] = 'w'
                        edge.head.marked[i,0] = 'w'
                else:
                    break
        return edge




    def expand_node(self,node):
        edges=list()
        edges.append(Edge())
        return edges




