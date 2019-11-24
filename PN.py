import numpy as np

class PN:
    pre = None  # The pre Matrix
    post = None  # The post Matrix
    M = list()  # The list of marks, m[0] = initial mark
    A = None
    M0 = None

    # LD.n: Add new constructor to use this class from covert_graph
    # this new parameter is the file name in which is saved the petri net's
    # initial configuration
    def __init__(self, file_name):
        self.set_from_file(file_name)

    def set_from_file(self,file_name):
        # f = open("data.txt", "r")
        f = open(file_name, "r")
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


# PN = PN()
# PN.set_from_file()
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
