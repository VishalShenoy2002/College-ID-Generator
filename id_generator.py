from PIL import Image,ImageDraw,ImageFont
import csv
import qrcode
import random
import os


FONT=ImageFont.truetype("fonts/OpenSans-Bold.ttf",20)
ID_SIZE=(1000,500)


def getStudentList():
    '''
    Gets the list of students
    '''

    with open("students.csv","r") as f:
        reader=csv.DictReader(f)

        for row in reader:
            yield row

        f.close()

def createCard(filename:str,data:dict,face:str):
    '''
    Creates a New ID Card with respective qrcode
    '''
    imgx,imgy=ID_SIZE

    img=Image.new("RGB",ID_SIZE,color="white")

    facephoto=Image.open(face)
    idfacephoto=facephoto.resize((150,125))
    facex,facey=idfacephoto.size

    qrdata=f"{data['Course']}-{data['Batch']}-{data['Rollno']}-{data['Name']}"
    studentqr=qrcode.make(qrdata)
    studentqr=studentqr.resize((150,125))
    qrx,qry=studentqr.size

    # Gathering Data to Write Into the ID
    name=data.get("Name")
    rollnumber=data.get("Rollno")
    course=data.get("Course")
    batch=data.get("Batch")
    date_of_birth=data.get("Date of Birth")
    blood_group=data.get("Blood Group")
    contact=data.get("Contact Number")


    paintbrush=ImageDraw.Draw(img)
    paintbrush.rectangle([(50,50),(imgx-50,imgy-50)],outline="black",width=2)

    # Writing Name
    paintbrush.text((60,60),"Name:",fill="black",font=FONT)
    paintbrush.text((250,60),f"{name}",fill="black",font=FONT)
    
    # Writing Roll Number
    paintbrush.text((60,100),"Rollno:",fill="black",font=FONT)
    paintbrush.text((250,100),f"{rollnumber}",fill="black",font=FONT)
    
    # Writing Course
    paintbrush.text((60,140),"Course:",fill="black",font=FONT)
    paintbrush.text((250,140),f"{course}",fill="black",font=FONT)
    
    # Writing Batch
    paintbrush.text((60,180),"Batch:",fill="black",font=FONT)
    paintbrush.text((250,180),f"{batch}",fill="black",font=FONT)
    
    # Writing Date of Birth
    paintbrush.text((60,220),"Date of Birth:",fill="black",font=FONT)
    paintbrush.text((250,220),f"{date_of_birth}",fill="black",font=FONT)
    
    # Writing Blood Group
    paintbrush.text((60,260),"Blood Group:",fill="black",font=FONT)
    paintbrush.text((250,260),f"{blood_group}",fill="black",font=FONT)
    
    # Writing Contact Number
    paintbrush.text((60,300),"Contact Number:",fill="black",font=FONT)
    paintbrush.text((250,300),f"{contact}",fill="black",font=FONT)

    # Pasting the Face of the Student
    face_area=((imgx-facex-100),(imgy-facey)//5)
    Image.Image.paste(img,idfacephoto,face_area)

    # Pasting the student QR
    qr_area=((imgx-qrx-100),(imgy-qry+75)//2)
    Image.Image.paste(img,studentqr,qr_area)

    img.save(filename)
    studentqr.save("test.png")

if __name__=="__main__":
    for student in getStudentList():
        face=random.choice(os.listdir(os.path.join(os.getcwd(),"facepics")))
        filename=f"ids/{student['Course']}-{student['Batch']}-{student['Rollno']}-{student['Name']}.png"
        print(f"Creating ID of {student['Name']}")
        createCard(filename,student,os.path.join(os.getcwd(),"facepics",face))
    # break