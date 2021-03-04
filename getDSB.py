import pydsb
import json
import urllib.request
from bs4 import BeautifulSoup
import re
from os import path
import os
from plyer import notification
import certifi
from datetime import datetime


def getWholeTable(*args):
    maxNewDate = None
    print("args")
    print(args)
    configPath = "config.json"
    listdir = os.listdir("Tables")
    with open(configPath,"r" , encoding="utf-8") as datei:
        conf=json.loads(datei.read())
    dsb = pydsb.PyDSB(conf["benutzer"],conf["passwort"])
    klassen = conf["klassen"].split(",")
    try:
        timetables=dsb.get_plans()
    except:
        return
    tabInfos = []
    toCompare = []

    if timetables == None:
        return
    with open("Tables/lastUpdateFull.txt", "r", encoding="utf-8")as lastUpdate:
        lUpdate = datetime.strptime(lastUpdate.read(), '%d.%m.%Y %H:%M')
    for table in timetables:
        tableLUpdate = datetime.strptime(table["uploaded_date"],'%d.%m.%Y %H:%M')
        if lUpdate >= tableLUpdate:
            print("hash stimmt überein")
            continue
        else:
            if not maxNewDate == None:
                if maxNewDate < tableLUpdate:
                    maxNewDate = tableLUpdate
            else:
                maxNewDate = tableLUpdate

        #print(table)
        with urllib.request.urlopen(table["url"],cafile=certifi.where()) as f:
            print("type(f)")
            print(type(f))
            timetabledata = str(f.read().decode("latin1").encode('utf8').decode("utf-8")) # .decode('utf-8')

        soup = BeautifulSoup(timetabledata, 'html.parser')
        tableInfoTag = soup.find('div', attrs={'class': 'mon_title'})
        tableInfo = tableInfoTag.text.strip()
        tableInfo = re.sub('\([^)]+\)', " ", tableInfo)
        file = "Tables/Total_" + tableInfo.replace(" ", "") + ".html"
        #print(tableInfo)
        reineTabelle = soup.find('table', attrs={'class': 'mon_list'})
        legende = reineTabelle.find("tr")
        reineTabellestr = reineTabelle.text.strip()

        comp = False
        if path.exists(file)and tableInfo+".compare" in tabInfos:
            if not file in toCompare:
                toCompare.append(file)
            file = file + ".compare"

            comp = True
            tableInfo += ".compare"

        if tableInfo in tabInfos:
            #print("true")
            with open(file, "r", encoding="utf-8")as datei:
                content = datei.read()
            with open(file, "w", encoding="utf-8")as datei:
                datei.write(content.split("</table>")[0])
                for einzeln in reineTabelle.findAll('tr'):
                    einzelTrStr = str(einzeln)
                    datei.write(einzelTrStr)
                datei.write("</table></body>")
        else:
            if path.exists(file):
                if not file in toCompare:
                    toCompare.append(file)
                file = file + ".compare"

                comp = True
                tableInfo += ".compare"

            with open(file, "w", encoding="utf-8")as datei:
                datei.write("\n<body>")
                datei.write(re.sub('\([^)]+\)', " ",str(tableInfoTag)))
                datei.write("<table>")
                datei.write(str(legende))

                for einzeln in reineTabelle.findAll('tr'):
                    einzelTrStr = str(einzeln)
                    datei.write(einzelTrStr)

                datei.write("</table></body>")
                tabInfos.append(tableInfo)
    if not maxNewDate == None:
        with open("Tables/lastUpdateFull.txt", "w")as updateFile:
            updateFile.write(maxNewDate.strftime('%d.%m.%Y %H:%M'))
    print(toCompare)
    for file in toCompare:
        with open(file, "r", encoding="utf-8")as datei:
            soup = BeautifulSoup(datei.read(), 'html.parser')
        compfilename = file+".compare"
        with open(compfilename, "r", encoding="utf-8")as compdatei:
            compSoup = BeautifulSoup(compdatei.read(), 'html.parser')

        for x in soup.find_all():
            if len(x.get_text(strip=True)) == 0:
                x.extract()
        soup = soup.prettify()

        for x in compSoup.find_all():
            if len(x.get_text(strip=True)) == 0:
                x.extract()
        compSoup = compSoup.prettify()
        if str(soup) == str(compSoup):
            os.remove(compfilename)
            print("removed copy")
        else:
            os.remove(file)
            os.rename(compfilename,file)


def getContent(total=False,*args):
    try:
        urllib.request.urlopen("https://www.dsbmobile.de",cafile=certifi.where())
    except:
        return


    maxNewDate = None
    if total:
        getWholeTable()
    
    print("args")
    print(args)
    configPath = "config.json"
    listdir = os.listdir("Tables")
    with open(configPath,"r" , encoding="utf-8") as datei:
        conf=json.loads(datei.read())
    dsb = pydsb.PyDSB(conf["benutzer"],conf["passwort"])
    klassen = conf["klassen"].replace(" ","").split(",")
    print(klassen)
    try:
        timetables=dsb.get_plans()
    except:
        return
    #print(timetables)
    tabInfos = []
    toCompare = []
    if timetables == None:
        return
    print(timetables)
    with open("Tables/lastUpdate.txt", "r", encoding="utf-8")as lastUpdate:
        lUpdate = datetime.strptime(lastUpdate.read(), '%d.%m.%Y %H:%M')

    for table in timetables:
        tableLUpdate = datetime.strptime(table["uploaded_date"],'%d.%m.%Y %H:%M')
        if lUpdate >= tableLUpdate:
            print("hash stimmt überein")
            continue
        else:
            if not maxNewDate == None:
                if maxNewDate<tableLUpdate:
                    maxNewDate = tableLUpdate
            else:
                maxNewDate = tableLUpdate
            print("hash stimmt nicht überein\nsetze Fort")
        print("table")
        print(table)
        with urllib.request.urlopen(table["url"],cafile=certifi.where()) as f:
            #f = f.decode('utf-8')
            timetabledata = str(f.read().decode("latin1").encode('utf8').decode("utf-8")) #.encode('utf8'))
            with open("test.txt","w",encoding="utf-8") as test:
                test.write(timetabledata)







        soup = BeautifulSoup(timetabledata, 'html.parser')
        head = tableInfoTag = soup.head
        #print(str(head))
        tableInfoTag = soup.find('div', attrs={'class': 'mon_title'})
        tableInfo = tableInfoTag.text.strip()
        tableInfo = re.sub('\([^)]+\)', " ", tableInfo)
        #print(tableInfo)
        reineTabelle = soup.find('table', attrs={'class': 'mon_list'})
        legende = reineTabelle.find("tr")
        reineTabellestr = reineTabelle.text.strip()
        file = "Tables/"+tableInfo.replace(" ","")+".html"
        comp = False
        print(tabInfos)
        if path.exists(file)and tableInfo+".compare" in tabInfos:
            if not file in toCompare:
                toCompare.append(file)
            file = file + ".compare"

            comp = True
            tableInfo += ".compare"

        if tableInfo in tabInfos:
            #print("true")
            with open(file, "r", encoding="utf-8")as datei:
                content = datei.read()
            with open(file, "w", encoding="utf-8")as datei:
                datei.write(content.split("</table>")[0])
                for klasse in klassen:
                    for einzeln in reineTabelle.findAll('td'):

                        if (klasse.lower() in str(einzeln).lower()):

                            einzelTr = einzeln.find_parent('tr')
                            einzelTrStr = str(einzelTr)

                            datei.write(einzelTrStr)
                            #print(einzelTrStr)
                            #print(type(einzelTrStr))
                datei.write("</table></body>")
        else:
            if path.exists(file):
                if not file in toCompare:
                    toCompare.append(file)
                file = file + ".compare"

                comp = True
                tableInfo += ".compare"

            anzTrs = 0
            with open(file, "w", encoding="utf-8")as datei:
                datei.write(str(head)+"\n<body>")
                datei.write(re.sub('\([^)]+\)', " ",str(tableInfoTag)))
                datei.write("<table>")
                datei.write(str(legende))

                for klasse in klassen:
                    for einzeln in reineTabelle.findAll('td'):
                        if (klasse.lower() in str(einzeln).lower()):
                            anzTrs+=1
                            einzelTr = einzeln.find_parent('tr')
                            einzelTrStr = str(einzelTr)

                            datei.write(einzelTrStr)
                            #print(einzelTrStr)
                            #print(type(einzelTrStr))
                datei.write("</table></body>")

            if anzTrs == 0:
                os.remove(file)
            else:
                tabInfos.append(tableInfo)
    if not maxNewDate == None:
        with open("Tables/lastUpdate.txt", "w")as updateFile:
            updateFile.write(maxNewDate.strftime('%d.%m.%Y %H:%M'))

    print("toCompare")
    print(toCompare)
    for file in toCompare:
        with open(file, "r", encoding="utf-8")as datei:
            soup = BeautifulSoup(datei.read(), 'html.parser')
        compfilename = file+".compare"
        with open(compfilename, "r", encoding="utf-8")as compdatei:
            compSoup = BeautifulSoup(compdatei.read(), 'html.parser')

        for x in soup.find_all():
            if len(x.get_text(strip=True)) == 0:
                x.extract()
        soup = soup.prettify()

        for x in compSoup.find_all():
            if len(x.get_text(strip=True)) == 0:
                x.extract()
        compSoup = compSoup.prettify()
        if str(soup) == str(compSoup):
            os.remove(compfilename)
            print("removed copy")
        else:
            print("removed Original::::")
            notification.notify(title="DSB NEWS", message ="Es sind für Sie relevante Veränderungen auf dem Vertretungsplan entstanden",
                   app_name ="DSB News", app_icon ="", timeout = 10, ticker ="", toast = False)
            print(str(soup))
            print("Secon:")
            print(str(compSoup))
            os.remove(file)
            os.rename(compfilename,file)
    if not listdir == os.listdir("Tables"):
        notification.notify(title="DSB NEWS", message="Es sind für Sie relevante Veränderungen auf dem Vertretungsplan entstanden",
               app_name="DSB News", app_icon="", timeout=10, ticker="", toast=False)


#getContent(total=True)