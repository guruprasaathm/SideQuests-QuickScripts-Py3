from requests import get as rget
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timezone, timedelta, time
from dateutil import tz

__author__ = "GuruPrasaath Manirajan"

class scheduleTSU:
	def __init__(self):
		self.classes = []
		self.tomskTimeZ = timezone(timedelta(hours=7))
		self.tomsk = tz.gettz('Asia/Tomsk')
		self.schedule = self.extractDaySchedule()

	def toEnglish(self, russianText):
		url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
		params = {
			"key":"trnsl.1.1.20210903T155007Z.ca995aee2a661b20.5d5215852af62a9433a3927c2855c9ec0949ec31",
			"text":russianText,
			"lang":"ru-en",
			"format":"plain"
		}
		yandexRequest = rget(url, params=params)

		return yandexRequest.json()["text"][0]

	def requestWeeklySchedule(self):
		url = "https://intime.tsu.ru/api/schedule/group/4e0e15aa-0699-11ec-816a-005056bc249c?dateStart=1630281600&dateEnd=1630799999"

		headers = CaseInsensitiveDict()
		headers["Connection"] = "keep-alive"
		headers["Accept"] = "application/json, text/plain, */*"
		headers["DNT"] = "1"
		headers["sec-ch-ua-mobile"] = "?0"
		headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
		headers["Sec-Fetch-Site"] = "same-origin"
		headers["Sec-Fetch-Mode"] = "cors"
		headers["Sec-Fetch-Dest"] = "empty"
		headers["Referer"] = "https://intime.tsu.ru/schedule/group/4e0e15aa-0699-11ec-816a-005056bc249c?name=972105"
		headers["Accept-Language"] = "en-US,en;q=0.9"

		resp = rget(url, headers=headers)

		return resp.json()

	def extractDaySchedule(self):
		schedule_dict = self.requestWeeklySchedule()

		now = datetime.now(timezone.utc)
		today_midnight = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		today = str(int(datetime.timestamp(today_midnight)))

		today_schedule = schedule_dict["data"][today]['schedule']

		tomskTime = datetime.now(self.tomskTimeZ).date()

		Classes = []
		for class_session in today_schedule:

			class_name = self.toEnglish(class_session["title"])
			teacher = self.toEnglish(class_session["teacher"]["name"])

			tomskStart = class_session["starts"]
			tomskEnd = class_session["ends"]

			starts_datetime = datetime.combine(tomskTime, time(int(tomskStart[:2]), int(tomskStart[3:])), tzinfo=self.tomsk).astimezone()
			ends_datetime = datetime.combine(tomskTime, time(int(tomskEnd[:2]), int(tomskEnd[3:]))).astimezone()

			starts_formatted = starts_datetime.strftime("%I:%M %p")
			ends_formatted = ends_datetime.strftime("%I:%M %p")

			Classes.append({"class":class_name, "teacher":teacher, "starts":starts_formatted, "ends":ends_formatted})

		return Classes

today = (datetime.now().date())

scheduleObj = scheduleTSU()
CurrentSchedule = scheduleObj.schedule

writeStr = f'''\t\t   Classes for {today.strftime("%A, %d-%m-%y")}\n\n'''

for class_session in CurrentSchedule:
	cur_str = class_session["class"] + " - " + class_session["teacher"] + " - " + class_session["starts"] + " to " + class_session["ends"] + "\n"
	writeStr = writeStr + cur_str

print(writeStr)

with open(today.strftime("%A, %d-%m-%y")+".txt", 'w+') as fp:
	fp.write(writeStr)

print("\nWritten to text file!")