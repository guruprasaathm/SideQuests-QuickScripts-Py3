from aiohttp import ClientSession
from asyncio import get_event_loop
from aiofiles import open as aio_open
from PyPDF2 import PdfFileReader, PdfFileWriter
from os import remove

__author__="GuruPrasaath Manirajan"

def pdf_cat(input_files, output_stream):
	input_streams = []
	try:
		for input_file in input_files:
			input_streams.append(open(input_file, 'rb'))
		writer = PdfFileWriter()
		for reader in map(PdfFileReader, input_streams):
			for n in range(reader.getNumPages()):
				writer.addPage(reader.getPage(n))
		writer.write(output_stream)
	finally:
		for f in input_streams:
			f.close()

async def main():
	async with ClientSession() as session:
		for subject in ['mh', 'ph', 'ch']:
			temp_fp_arr = []
			for bookno in [1,2]:
				pdfcode = 1
				while True:
					rgeturl = "https://ncert.nic.in/textbook/pdf/le{}{}0{}.pdf".format(subject, bookno, pdfcode)
					async with session.get(rgeturl) as r:
						if r.headers['content-type'] == "application/pdf":
							f = await aio_open("{}{}{}.pdf".format(subject, bookno, pdfcode), mode='wb+')
							await f.write(await r.read())
							await f.close()

							temp_fp_arr.append("{}{}{}.pdf".format(subject, bookno, pdfcode))
						else:
							break

						pdfcode+=1

			else:
				with open("{}.pdf".format(subject), "wb+") as wf:
					pdf_cat(temp_fp_arr, wf)
				for file in temp_fp_arr:
					remove(file)

loop = get_event_loop()
loop.run_until_complete(main())


'''
driver = webdriver.Chrome()

driver.get('')

std_wait = WebDriverWait(driver, 5)
ext_wait = WebDriverWait(driver, 10)
'''