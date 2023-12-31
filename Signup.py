from ctypes import resize
import sys
import os
import textwrap
from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox

def printtext():
    global entry_1, entry_2, entry_3, entry_8, entry_9
    global string
    ssn = entry_1.get()
    fname = entry_2.get()
    lname = entry_3.get()
    uname = entry_8.get()
    password = entry_9.get()

    entry_1.delete(first=0, last=100)
    entry_2.delete(first=0, last=100)
    entry_3.delete(first=0, last=100)
    entry_8.delete(first=0, last=100)
    entry_9.delete(first=0, last=100)

    string_d = ssn + "|" + fname + "|" + lname
    string_a = uname + "|" + password

    # Check if the given SSN is already present in the file
    with open("hashcontent.txt", "r") as file:
        for line in file:
            existing_ssn = line.split('|')[1]
            if ssn == existing_ssn:
                messagebox.showerror("Error", "SSN already exists!")
                return

    string_a = (''.join(format(ord(x), 'b') for x in string_a))
    hashval = int(hashrec(string_a), 16)

    # Collision resolution
    while check_collision(hashval):
        hashval += 1

    string = '{:08x}'.format(hashval) + "|" + string_d + "\n"
    ahead.write(string)

def check_collision(hashval):
    with open("hashcontent.txt", "r") as file:
        for line in file:
            existing_hash, _, _, _ = line.split('|')
            if hashval == int(existing_hash, 16):
                return True
    return False

def log():
	os.system("python Login.py")
	
def dest():
	ahead.close()
	# shead.close()
	# phead.close()
	root.destroy()


def wordret(wa,wb,wc):
	a=int(wa,2)^int(wb,2)^int(wc,2)
	return '{0:032b}'.format(a)

def F1(S2,S3,S4):
	return (S2&S3)|(~S2&S4)
def F2(S2,S3,S4):
	return S2^S3^S4
def F3(S2,S3,S4):
	return (S2&S3)|(S2&S4)|(S3&S4)
def F4(S2,S3,S4):
	return S2^S3^S4

def process(chunk):
	words=[]
	words=textwrap.wrap(chunk, 32)
	words.append(wordret(words[0],words[1],words[2]))
	return words

def compress(words):
	k1=0x5A827999
	k2=0x6ED9EBA1
	k3=0x8F1BBCDC
	k4=0xCA62C1D6
	s1 = 0x67452301
	s2 = 0xEFCDAB89
	s3 = 0x98BADCFE
	s4 = 0x10325476
	s5 = 0xC3D2E1F0
	h1=s1
	h2=s2
	h3=s3
	h4=s4
	h5=s5
	for i in range(0,3):
		temp=s5+(s1<<5)+F1(s2,s3,s4)+k1+int(words[i],2)
		s5=s4
		s4=s3
		s3=s2
		s2=s1
		s1=temp
	h1 = h1 + s1 & 0xffffffff

	return h1


def hashrec(string):
    length = len(string)
    low = 0
    high = 20
    while length > 20:
        chunk = string[low:high]
        binlength = '{0:064b}'.format(20)
        chunk += binlength
        obj1 = process(chunk)
        length = length - 20
        low = low + 20
        high = high + 20
        obj2 = compress(obj1)

        # Convert the hash to a hexadecimal string
        hashval = '{:08x}'.format(obj2)

        # Check for collisions
        while check_collision(hashval):
            obj2 += 1
            hashval = '{:08x}'.format(obj2)

    if length == 20:
        string += '1'
        length = '{0:064b}'.format(length)
        string += length
        obj1 = process(string)
        obj2 = compress(obj1)

        # Convert the hash to a hexadecimal string
        hashval = '{:08x}'.format(obj2)

        # Check for collisions
        while check_collision(hashval):
            obj2 += 1
            hashval = '{:08x}'.format(obj2)

    elif length < 20:
        string += '1'
        length = len(string)
        for i in range(length, 20):
            string += '0'
        length = '{0:064b}'.format(length)
        string += length
        obj1 = process(string)
        obj2 = compress(obj1)

        # Convert the hash to a hexadecimal string
        hashval = '{:08x}'.format(obj2)

        # Check for collisions
        while check_collision(hashval):
            obj2 += 1
            hashval = '{:08x}'.format(obj2)

    return hashval

ahead = open("hashcontent.txt","a+")
# shead = open("secondary.txt","a+")
# phead = open ("secondaryph.txt","a+")

# MAIN STARTS HERE
root = Tk()
root.geometry('500x900')
root.title("Add GUI")
#root.configure(background='#e9e4e6')
root.configure(background='#b1dee3')
# bg = PhotoImage(file=r".\signuplogo.png")

# label1 = Label(root, image=bg,width=200, height=100)
# label1.place(x=50, y=280)
image = Image.open("signuplogo.png")
resize_image = image.resize((150, 150))
img = ImageTk.PhotoImage(resize_image)
label_img = Label(image=img,background="#b1dee3")
label_img.image = img
label_img.pack()
label_img.place(x=175, y=80)

label_head = Label(root, text="FIR PORTAL",width=15,font=("Tahoma", 40,"bold"),fg ="#152930", background='#b1dee3',justify="center")
label_head.place(x=0,y=5)

label_0 = Label(root, text="SIGN-IN",width=23,font=("Tahoma", 20,"bold"),fg ="#152930", background='#b1dee3',justify="center")
label_0.place(x=50,y=250)

label_1 = Label(root, text="SSN",width=13,font=("Century Gothic", 16,"bold"),fg ="#152930", background='#b1dee3')
label_1.place(x=50,y=320)

entry_1 = Entry(root, width=13,font=("Courier New",17))
entry_1.pack()
entry_1.focus_set()
entry_1.place(x=242,y=320)

label_2 = Label(root, text="First Name",width=13,font=("Century Gothic", 16,"bold"),fg ="#152930", background='#b1dee3')
label_2.place(x=50,y=360)

entry_2 = Entry(root, width=13,font=("Courier New",17))
entry_2.pack()
entry_2.focus_set()
entry_2.place(x=242,y=360)

label_3 = Label(root, text="Last Name",width=13,font=("Century Gothic", 16,"bold"),fg ="#152930", background='#b1dee3')
label_3.place(x=50,y=400)

entry_3 = Entry(root, width=13,font=("Courier New",17))
entry_3.pack()
entry_3.focus_set()
entry_3.place(x=242,y=400)


label_8 = Label(root, text="Username",width=13,font=("Century Gothic", 16,"bold"),fg ="#152930", background='#b1dee3')
label_8.place(x=50,y=460)

entry_8 = Entry(root, width=13,font=("Century Gothic",17))
entry_8.pack()
entry_8.focus_set()
entry_8.place(x=242,y=460)

label_9 = Label(root, text="Password",width=13,font=("Century Gothic", 16,"bold"),fg ="#152930", background='#b1dee3')
label_9.place(x=50,y=510)

entry_9 = Entry(root, width=13,font=("Century Gothic",17),show="*")
entry_9.pack()
entry_9.focus_set()
entry_9.place(x=240,y=510)


b = Button(root, text='Submit',width=13,height=1,bg='#049372',fg='black',background="#89C4F4", command=printtext,font=("Century Gothic", 16,"bold"),activebackground="#00ff00").place(x=146,y=550)
Button(root, text='Login',width=13,height=1,bg='#049372',fg='black',background="#89C4F4", command=log,font=("Century Gothic", 16,"bold"),activebackground="#00ff00").place(x=146,y=600)
Button(root,text='Quit',width=13,height=1,bg='#D24D57',fg='black', command=dest,font=("Century Gothic", 16,"bold"),activebackground="#ff0000").place(x=146, y=650)
root.mainloop()
