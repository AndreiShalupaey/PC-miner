import hashlib

def generate_block(index, addres_sender, addres_recipient, cost):
    previous_block_data = ""
    previous_block_hash = ""
    proof = 0
    previous_block_data = read_block(index - 1, "all")
    previous_block_hash = str(hashlib.sha256(previous_block_data.encode()).hexdigest())
    while True:
        block_hash = str(hashlib.sha256(str(previous_block_hash + addres_sender + addres_recipient + str(cost) + ":" + str(proof)).encode()).hexdigest())
        if (block_hash[60] == '0' and block_hash[61] == '0' and block_hash[62] == '0' and block_hash[63] == '0'):
            break
        proof = proof + 1
    block_file = open("blockchain/" + str(index), "w")
    block_file.write(previous_block_hash + addres_sender + addres_recipient + str(cost) + ":" + str(proof))
    block_file.close()

def read_block(index, mode):
    block_data = ""
    previous_block_hash = ""
    addres_sender = ""
    addres_recipient = ""
    cost = ""
    block_file = open("blockchain/" + str(index), "r")
    block_data = block_file.read()
    block_file.close()
    if (mode == "all"):
        return block_data
    block_data, proof = block_data.split(":")
    if (mode == "hash"):
        for j in range(0, 64):
            previous_block_hash = previous_block_hash + block_data[j]
        return previous_block_hash
    if (mode == "sender"):
        for j in range(64,128):
            addres_sender = addres_sender + block_data[j]
        return addres_sender
    if (mode == "recipient"):
        for j in range(128,192):
            addres_recipient = addres_recipient + block_data[j]
        return addres_recipient
    if (mode == "cost"):
        for j in range(192,len(block_data)):
            cost = cost + block_data[j]
        return cost
    if (mode == "proof"):
        return str(proof)

def genesis_block():
    proof = 0
    while True:
        block_hash = str(hashlib.sha256(str("First block in blockchain:" + str(proof)).encode()).hexdigest())
        if (block_hash[60] == '0' and block_hash[61] == '0' and block_hash[62] == '0' and block_hash[63] == '0'):
            break
        proof = proof + 1
    block_file = open("blockchain/0", "w")
    block_file.write("First block in blockchain:" + str(proof))
    block_file.close()