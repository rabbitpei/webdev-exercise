__author__ = 'Pchen'
from Tkinter import *
import tkMessageBox
from urllib2 import Request, urlopen, URLError
import json
import time
import ttk 

class checkstatus(object):
    def __init__(self,pj):
        self.proj_name=pj
    def __call__(self):
        request=Request("https://api.github.com/repos/quixey/webdev-exercise/compare/baseline-branch..." + self.proj_name)
        try:
            response=urlopen(request)
            data=json.loads(response.read())
            try:
                val=data['status']
                tkMessageBox.showinfo(message="Status is "+str(val))
            except URLError,e:
                tkMessageBox.showinfo(message="Checking status failed.")
        except URLError,e:
            tkMessageBox.showinfo(message="Checking updated failed, please try again later.")

def show_projects(frame,CURRENT_PROJECTS):
    i=0
    row_start=2
    for pj in CURRENT_PROJECTS:
        row_start+=1
        lab2 = Label(text = pj[0],font='Helvetica -15')
        lab2.grid(row=row_start,column=1)
        lab2 = Label(text = pj[1],font='Helvetica -15')
        lab2.grid(row=row_start,column=2)
        lab2 = Label(text = pj[2],font='Helvetica -15')
        lab2.grid(row=row_start,column=3)
        lab2 = Label(text = pj[3]+"  ",font='Helvetica -15')
        lab2.grid(row=row_start,column=4)
        buttons = Button(frame, text="check update",command=checkstatus(pj[2]))
        buttons.grid(row=row_start,column=5,sticky=W)
        i+=1

def addproj():
    proj_type=enter1.get()
    proj_name=enter2.get()
    if len(proj_type)<1:
        tkMessageBox.showinfo(message="Can't create a project with empty type!")      
        enter2.delete(0,END)
        return
    if len(proj_name)<1:
        tkMessageBox.showinfo(message="Can't create a project with empty name!")
        enter1.delete(0,END)
        return
    if proj_name in project_set:
        tkMessageBox.showinfo(message="The project is already in the list!")
        enter1.delete(0,END)
        enter2.delete(0,END)
        return
    request=Request('https://api.github.com/repos/quixey/webdev-exercise/branches/'+proj_name)
    tkMessageBox.showinfo(message="Querying if this project exists in Github!")
    try:
        response=urlopen(request)
        newproj=(str(len(CURRENT_PROJECTS)+1),proj_type,proj_name,time.strftime("%m-%d-%Y %H:%M:%S", time.localtime()))
        CURRENT_PROJECTS.append(newproj)
        project_set.add(proj_name)
        row_start=2+len(CURRENT_PROJECTS)
        lab2 = Label(text = newproj[0],font='Helvetica -15')
        lab2.grid(row=row_start,column=1)
        lab2 = Label(text = newproj[1],font='Helvetica -15')
        lab2.grid(row=row_start,column=2)
        lab2 = Label(text = newproj[2],font='Helvetica -15')
        lab2.grid(row=row_start,column=3)
        lab2 = Label(text = newproj[3]+"  ",font='Helvetica -15')
        lab2.grid(row=row_start,column=4)
        buttonsa = Button(win, text="check update",command=checkstatus(newproj[2]))
        buttonsa.grid(row=row_start,column=5,sticky=W)
    except URLError, e:
        tkMessageBox.showinfo(message="Didn't find the project in Github, please reenter the info!")
    enter1.delete(0,END)
    enter2.delete(0,END)

    
CURRENT_PROJECTS=[("1","Training","Patrick's experimental branch   ","6-7-2014 13:19:02  "),
                   ("2","Testing","Blind test of autosuggest model   ","21-7-2014 18:47:49  ")]
project_set=set(["Patrick's experimental branch","Blind test of autosuggest model"])

win= Tk()  
win.title('Project overview')    
lab1=Label(text="All",font='Helvetica -25 bold').grid(row=1,column=0,sticky=W)
lab1=Label(text="active projects",font='Helvetica -25 bold').grid(row=1,column=1,sticky=W)
lab1=Label(text="ID",font='Helvetica -18 bold').grid(row=2,column=1)
lab1=Label(text="Type",font='Helvetica -18 bold').grid(row=2,column=2)
lab1=Label(text="Name   ",font='Helvetica -18 bold').grid(row=2,column=3)
lab1=Label(text="Last activity",font='Helvetica -18 bold').grid(row=2,column=4)
show_projects(win,CURRENT_PROJECTS)
row_start=2+len(CURRENT_PROJECTS)

lab1=Label(text=" ").grid(row=100,column=0,sticky=W)
lab1=Label(text="Add",font='Helvetica -25 bold').grid(row=101,column=0,sticky=W)
lab1=Label(text="new project",font='Helvetica -25 bold').grid(row=101,column=1,sticky=W)
lab1=Label(text="Project type",font='Helvetica -15').grid(row=102,column=1,sticky=W)
lab1=Label(text="Project name",font='Helvetica -15').grid(row=103,column=1,sticky=W)
enter1 = ttk.Combobox(win, textvariable="", values=["training", "testing", "analysising"])
enter1.grid(row=102,column=2,sticky=W)
#enter1=Entry(win,text='type')
#enter1.grid(row=102,column=2,sticky=W)
enter2=Entry(win,text='name')
enter2.grid(row=103,column=2,sticky=W)
button3 = Button(win, text="Add project",command=addproj).grid(row=104,column=1,sticky=W)

mainloop()
