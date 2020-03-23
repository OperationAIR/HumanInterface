from time import sleep



def sendCommand(sendtype, sendvalue):

    if sendtype == "PEEP":
        print(sendvalue)
    elif sendtype == "Freq":
        print(sendvalue)
    elif sendtype == "Tida":
        print(sendvalue)
    elif sendtype == "Pres":
        print(sendvalue)   
    else:
        print("fout")


