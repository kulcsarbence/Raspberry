from pirc522 import RFID
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

sleepInterval = 10
GPIO.setwarnings(False)
rdr = RFID()

uidPath = "acceptedUID.txt"
parkedPath = "parkedUID.txt"
line_count = sum(1 for line in open(uidPath))
global p_line_count
acceptedUID = [[0 for x in range(5)] for y in range(line_count)]
global p_acceptedUID
p_line_count = sum(1 for line in open(parkedPath))
p_acceptedUID = [[0 for x in range(5)] for y in range(p_line_count)]
#Az ultrahang szenzor fuggvenyei kovetkeznek:

trigPin = 35
echoPin = 37
gLedPin = 38
max_dist = 220
timeOut = max_dist*60

GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(gLedPin, GPIO.OUT)

def pulseTime(pin, level, timeOut):
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.00001):
            return 0;
    pulse = (time.time() - t0)
    return pulse

def isThereACar():
    isThere = False
    GPIO.output(trigPin, GPIO.HIGH)
    time.sleep(0.00001) #10 mikroszekundum
    GPIO.output(trigPin, GPIO.LOW) #eloallt a 10 mikroseces jel
    pingTime = 0
    while(pingTime==0):
        pingTime = pulseTime(echoPin,GPIO.HIGH,timeOut)
    distance = pingTime * 340.0 / 2.0 * 100.0  #CMben kapjuk meg
    print(distance)
    if distance<20.0:
        isThere = True
    return isThere


#Vege az ultrahang szenzor fuggvenyeinek

def p_getAcceptedUID():
    p_acceptedUID = [[0 for x in range(5)] for y in range(p_line_count)]
    file2 = open(parkedPath, "r")
    for i in range(0, p_line_count, 1):
        string = file2.readline()
        p_acceptedUID[i] = [x.strip() for x in string.split(',')]
        for j in range(0,5,1):
            print(p_acceptedUID[i][j])
            p_acceptedUID[i][j] = int(p_acceptedUID[i][j])
    file2.close()
    return p_acceptedUID

def p_checkUIDmatch(current_uid):
    accepted = p_getAcceptedUID()
    tmp = True
    toReturn = False
    for i in range(0, p_line_count, 1):
        tmp = True
        for j in range(0, 5, 1):
            if current_uid[j]!=accepted[i][j]:
                tmp = False
        if tmp:
            toReturn = True
    return toReturn


def getAcceptedUID():
    file = open(uidPath, "r")
    for i in range(0, line_count, 1):
        string = file.readline()
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
                return uid
    rdr.cleanup()
    return toReturn


def main():
    global p_line_count
    try:
        while True:
            print(p_line_count)
            print("Elindult a while true")
            uidd = getUID()
            if p_checkUIDmatch(uidd):
                c = uidd
                print("Viszontlatasra")
                with open(parkedPath, "r") as f:
                    lines = f.readlines()
                with open(parkedPath, "w") as f:
                    for line in lines:
                        if line.strip("\n") != str(c[0])+","+str(c[1])+","+str(c[2])+","+str(c[3])+","+str(c[4]):
                            f.write(line)
                p_line_count = sum(1 for line in open(parkedPath, "r"))
                time.sleep(sleepInterval)
            else:
                if checkUIDmatch(uidd):
                    c = uidd
                    print("Belepes engedelyezve!")
                    GPIO.output(gLedPin, GPIO.HIGH)
                    File3 = open(parkedPath, "a+")
                    print(c[0])
                    File3.write(str(c[0])+","+str(c[1])+","+str(c[2])+","+str(c[3])+","+str(c[4])+"\n")
                    File3.close()
                    File4 = open(parkedPath, "r")
                    print(File4.readlines())
                    File4.close()
                    p_line_count = sum(1 for line in open(parkedPath, "r"))
                    print(p_line_count)
                    while(not isThereACar()):
                        print("")
                    print("Auto megerkezett")
                    time.sleep(sleepInterval)
                    GPIO.output(gLedPin, GPIO.LOW)
                    print("Lecsukjuk a kaput")
                else:
                    print("A kartya nincs a rendszerben.")
    except KeyboardInterrupt:
        with open(parkedPath, "w") as f:
            f.write("")
        GPIO.output(gLedPin, GPIO.LOW)
        GPIO.cleanup()

if __name__=="__main__":
    main()
