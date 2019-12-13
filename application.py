from tkinter import *
from connect import *
import tkinter.ttk as ttk
import tkinter as tk
from calls import *
from proc import *

objects=[]

db_connect = {'port': 5432,
              'host': 'localhost',
              'user': "postgres",
              'dbname': 'test', }


counter = 0

def get_appointments_call():
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('get_appointments', ())
    return view(tree, cur.fetchall())

def search_appointments_view():
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('get_appointments', ())
    return view(tree, cur.fetchall())

def add_appointment():
    list_enters=[e1, e2, e3, comboExample, e5, e6]
    values = tuple([e.get() for e in list_enters])
    if not all([True if value!='' else False for value in values]):
        new_window = Toplevel(window)
        label = Label(new_window, text='Please, enter the data')
        label.grid(row=0, column=0)
        return


    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('insert_appointment', values)
    cur.close()
    conn.commit()
    get_appointments_call()
    for enter in list_enters:
        enter.delete(0, END)

def search_app_call():
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    _e2 = e2.get() if e2.get() != '' else '01-01-0001'
    _e5 = e5.get() if e5.get() != '' else -1
    cur.callproc('search_appointment', (e1.get(), _e2, e3.get(), comboExample.get(), _e5, e6.get()))
    return view(tree, cur.fetchall())

def focus_appo():
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    item = tree.item(tree.focus())['values']
    cur.callproc('delete_exact_app', item)
    cur.close()
    conn.commit()

def view(tree, records):
    tree.delete(*tree.get_children())
    for record in records:
        output_text = []
        for item in record:
            output_text.append(str(item))
        tree.insert('', 'end', text=output_text[0],
                    values=tuple(output_text[1:]))


def all_patients_view():
    new_window = Toplevel(window)
    tree = ttk.Treeview(new_window,
                        columns=('ID', 'Name',
                                 'Date of birth', 'Sex'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Name')
    tree.heading('#2', text='Date of birth')
    tree.heading('#3', text='Sex')

    tree.column('#0', stretch=YES, width=30)
    tree.column('#1', stretch=YES, width=150)
    tree.column('#2', stretch=YES, width=150)
    tree.column('#3', stretch=YES, width=100)
    tree.grid(row=2, columnspan=4, sticky='nsew')

    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('view_patients')
    records = cur.fetchall()
    conn.close()
    view(tree, records)


def all_doctors_view():
    new_window = Toplevel(window)
    tree = ttk.Treeview(new_window,
                        columns=('Name', 'Profession',
                                 'Experience'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Name')
    tree.heading('#2', text='Profession')
    tree.heading('#3', text='Experience')

    tree.column('#0', stretch=YES, width=30)
    tree.column('#1', stretch=YES, width=150)
    tree.column('#2', stretch=YES, width=80)
    tree.column('#3', stretch=YES, width=80)
    tree.grid(row=2, columnspan=4, sticky='nsew')

    conn = psycopg2.connect(**db_connect)

    cur = conn.cursor()
    cur.callproc("view_doctors")
    records = cur.fetchall()
    conn.close()
    view(tree, records)

def new_doctor_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, add a new doctor")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)
    l2 = Label(new_window, text='Profession')
    l2.grid(row=1, column=2)
    l3 = Label(new_window, text='Experience')
    l3.grid(row=3, column=0)

    name = StringVar()
    e1 = Entry(new_window, textvariable=name)
    e1.grid(row=1, column=1)
    profession = StringVar()
    e2 = Entry(new_window, textvariable=profession)
    e2.grid(row=1, column=3)
    experience = StringVar()
    e3 = Entry(new_window, textvariable=experience)
    e3.grid(row=3, column=1)

    add_doctor_to_datebase = Button(new_window, text='Add', width=12,
                                    command=lambda: insert_doctor_call(e1.get(), e2.get(), e3.get(), new_window))
    add_doctor_to_datebase.grid(row=4, column=3)
    new_window.mainloop()

def delete_patient_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, delete a patient")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)
    l2 = Label(new_window, text='Date of birth')
    l2.grid(row=1, column=2)

    e1 = Entry(new_window, textvariable=StringVar())
    e1.grid(row=1, column=1)

    e2 = Entry(new_window, textvariable=StringVar())
    e2.grid(row=1, column=3)


    _e2 = e2.get() if e2.get() != '' else '01-01-0001'

    del_patient_from_datebase = Button(new_window, text='Delete', width=12,
                                    command=lambda: delete_patient_call(e1.get(), _e2, new_window))
    del_patient_from_datebase.grid(row=4, column=3)
    new_window.mainloop()

def search_patient_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, search a patient")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)
    l2 = Label(new_window, text='Date of birth')
    l2.grid(row=1, column=2)
    l3 = Label(new_window, text='Sex')
    l3.grid(row=2, column=0)

    name = StringVar()
    e1 = Entry(new_window, textvariable=name)
    e1.grid(row=1, column=1)
    datebirth = StringVar()
    e2 = Entry(new_window, textvariable=datebirth)
    e2.grid(row=1, column=3)
    sex = StringVar()
    e3 = Entry(new_window, textvariable=sex)
    e3.grid(row=2, column=1)

    tree = ttk.Treeview(new_window,
                        columns=('ID', 'Name',
                                 'Date of birth', 'Sex'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Name')
    tree.heading('#2', text='Date of birth')
    tree.heading('#3', text='Sex')

    tree.column('#0', stretch=YES, width=30)
    tree.column('#1', stretch=YES, width=150)
    tree.column('#2', stretch=YES, width=150)
    tree.column('#3', stretch=YES, width=100)
    tree.grid(row=3, columnspan=5, sticky='nsew')


    _e2 = e2.get() if e2.get() != '' else '01-01-0001'
    #
    add_patient_to_datebase = Button(new_window, text='Search patient', width=12,
                                     command=lambda: view(tree, search_patient_call(e1.get(), _e2, e3.get())))

    add_patient_to_datebase.grid(row=2, column=3)

#new
def delete_doctor_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, delete a doctor")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)

    e1 = Entry(new_window, textvariable=StringVar())
    e1.grid(row=1, column=1)

    del_doctor_from_datebase = Button(new_window, text='Delete', width=12,
                                    command=lambda: delete_doctor_call(e1.get(), new_window))
    del_doctor_from_datebase.grid(row=4, column=3)
    new_window.mainloop()


def new_patient_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, add a new patient")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)
    l2 = Label(new_window, text='Date of birth')
    l2.grid(row=1, column=2)
    l3 = Label(new_window, text='Sex')
    l3.grid(row=2, column=0)

    name = StringVar()
    e1 = Entry(new_window, textvariable=name)
    e1.grid(row=1, column=1)
    datebirth = StringVar()
    e2 = Entry(new_window, textvariable=datebirth)
    e2.grid(row=1, column=3)
    sex = StringVar()
    e3 = Entry(new_window, textvariable=sex)
    e3.grid(row=2, column=1)

    add_patient_to_datebase = Button(new_window, text='Add patient', width=12,
                                     command=lambda: insert_patient_call(e1.get(), e2.get(), e3.get(), new_window))
    add_patient_to_datebase.grid(row=2, column=3)

    # _e2 = e2.get() if e2.get() != '' else '01-01-0001'
    #
    # del_patient_from_datebase = Button(new_window, text='Del patient', width=12,
    #                                  command=lambda: search_patient_call(e1.get(), _e2, e3.get()))
    # del_patient_from_datebase.grid(row=3, column=3)

    new_window.mainloop()


def delete_db2():
    delete_database()
    window.destroy()

def delete_db1():
    new_window = Toplevel(window)
    del_button = Button(new_window, text='Delete the database?', height=4,
                                     command=delete_db2)
    del_button.grid(row=1, column=1)
    new_window.mainloop()



window = Tk()

l1 = Label(window, text='Name')
l1.grid(row=0, column=0)
objects.append(l1)

l2 = Label(window, text='Date of birth')
l2.grid(row=0, column=2)
objects.append(l2)

l3 = Label(window, text='Service')
l3.grid(row=0, column=4)
objects.append(l3)

l4 = Label(window, text='Doctors')
l4.grid(row=1, column=0)
objects.append(l4)

l5 = Label(window, text='Price')
l5.grid(row=1, column=2)
objects.append(l5)

l6 = Label(window, text='Time')
l6.grid(row=1, column=4)
objects.append(l6)

## =====================================

e1 = Entry(window, textvariable=StringVar())
e1.grid(row=0, column=1)
objects.append(e1)

e2 = Entry(window, textvariable=StringVar())
e2.grid(row=0, column=3)
objects.append(e2)

e3 = Entry(window, textvariable=StringVar())
e3.grid(row=0, column=5)
objects.append(e3)

e5 = Entry(window, textvariable=StringVar())
e5.grid(row=1, column=3)
objects.append(e5)

e6 = Entry(window, textvariable=StringVar())
e6.grid(row=1, column=5)
objects.append(e6)

## =====================================

list1 = Listbox(window, height=8, width=35)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)
objects.append(list1)

## =====================================
scr = Scrollbar(window)
scr.grid(row=2, column=2, rowspan=6, )
objects.append(scr)

list1.configure(yscrollcommand=scr.set)
scr.configure(command=list1.yview)

## =====================================

submit_button = Button(window, text='Add patient', width=12, command=new_patient_window)
submit_button.grid(row=2, column=5)
objects.append(submit_button)

view_patients_button = Button(window, text='View patients', width=12, command=all_patients_view)
view_patients_button.grid(row=3, column=5)
objects.append(view_patients_button)

add_doctor_button = Button(window, text='Add doctor', width=12, command=new_doctor_window)
add_doctor_button.grid(row=4, column=5)
objects.append(add_doctor_button)

view_doctors_button = Button(window, text='View doctors', width=12, command=all_doctors_view)
view_doctors_button.grid(row=5, column=5)
objects.append(view_doctors_button)

add_appo = Button(window, text='New appointment', width=12, command=add_appointment)
add_appo.grid(row=2, column=3)
objects.append(add_appo)

refresh_appo = Button(window, text='Apps', width=12, command=get_appointments_call)
refresh_appo.grid(row=2, column=4)
objects.append(refresh_appo)

delete_patient_button = Button(window, text='Del patient', width=12, command=delete_patient_window)
delete_patient_button.grid(row=2, column=6)
objects.append(delete_patient_button)

#new
delete_doctor_button = Button(window, text='Del doctor', width=12, command=delete_doctor_window)
delete_doctor_button.grid(row=3, column=6)
objects.append(delete_doctor_button)

delete_database_button = Button(window, text='Del database', width=12, command=delete_db1)
delete_database_button.grid(row=4, column=6)
objects.append(delete_database_button)

search_patient_button = Button(window, text='Search patient', width=12, command=search_patient_window)
search_patient_button.grid(row=5, column=6)

searh_app_button = Button(window, text='Search app', width=12, command=search_app_call)
searh_app_button.grid(row=3, column=4)

delete_appo_button = Button(window, text='Delete this', width=12, command=focus_appo)
delete_appo_button.grid(row=4, column=4)


tree = ttk.Treeview(window,
                    columns=('id', 'Patient',
                             'Service', 'Doctor', 'Price', 'Time' ))

tree.heading('#0', text='id')
tree.heading('#1', text='Patient')
tree.heading('#2', text='Service')
tree.heading('#3', text='Doctor')
tree.heading('#4', text='Price')
tree.heading('#5', text='Time')

tree.column('#0', stretch=YES, width=30)
tree.column('#1', stretch=YES, width=150)
tree.column('#2', stretch=YES, width=150)
tree.column('#3', stretch=YES, width=150)
tree.column('#4', stretch=YES, width=90)
tree.column('#5', stretch=YES, width=90)

tree.grid(row=20, columnspan=10,)
treeview = tree


comboExample = ttk.Combobox(window,
                            values=get_docnames_call())

comboExample.grid(row=1, column=1)


# connect()

entry_list = [children for children in window.children.values() if 'entry' in str(children)]
window.mainloop()


"""1) РРґРµРј РІ proc.py Рё СЃРѕР·РґР°РµРј РЅРѕРІСѓСЋ РїСЂРѕС†РµРґСѓСЂСѓ
2) СЃС‚РѕРёС‚ РїСЂРѕРІРµСЂРёС‚СЊ РµС‘ СЂР°Р±РѕС‚Сѓ С‡РµСЂРµР· bash (select * func_name(...) )
3) РЎРѕР·РґР°С‘Рј РІ calls.py РІС‹Р·РѕРІ СЌС‚РѕР№ С„СѓРЅРєС†РёРё
4) Р”РµР»Р°РµРј РєРЅРѕРїРєСѓ, РєРѕС‚РѕСЂР°СЏ Р±СѓРґРµС‚ РІС‹Р·С‹РІР°С‚СЊ РЅР°С€Сѓ РїСЂРѕС†РµРґСѓСЂСѓ
5) Р•СЃР»Рё РЅСѓР¶РµРЅ РІС‹Р·РѕРІ РЅРѕРІРѕРіРѕ РѕРєРЅР°, С‚Рѕ РґРµР»Р°РµРј def ..._new_window()
6) Р’ СЌС‚РѕРј РЅРѕРІРѕРј РѕРєРЅРµ СЃРѕР·РґР°С‘Рј РєРЅРѕРїРєСѓ, РєРѕС‚РѕСЂР°СЏ СѓР¶Рµ Рё Р±СѓРґРµС‚ РІС‹РїРѕР»РЅСЏС‚СЊ РІС‹Р·РѕРІ С„СѓРЅРєС†РёРё call РёР· С€Р°РіР° 3
7) РІСЃС‘
"""