# Ez a repository a *Mikroelektromechanikai rendszerek* (GKNB_INTM020) tantárgyra készült.
### A célja egy "okos" parkoló rendszer készitése, mely hallgatói (és egyébb rfid) kártyák használatával kezeli a felhasználók beléptetését és az ehez szükséges és ez által felmerülő (belépési idő, stb.) adatokat egy adatbázisban tárolja, mely elérhető egy a Raspberry pi-on hostolt php weblapon.
Mellékelt file-ok és általuk elvégzet feladatok:
- 'addCard.py': új kártyák hozzá adása a rendszerhez
- 'removeCard.py': kártyák kivétele a rendszerből
- 'main.py': a program fő feladatainak elvégzése, kapu nyitása, kártyák beolvasása, informáciok közlése a felhasználóval és komunikáció a külső twitter serverekkel
-
-
Felhasznált python library-k és egyébb felhasznált források:
- [pirc522](https://github.com/ondyraso/pi-rc522): egy python library a Raspberry és a rc522 rfid olvasó közötti komunikációhoz
- [tweepy](https://github.com/tweep/tweepy): python library a twitter serverekhez való autentikációhoz és a tweetek küldéséhez
-
Egyébb információk, dokumentációk elérhetők a repository wiki szekciójában.

