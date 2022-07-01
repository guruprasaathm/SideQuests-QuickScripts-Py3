import requests
from requests.structures import CaseInsensitiveDict
import sqlite3

def bubbleSort(arr):
	n = len(arr)
	for i in range(n):
		for j in range(0, n-i-1):
			try:
				if arr[j]["total"] < arr[j+1]["total"] :
					arr[j+1], arr[j] = arr[j], arr[j+1]
			except:
				pass


def getMarks(rolln):
	url = "https://results.digitallocker.gov.in/results/MetaData_HSCER"
	headers = CaseInsensitiveDict()
	headers["accept"] = "*/*"
	headers["dnt"] = "1"
	headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
	data = f"rroll={rolln}&doctype=HSCER&sch=55145&year=2021"
	resp = requests.post(url, headers=headers, data=data)
	return resp.json()["DocDetails"]["MetadataContent"]

MarkDict = []

for roll in range(20652009, 20652055):
	thisMark = getMarks(roll)
	thisMarkSet = {}
	thisMarkSet["rno"] = thisMark["RROLL"]
	thisMarkSet["name"] = thisMark["CNAME"]
	thisMarkSet["sex"] = thisMark["SEX"]
	thisMarkSet["eng"] = int(thisMark["MRK13"])
	thisMarkSet["math"] = int(thisMark["MRK23"])
	thisMarkSet["phy"] = int(thisMark["MRK33"])
	thisMarkSet["chem"] = int(thisMark["MRK43"])
	thisMarkSet["cs"] = int(thisMark["MRK53"])
	thisMarkSet["bio"] = 0
	thisMarkSet["total"] = thisMarkSet["eng"] + thisMarkSet["math"] + thisMarkSet["phy"] +thisMarkSet["chem"] + thisMarkSet["cs"] + thisMarkSet["bio"]

	print(thisMarkSet["name"], thisMarkSet["total"])

	MarkDict.append(thisMarkSet)

for roll in range(20652055, 20652129):
	thisMark = getMarks(roll)
	thisMarkSet = {}
	thisMarkSet["rno"] = thisMark["RROLL"]
	thisMarkSet["name"] = thisMark["CNAME"]
	thisMarkSet["sex"] = thisMark["SEX"]
	thisMarkSet["eng"] = int(thisMark["MRK13"])
	thisMarkSet["math"] = int(thisMark["MRK23"])
	thisMarkSet["phy"] = int(thisMark["MRK33"])
	thisMarkSet["chem"] = int(thisMark["MRK43"])
	thisMarkSet["cs"] = 0
	thisMarkSet["bio"] = int(thisMark["MRK53"])
	thisMarkSet["total"] = thisMarkSet["eng"] + thisMarkSet["math"] + thisMarkSet["phy"] +thisMarkSet["chem"] + thisMarkSet["cs"] + thisMarkSet["bio"]

	print(thisMarkSet["name"], thisMarkSet["total"])

	MarkDict.append(thisMarkSet)

bubbleSort(MarkDict)

i=1
for elem in MarkDict:
	elem["rank"]=i
	i+=1

print(MarkDict)

with open('MarkData.db', 'wb+') as dbp:
	dbp.close()

con = sqlite3.connect('MarkData.db')
cur = con.cursor()

cur.execute('''CREATE TABLE marks
			   (rank int, rno int, name text, sex text, eng int, math int, phy int, chem int, cs int, bio int, total int)''')

for mark in MarkDict:
	cur.execute("INSERT INTO marks VALUES (?,?,?,?,?,?,?,?,?,?,?)", (mark["rank"], mark["rno"], mark["name"], mark["sex"], mark["eng"], mark["math"], mark["phy"], mark["chem"], mark["cs"], mark["bio"], mark["total"]))

con.commit()

con.close()