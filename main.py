import pdfquery
from values import days, studentData, xoffset, \
                   xsize, yoffset, yjump, ysize, \
                   correction, testClassWidth, personalClassesGap

from functions import getTextHeight, getClass, getClassNumber, getModule

# Opens and loads the files that will be used during execution
testFile = open("TEST.txt", "w")
pdf = pdfquery.PDFQuery('sample5.pdf')
pdf.load()


# Creates shortcuts for used dictionaries
studentClasses = studentData["classes"]
studentSchedule = studentData["schedule"]
personalData = studentData["personalData"]


# Fetches the personalData from the pdf 
personalData["name"] = pdf.pq('LTTextLineHorizontal:overlaps_bbox("442.72, 667.574, 514.288, 675.574")').text()
personalData["lastName"] = pdf.pq('LTTextLineHorizontal:overlaps_bbox("158.55, 667.574, 179.446, 675.574")').text()
personalData["career"] = pdf.pq('LTTextLineHorizontal:overlaps_bbox("42.22, 644.131, 57.788, 651.131")').text()
personalData["careerName"] = pdf.pq('LTTextLineHorizontal:overlaps_bbox("247.13, 644.131, 368.874, 651.131")').text()


# Fetches the first class (How would you have an schedule if you don't have any classes)
# and then checks the next rows until there are no more classes.
firstClassHeight = getTextHeight(pdf, "NOMBRE ASIGNATURA")
classY = float(firstClassHeight) - personalClassesGap
classNumber = getClassNumber(pdf, classY)
classes = 0
while classNumber.isdigit():
    classes+=1
    studentClasses[int(classNumber)] = getClass(pdf, classY)

    classY -= testClassWidth
    classNumber =  getClassNumber(pdf, classY)


# Due to pdfquery's way of working with pdf pages, the point
# represents the lower left corner.
scheduleY = getTextHeight(pdf, "LUNES")
scheduleHeight = float(classY) - 44
originalPoint = [169.000, scheduleHeight]
point = [originalPoint[0] - xsize - xoffset, originalPoint[1]]


# Fetches the class and the classroom from every module of every day.
# Also, makes sure classroom and class are given in order
for x in range(6):
    point[0] += xsize + xoffset
    point[1] = originalPoint[1]
    for y in range(9):
        studentSchedule[days[x]][y+1] = getModule(pdf, point[0], point[1],
                                                  xsize, ysize, correction)

        point[1] -= ysize + yoffset
        if (1 + y) % 3 == 0:
            point[1] -= yjump


print(studentData)
testFile.write(str(studentData))


