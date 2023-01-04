import pdfquery
from values import days, studentData, xoffset, \
                   xsize, yoffset, yjump, ysize, \
                   correction, testClassWidth, classY

# Opens and loads the files that will be used during execution
testFile = open("TEST.txt", "w")
pdf = pdfquery.PDFQuery('sample1.pdf')
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
classNumber = str(pdf.pq(f'LTTextLineHorizontal:overlaps_bbox("20, {classY}, 44, {classY + 15}")').text()).strip()
#print(classY, classNumber)
classes = 0
while classNumber.isdigit():
    classes+=1
    classData = pdf.pq(f'LTTextLineHorizontal:overlaps_bbox("45, {classY}, 504, {classY + 15}")').text().rsplit(" ", 2)
    #print(classData)
    classData[0] = classData[0].split(" ", 1)
    classData = {"code": classData[0][0], "class": classData[0][1], "coord": classData[1], "type": classData[2]}
    studentClasses[int(classNumber)] = classData

    classY -= testClassWidth
    classNumber = str(pdf.pq(f'LTTextLineHorizontal:overlaps_bbox("20, {classY}, 44, {classY + 15}")').text()).strip()
    #print(classNumber, classY)


# Due to pdfquery's way of working with pdf pages, the point
# represents the lower left corner.
scheduleHeight = classY - 46
originalPoint = [169.000, scheduleHeight]
point = [originalPoint[0] - xsize - xoffset, originalPoint[1]]


# Fetches the class and the classroom from every module of every day.
# Also, makes sure classroom and class are given in order
for x in range(6):
    point[0] += xsize + xoffset
    point[1] = originalPoint[1]
    for y in range(9):
        texto = pdf.pq(f'LTTextLineHorizontal:overlaps_bbox("{point[0] + correction}, {point[1] + correction}, {point[0] + xsize - correction}, {point[1] + ysize - correction}")').text()
        #print(point)
        if texto:
            texto = texto.split(" ")
            #print(texto, days[x], y)
            if texto[0] == 'Sala:':
                studentSchedule[days[x]][y + 1]['class'] = texto[1]
                studentSchedule[days[x]][y+1]['classroom'] = texto[2]
            else:
                studentSchedule[days[x]][y + 1]['class'] = texto[0]
                studentSchedule[days[x]][y+1]['classroom'] = texto[2]
        else:
            studentSchedule[days[x]][y + 1]['class'] = None
            studentSchedule[days[x]][y+1]['classroom'] = None

        point[1] -= ysize + yoffset
        if (1 + y) % 3 == 0:
            point[1] -= yjump


print(studentData)
testFile.write(str(studentData))
# Bloques de clase
# SALTOS HORIZONTALES DE 70 ENTRE INICIO E INICIO
# X MÁS O MENOS 182.05 ---> 170

#bbox="[182.05, 430.201, 220.956, 437.201]" word_margin="0.1">13308-0-A-1
#print("classes: " +  str(classes))

# Y += 30
# Y + GAP = 33
# 239 -> 304
# X += 64
# X + GAP = 69


'''<LTLine y0="478.0" y1="478.0" x0="168.75" x1="234.25"
<LTLine y0="447.75" y1="478.25" x0="169.0" x1="169.0"
<LTLine y0="448.0" y1="448.0" x0="168.75" x1="234.25"
<LTLine y0="447.75" y1="478.25" x0="234.0" x1="234.0"
<LTLine y0="445.0" y1="445.0" x0="168.75" x1="234.25"
<LTLine y0="414.75" y1="445.25" x0="169.0" x1="169.0"
<LTLine y0="415.0" y1="415.0" x0="168.75" x1="234.25"
<LTLine y0="414.75" y1="445.25" x0="234.0" x1="234.0"
<LTLine y0="412.0" y1="412.0" x0="168.75" x1="234.25"
<LTLine y0="381.75" y1="412.25" x0="169.0" x1="169.0"
<LTLine y0="382.0" y1="382.0" x0="168.75" x1="234.25"
<LTLine y0="381.75" y1="412.25" x0="234.0" x1="234.0"
<LTLine y0="478.0" y1="478.0" x0="238.75" x1="304.25"
<LTLine y0="447.75" y1="478.25" x0="239.0" x1="239.0"
<LTLine y0="448.0" y1="448.0" x0="238.75" x1="304.25"
<LTLine y0="447.75" y1="478.25" x0="304.0" x1="304.0"
<LTLine y0="445.0" y1="445.0" x0="238.75" x1="304.25"'''



    

    




#print(studentData)

