import socket
import hashlib
import uuid
import datetime
import os

port = "9090"

while True:
    print("1. Start node")
    print("2. Generate first block")
    print("3. Config miner")
    print("4. Exit")
    option = input()
    if (option == "1"):
        while True:
            server_config_file = open("server_config", "r")
            port = server_config_file.read()
            server_config_file.close()
            sock = socket.socket()
            sock.bind(('', int(port)))
            sock.listen(1)
            conn, conn_addr = sock.accept()
            print ('connected:' , conn_addr)
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                if (data[0] == 's' and data[1] == 'y' and data[2] == 'n' and data[3] == 'c' and data[4] == " "):
                    addr = ""
                    count = 0
                    addres_recipient = ""
                    addres_sender = ""
                    cost = ""
                    addres_cost = 0
                    hash_block = ""
                    print("Sync to: ", conn_addr)
                    for i in range(5, 69):
                        addr = addr + data[i]
                    print("Addres of wallet: ", addr)
                    counter_file = open("blockchain/counter", "r")
                    count = int(counter_file.read())
                    counter_file.close()
                    for i in range(count):
                        transaction_file = open("blockchain/"+str(i+1), "r")
                        transaction = str(transaction_file.read())
                        transaction_file.close()
                        for j in range(0, 64):
                            hash_block = hash_block + transaction[j]
                        for j in range(64,128):
                            addres_sender = addres_sender + transaction[j]
                        for j in range(128,192):
                            addres_recipient = addres_recipient + transaction[j]
                        for j in range(192,len(transaction)):
                            cost = cost + transaction[j]
                        previos_transaction_file = open("blockchain/"+str(i), "r")
                        previous_block = previos_transaction_file.read()
                        previos_transaction_file.close()
                        if (hash_block != str(hashlib.sha256(previous_block.encode()).hexdigest())):
                            print("Wrong block!!!  " + str(i))
                            conn.close()
                            exit()
                        if (addres_recipient == addr):
                            addres_cost = addres_cost + int(cost)
                        if (addres_sender == addr):
                            addres_cost = addres_cost - int(cost)
                        addres_recipient = ""
                        addres_sender = ""
                        cost = ""
                        hash_block = ""
                    config_miner_file = open("miner_config", "r")
                    miner_addres = ""
                    for i in range(0, 64):
                        miner_addres = miner_addres + config_miner_file.read(i)
                    config_miner_file.close()
                    previos_transaction_file = open("blockchain/"+str(count), "r")
                    previous_block = previos_transaction_file.read()
                    previos_transaction_file.close()
                    transaction_file = open("blockchain/" + str(count + 1), "w")
                    transaction_file.write(str(hashlib.sha256(str(previous_block).encode()).hexdigest()) + "0000000000000000000000000000000000000000000000000000000000000000" + miner_addres + str(count))
                    transaction_file.close()
                    counter_file = open("blockchain/counter", "w")
                    counter_file.write(str(count+1))
                    counter_file.close()
                    conn.send(str(addres_cost).encode())
                    count = 0
                if (data[0] == 's' and data[1] == 'e' and data[2] == 'n' and data[3] == 'd' and data[4] == " "):
                    addr_sender = ""
                    addr_recipient = ""
                    cost_send = ""
                    count = 0
                    for i in range(5, 69):
                        addr_sender = addr_sender + data[i]
                    for i in range(69, 133):
                        addr_recipient = addr_recipient + data[i]
                    for i in range(133, len(data)):
                        cost_send = cost_send + data[i]
                    counter_file = open("blockchain/counter", "r")
                    count = int(counter_file.read())
                    counter_file.close()
                    counter_file = open("blockchain/counter", "w")
                    counter_file.write(str(count+1))
                    counter_file.close()
                    count = count + 1
                    previos_transaction_file = open("blockchain/"+str(count-1), "r")
                    previous_block = previos_transaction_file.read()
                    previos_transaction_file.close()
                    transaction_file = open("blockchain/" + str(count), "w")
                    transaction_file.write(str(hashlib.sha256(previous_block.encode()).hexdigest()) + addr_sender+addr_recipient+cost_send)
                    transaction_file.close()
                    print(addr_sender + " send " + cost_send + " coins to " + addr_recipient)
                    addr_sender = ""
                    addr_recipient = ""
                    cost_send = ""
                    count = 0
            conn.close()
    if (option == "2"):
        os.mkdir("blockchain/")
        config_miner_file = open("miner_config", "r")
        miner_addres = ""
        for i in range(0, 64):
            miner_addres = miner_addres + config_miner_file.read(i)
        config_miner_file.close()
        counter_file = open("blockchain/counter", "w")
        counter_file.write("1")
        counter_file.close()
        transaction_file = open("blockchain/0", "w")
        transaction_file.write("First block in blockchain")
        transaction_file.close()
        transaction_file = open("blockchain/0", "r")
        first_block = transaction_file.read()
        transaction_file.close()
        transaction_file = open("blockchain/1", "w")
        transaction_file.write(str(hashlib.sha256(str(first_block).encode()).hexdigest()) + "0000000000000000000000000000000000000000000000000000000000000000" + miner_addres + "100")
        transaction_file.close()
    if (option == "3"):
        addres_miner = input("input addres for miner: ")
        config_miner_file = open("miner_config", "w")
        config_miner_file.write(addres_miner)
        config_miner_file.close()
        addres_miner = ""
        server_config_file = open("server_config", "w")
        port = input("Input server port: ")
        server_config_file.write(str(port))
        server_config_file.close()
    if (option == "4"):
        break