from pirc522 import RFID
import RPi.GPIO as GPIO
import time
import tweepy
import mysql.connector
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

GPIO.setmode(GPIO.BOARD)

sleepInterval = 5
GPIO.setwarnings(False)
rdr = RFID()

#Az ultrahang szenzor fuggvenyei kovetkeznek:

trigPin = 35
echoPin = 37
gLedPin = 38
rLedPin = 40    # red led pin
gatePin = 39    # gate trigger pin
max_dist = 220
timeOut = max_dist*60

#inicializaljuk a max szabad helyeket, az ures helyeket
global emptySpaces
global totalSpaces
global api
totalSpaces = 100
emptySpaces = totalSpaces

GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(gLedPin, GPIO.OUT)
GPIO.setup(rLedPin, GPIO.OUT)

#a fuggveny visszaadja, hogy a kikuldott hang mennyi ido mulva erkezik vissza
def pulseTime(pin, level, timeOut):
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.00001):
            return 0
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

#Az RFID chipnel levo kartya UIDjenek meghatarozasa
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

def initTwitter():
    # Secret fajlbol kiolvassuk az autentikaciohoz szukseges adatokat
    with open("secret.txt", "r") as fd:
            lines = fd.read().splitlines()
    auth = tweepy.OAuthHandler(lines[0], lines[1])
    auth.set_access_token(lines[2], lines[3])
    # API objektum letrehozasa
    global api
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    return

def tweetString(string):
    global api
    api.update_status(string) # Twitterre kikuldjuk a tweetet
    return

def blinkLed(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)  # a kapott pinen helyezkedo ledet haromszot egymas utan felvilantjuk
    time.sleep(0.25)                       # varunk 1/4 mpt
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(led_pin, GPIO.LOW)
    return


def main():
    global emptySpaces
    PCF8574_address = 0x27 # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F # I2C address of the PCF8574A chip.
    # Create PCF adapter
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print ('I2C Address Error !')
            exit(1)
                     # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
    mcp.output(3,1) # LCD hattervilagitas
    lcd.begin(16,2) # Sorok oszlopok beallitasa
    lcd.setCursor(0,0)
    lcd.message('Szabad helyek:\n')
    lcd.message(str(emptySpaces))
    mydb = mysql.connector.connect(host="localhost",user="bence",passwd="benc1e",database="db")
    mydb2 = mysql.connector.connect(host="localhost",user="bence",passwd="benc1e",database="db2")
    cursor1 = mydb.cursor()
    cursor2 = mydb2.cursor()
    sql_addcard_db = "INSERT INTO parking (cardnumber) VALUES (%s)"
    sql_addcard_db2 = "INSERT INTO parked (cardnumber) VALUES (%s)"
    sql_deletecard_db2 = "DELETE FROM parked WHERE cardnumber = %s"
    sql_select_db = "SELECT cardnumber FROM parking WHERE cardnumber = %s"
    sql_select_db2 = "SELECT cardnumber FROM parked WHERE cardnumber = %s"
    cursor2.execute("DELETE FROM parked")
    mydb2.commit()
    global totalSpaces
    counter = 0
    initTwitter()       #twitter inicializacio 
    try:
        while True:
            lcd.clear()
            lcd.setCursor(0,0)
            lcd.message('Szabad helyek:\n')
            time.sleep(1)
            lcd.message(str(emptySpaces))
            counter = counter+1
            if (counter>10):
                counter=0
                tweetString("Jelenleg a szabad helyek szama: "+str(emptySpaces))
            print("Elindult a while true")
            print(str(emptySpaces))
            uidd = getUID()
            val = ( str(uidd[0]) + "," + str(uidd[1]) + "," + str(uidd[2]) + "," + str(uidd[3]) + "," + str(uidd[4]) )
            cursor2.execute(sql_select_db2, (val,) )
            if cursor2.fetchone():
                blinkLed(gLedPin)
                print("Viszontlatasra")
                if(emptySpaces != totalSpaces):             #biztositjuk hogy a szabad helyek erteke a vart hatarakon belul maradjon
                    emptySpaces += 1
                cursor2.execute(sql_deletecard_db2, (val,))
                mydb2.commit()
                time.sleep(sleepInterval)
            else:
                cursor1.execute(sql_select_db, (val,))
                if (cursor1.fetchone() is not None) & (emptySpaces > 0): #ha az uid az adatbazisban van ES van meg ures hely
                    print("Belepes engedelyezve!")
                    if(emptySpaces != 0):                   #biztositjuk hogy a szabad helyek erteke a vart hatarakon belul maradjon
                        emptySpaces -= 1
                    GPIO.output(gLedPin, GPIO.HIGH)
                    #GPIO.output(gatePin, GPIO.HIGH) #aktivaljuk a gate pin-t
                    cursor2.execute(sql_addcard_db2, (val,))
                    mydb2.commit()
                    while(not isThereACar()):
                        print("")
                    print("Auto megerkezett")
                    time.sleep(sleepInterval)
                    GPIO.output(gLedPin, GPIO.LOW)
                    print("Lecsukjuk a kaput")
                    #GPIO.output(gatePin, GPIO.LOW)
                else:
                    if emptySpaces==0:
                        print("Nincs szabad hely!")
                        blinkLed(rLedPin)
                    else:
                        print("Nem szerepel ez a kartya az adatbazisban!")
                        blinkLed(rLedPin)
                    time.sleep(1)
    except KeyboardInterrupt: #biztonsagi megfontolasbol mindent leallitunk
        GPIO.output(gLedPin, GPIO.LOW)
        GPIO.output(rLedPin, GPIO.LOW)
        GPIO.cleanup()
        cursor2.execute("DELETE FROM parked")
        mydb2.commit()
        cursor1.close()
        cursor2.close()
        mydb.close()
        mydb2.close()
        lcd.clear()

if __name__=="__main__":
    main()
