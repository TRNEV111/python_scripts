__author__ = 'TNEVILL and ABREZNICKY'
#Populate_Measures

import arcpy,math

arcpy.env.workspace = "C:\\TxDOT\\Projects\\2015\\2015 Evaluation\\1_Populate_Measures"

spatialRef = arcpy.Describe("Eval_.gdb\Lines").spatialReference

rows = arcpy.da.UpdateCursor("Eval_.gdb\Lines",["SHAPE@","BMP","EMP","LEN","OBJECTID"]) #rows are the dataset
for row in rows: #the for statement is the loop that the updatecursor uses
    shape = row[0]
    bmp = row[1]
    emp = row[2]
    wholeLen = shape.length * .000621371 #converting the length into miles
    row[3]= wholeLen #populating the len field in the miles set up above
    print "OBJECTID: " + str(row[4])
    allparts = shape.getPart() #finding all the parts of the line
    count = allparts.count #gives the amount of parts found per record(row)
    partnum = 1 #a varible
    partAry = arcpy.Array()#This will be an empty list to feed geometry into
#more varibles
    srtPnt = 0 #the first point
    lastX = 0
    lastY = 0
    lastM = 0 #
    for part in allparts: #loop through the parts(lines)
        print "part: " + str(partnum) + " of " + str(count)
        aryPos = partnum - 1 # the array position
        ary = arcpy.Array() #empty container of the part it is working on
        totalNum = len(part) - 1 #the last array position (0)

        for pnt in part: # pnt is a new varible that is equal to each point (vertice)
            if srtPnt == 0: #starting on the first point of the line (only time used for that line)
                x = pnt.X #the value of the x for the point working on)
                y = pnt.Y #the value of the y for the point working on)
                m = 0 #start with a 0 first measure
                nupnt = arcpy.Point(x, y, 0, m) #telling arcpy what the x, y,z, m are (creating a point out of these values
                ary.add(nupnt)#created points are place in the array for that part
                #these following points are being saved
                lastX = x
                lastY = y
                lastM = m
                print str(x) + "," + str(y) + "," + str(m)
                srtPnt += 1 #this tells the next point to do something different
            else:
                x = pnt.X
                y = pnt.Y
                newM = (math.sqrt((abs(x - lastX)) ** 2 + (abs(y - lastY)) ** 2))#finding the distance to the new point
                m = lastM + (newM * .000621371)# adding that distance to the previous m of point
                print str(m)
                nupnt = arcpy.Point(x, y, 0, m)
                ary.add(nupnt)
                print str(x) + "," + str(y) + "," + str(m)
                lastX = x
                lastY = y
                lastM = m
        partAry.add(ary)
        partnum += 1
    row[0] = arcpy.Polyline(partAry, spatialRef, False, True)
    row[1] = 0
    row[2] = m
    rows.updateRow(row)
del rows
print "done"