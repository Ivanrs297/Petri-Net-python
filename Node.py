
class Node:
    marked = None
    head_edges = []     # Parents
    tail_edges = []     # Child

    def __init__(self, marked):
        self.marked=marked

    def add_tail(self,tail):
        self.tail_edges.append(tail)

    def add_head(self,head):
        self.head_edges.append(head)

