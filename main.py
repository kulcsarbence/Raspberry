from pirc522 import RFID
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

sleepInterval = 10
GPIO.setwarnings(False)
rdr = RFID()

uidPath = "acceptedUID.txt"
line_count = sum(1 for line in open(uidPath))
acceptedUID = [[0 for x in range(5)] for y in range(line_count)]

#Az ultrahang szenzor fuggvenyei kovetkeznek:

trigPin = 35
echoPin = 37
max_dist = 220
timeOut = max_dist*60

GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

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
    try:
        while True:
            print("Elindult a while true")
            uidd = getUID()
            if checkUIDmatch(uidd):
                print("Belepes engedelyezve!")
                while(not isThereACar()):
                    print("Varakozunk")
                print("Auto megerkezett")
                time.sleep(sleepInterval)
                print("Lecsukjuk a kaput")
            else:
                print("elszartuk")
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__=="__main__":
    main()
