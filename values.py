days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

studentData = {
    "personalData" : {
        "name": str,
        "lastName": str,
        "career": int,
        "careerName": str
    },
    "classes" : {},
    "schedule": { day: {module : {"class" : str, "classroom": str} for module in range(1, 10)} for day in days }
}

personalClassesGap = 19
xoffset = 5
yoffset = 3
yjump = 9
xsize = 65
ysize = 30
correction = 10
testClassWidth = 16

