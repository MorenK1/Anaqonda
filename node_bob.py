from cqc.pythonLib import CQCConnection, qubit
import random
import json

N_QUBIT = 10

with CQCConnection("Bob") as Bob:
    # Preparing my qubits
    h_vector = [random.choice([0, 1]) for _ in range (N_QUBIT)]
    x_vector = [random.choice([0, 1]) for _ in range (N_QUBIT)]
    q_vector = []
    
    for _ in range(N_QUBIT):
        q_vector.append(qubit(Bob))
    
    for i in range(N_QUBIT):
        if x_vector[i] == 1:
            q_vector[i].X()
        if h_vector[i] == 1:
            q_vector[i].H()
    
    # Ask to Charlie (the commutor node as chosen for the network architecture)
    # if I am the master, stating who I am
    print("# Am I the master, stating who I am ?_?")
    Bob.sendClassical("Charlie", json.dumps( {"name": "Bob"} ).encode("utf-8"))
    charlie_attempt_response = Bob.recvClassical()
    im_master = json.loads(charlie_attempt_response.decode("utf-8"))
    
    # If Charlie responded than it's ready for receiving my qubits, I send them
    print("# I'm sending the qubits to Charlie T_T")
    for qubit in q_vector:
        Bob.sendQubit(qubit, "Charlie")
    
    # Receive the resulting matrix from Charlie
    matrix = json.loads(Bob.recvClassical().decode("utf-8"))
    
    hother_vector = [] #TODO: read vector
    #TODO: send vector

    if im_master:
        # Flips the necessary bits based on matrix correlation
        for i in range(N_QUBIT):
            if matrix[i][0] == 0:
                x_vector[i] = ''
                continue
            if (matrix[i][0] == 1) and (h_vector[i] == 1):
                continue
            x_vector[i] = 1 if x_vector[i] == 0 else 0
    else:
        pass  # nothing to do
    
    # Print the key obtained
    print(x_vector)

