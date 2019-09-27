from pirc522 import RFID
import RPi.GPIO as GPIO
rdr = RFID()

path = "acceptedUID.txt"
GPIO.setwarnings(False)

line_count = sum(1 for line in open(path))
acceptedUID = [[0 for x in range(5)] for y in range(line_count)]

def getAcceptedUID():
    file2 = open(path, "r")
    for i in range(0, line_count, 1):
        string = file2.readline()
        acceptedUID[i] = [x.strip() for x in string.split(',')]
        for j in range(0,5,1):
            acceptedUID[i][j] = int(acceptedUID[i][j])
    return acceptedUID

def checkUIDmatch(current_uid):
    accepted = getAcceptedUID()
    tmp = True
    toReturn = False
    for i in range(0, line_count, 1):
        tmp = True
        for j in range(0, 5, 1):
            if current_uid[j]!=accepted[i][j]:
                tmp = False
        if tmp:
            toReturn = True
    return toReturn


def getUID():
    toReturn = [0 for x in range(5)]
    while True:
        rdr.wait_for_tag()
        (error, tag_type) = rdr.request()
        if not error:
            (error, uid) = rdr.anticoll()
            if not error:
                return uid;
    rdr.cleanup()
    return toReturn

def main():
    c = getUID()
    if checkUIDmatch(c):
        print("A kartyat toroljuk a rendszerbol.")
        with open(path, "r") as f:
            lines = f.readlines()
        with open(path, "w") as f:
            for line in lines:
                if line.strip("\n") != str(c[0])+","+str(c[1])+","+str(c[2])+","+str(c[3])+","+str(c[4]):
                    f.write(line)
    else:
        print("A kartya nincs a rendszerben.")

if __name__=="__main__":
    main()
