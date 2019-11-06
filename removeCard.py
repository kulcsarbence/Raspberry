from pirc522 import RFID
import RPi.GPIO as GPIO
import mysql.connector

rdr = RFID()

GPIO.setwarnings(False)
#acceptedUID[i] = [x.strip() for x in string.split('-')]
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
    mydb = mysql.connector.connect(host="localhost", user="bence", passwd="benc1e", database="db")
    cursor = mydb.cursor()
    c = getUID()
    sql = "DELETE FROM parking WHERE cardnumber = %s"
    val = (str(c[0])+","+str(c[1])+","+str(c[2])+","+str(c[3])+","+str(c[4]))
    print(val)
    cursor.execute(sql,(val,))
    mydb.commit()
    cursor.close()
    mydb.close()


if __name__=="__main__":
    main()
