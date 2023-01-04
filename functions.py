import pdfquery
from values import days

# Returns the height of the lower left corner of a text line
# that matches {text} in a pdf
def getTextHeight(pdf, text) -> str:
    return pdf.pq(f'LTTextLineHorizontal:contains("{text}")').attr('y0')

# Returns the number of the class at certain height of
# the document
def getClassNumber(pdf, lowerLeftCorner) -> str:
    return str(pdf.pq(f'LTTextLineHorizontal:overlaps_bbox("20, {lowerLeftCorner}, 44, {lowerLeftCorner + 15}")').text()).strip()

# Returns a dict containing all relevant information of a class
def getClass(pdf, lowerLeftCorner) -> dict:
    classDict = {'code': str, 'class': str, 'coord': str, 'type': str}
    classData = pdf.pq(f'LTTextLineHorizontal:overlaps_bbox("45, {lowerLeftCorner}, 504, {lowerLeftCorner + 15}")').text()
    classData = classData.rsplit(" ", 2)
    classDict['coord'], classDict['type'] = classData[1], classData[2]
    classData = classData[0].split(" ", 1)
    classDict['code'] = classData[0]
    classDict['class'] = classData[1]

    return classDict

# Returns a dict containing all relevant information of a schedule module.
def getModule(pdf, x0, y0,moduleWidth,
              moduleHeight,correction) -> dict:
    module = {'class': str, 'classroom': str}
    moduleData:str = pdf.pq(f'LTTextLineHorizontal:overlaps_bbox("{x0 + correction}, {y0 + correction}, {x0 + moduleWidth - correction}, {y0 + moduleHeight - correction}")').text()
    if moduleData:
        moduleData:list = moduleData.split(" ")
        if moduleData[0] == 'Sala:':
            module['class'] = moduleData[1]
            module['classroom'] = moduleData[2]
        else:
            module['class'] = moduleData[0]
            module['classroom'] = moduleData[2]
            if len(moduleData) == 4 :
                module['classroom'] += moduleData[3]

    else:
        module['class'] = None
        module['classroom'] = None

    return module