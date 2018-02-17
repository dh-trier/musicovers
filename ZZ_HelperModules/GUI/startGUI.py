#!/usr/bin/python3

from tkinter import *
from ZZ_HelperModules.GUI import createCSV, classify


class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var, font=('Verdana', 12))
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


class Radiobar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT):
        Frame.__init__(self, parent)
        self.vars = []
        var = IntVar()
        for i in range(len(picks)):
            chk = Radiobutton(frame, text=picks[i], variable=var, value=i, font=('Verdana', 12))
            chk.pack(side=TOP)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


class Message:
    def __init__(self):
        v.set("Score: ...")

    def set(self, text):
        v.set("Score: " + text)


if __name__ == '__main__':
    root = Tk(className="bliblablub")
    root.geometry("700x500-100+100")

    frame = Frame(root, relief=RAISED, borderwidth=1)

    lbl_ft = Label(frame, text="Select the features\n(Selecting 'Faces' as the only feature will throw an error)", font=('Verdana', 14))
    lbl_ft.pack(side=TOP, pady=20)
    ft = Checkbar(frame, ['Faces', 'Objects', 'RGB', 'HSV', 'Gray'])
    ft.config(relief=FLAT, bd=2)
    ft.pack(side=TOP)

    lbl_alg = Label(frame, text="Choose an Algorithm", font=('Verdana', 14))
    lbl_alg.pack(side=TOP, pady=20)
    alg = Radiobar(frame, ['kNN', 'SVM', 'C4.5 (Decision Tree)'])
    alg.config(relief=FLAT, bd=2)
    alg.pack(side=TOP)

    frame1 = Frame(frame, relief=SOLID, borderwidth=1)
    lbl_n = Label(frame1, text="if kNN: How many Neighbours? ", font=('Verdana', 14))
    lbl_n.pack(side=LEFT, pady=20)
    neighbours = Entry(frame1, font=('Verdana', 14))
    neighbours.pack(side=RIGHT)
    frame1.pack(side=TOP)

    frame2 = Frame(frame, relief=SOLID, borderwidth=1)
    lbl_ts = Label(frame2, text="Size of test set? (max. 6500)" , font=('Verdana', 14))
    lbl_ts.pack(side=LEFT, pady=20)
    testset = Entry(frame2, font=('Verdana', 14))
    testset.pack(side=RIGHT)
    frame2.pack(side=TOP)

    frame.pack(fill=BOTH, expand=True)


    def handle_selections(msg):
        feature_selections = list(ft.state())
        faces, objects, rgb, hsv, gray = False, False, False, False, False
        if feature_selections[0] == 1:
            faces = True
        if feature_selections[1] == 1:
            objects = True
        if feature_selections[2] == 1:
            rgb = True
        if feature_selections[3] == 1:
            hsv = True
        if feature_selections[4] == 1:
            gray = True

        algorithm = list(alg.state())[0]

        neighbours_number = neighbours.get()
        if neighbours_number is not '':
            neighbours_number = int(neighbours.get())
        else:
            neighbours_number = None

        testsize = testset.get()
        if testsize is not '':
            testsize = int(testset.get())
        else:
            testsize = None

        createCSV.mkcsv(faces, objects, rgb, hsv, gray)
        classify.main(algorithm, msg, neighbours_number, testsize)


    v = StringVar()
    msg = Message()

    message = Label(frame, textvariable=v, font=('Verdana', 14, 'italic'))
    message.pack(side=TOP)

    start_button = Button(root, text='Start', command=lambda: handle_selections(msg), width=35, bg='#A9A9A9', font=14)
    start_button.pack(side=BOTTOM)

    root.mainloop()
