#!/usr/bin/python3

"""
This module provides a GUI for testing different feature and algorithm combinations.
"""

from tkinter import *
from src import classifyHelp, classify, buildConfusionMatrix


# ========================
# Classes
# ========================

class Checkbar(Frame):
    """ Create multiple checkboxes """

    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        """
        Initialize Checkbar object
        :param parent: The parent window
        :param picks: The checkboxes that will be included
        :param side: Alignment of the checkboxes
        :param anchor: I don't know what that means
        """
        Frame.__init__(self, parent)
        self.vars = []
        # generate checkbox list
        for pick in picks:
            var = IntVar(value=1)  # value=1 means that all checkboxees are selected by default
            chk = Checkbutton(self, text=pick, variable=var, font=('Verdana', 12))
            chk.pack(side=side, anchor=anchor, expand=YES)  # place checkboxes in window
            self.vars.append(var)

    def state(self):
        """
        Show selected checkboxes as string
        :return: Selected checkboxes as string
        """
        return map((lambda var: var.get()), self.vars)


class Radiobar(Frame):
    """ Create multiple radiobuttons """

    @staticmethod
    def show_knn_entry(knn_settings_frame, svm_settings_frame):
        """
        Show only the kNN settings frame
        :param knn_settings_frame: kNN settings frame
        :param svm_settings_frame: SVM settings frame
        """
        knn_settings_frame.pack(side=TOP)
        svm_settings_frame.pack_forget()

    @staticmethod
    def show_svm_entry(knn_settings_frame, svm_settings_frame):
        """
        Show only the SVM settings frame
        :param knn_settings_frame: kNN settings frame
        :param svm_settings_frame: SVM settings frame
        """
        knn_settings_frame.pack_forget()
        svm_settings_frame.pack(side=TOP)

    @staticmethod
    def hide_entry(knn_settings_frame, svm_settings_frame, entries):
        """
        Hide both the kNN and SVM settings frame
        :param knn_settings_frame: kNN settings frame
        :param svm_settings_frame: SVM settings frame
        :param entries: List of settings to hide
        """
        if 'knn' in entries:
            knn_settings_frame.pack_forget()
        if 'svm' in entries:
            svm_settings_frame.pack_forget()

    def __init__(self, knn_settings_frame, svm_settings_frame, parent=None, picks=[]):
        """
        Initialze Radiobar object
        :param knn_settings_frame: kNN settings frame
        :param svm_settings_frame: SVM settings frame
        :param parent: Parent window
        :param picks: The radiobuttons that will be included
        """
        Frame.__init__(self, parent)
        self.vars = []
        var = IntVar()

        for i in range(len(picks)):
            if i == 0:  # True for the kNN radiobutton
                rdbutton = Radiobutton(main_frame, text=picks[i], variable=var, value=i,
                                       command=lambda: self.show_knn_entry(knn_settings_frame, svm_settings_frame),
                                       font=('Verdana', 12))
            elif i == 1:  # True for the SVM radiobutton
                rdbutton = Radiobutton(main_frame, text=picks[i], variable=var, value=i,
                                       command=lambda: self.show_svm_entry(knn_settings_frame, svm_settings_frame),
                                       font=('Verdana', 12))
            else:  # every other radiobutton
                rdbutton = Radiobutton(main_frame, text=picks[i], variable=var, value=i,
                                       command=lambda: self.hide_entry(knn_settings_frame, svm_settings_frame, ['knn', 'svm']),
                                       font=('Verdana', 12))
            rdbutton.pack(side=TOP)
            self.vars.append(var)

    def state(self):
        """
        Show selected radiobuttons as string
        :return: Selected radiobuttons as string
        """
        return map((lambda var: var.get()), self.vars)


class Message:
    """ Show a message in the GUI """

    def __init__(self):
        """
        Initialize Message object
        """
        msg_text.set("")

    @staticmethod
    def set(text):
        """
        Set message text
        :param text: Text for the Message
        :return: Message text
        """
        msg_text.set(text)


# ========================
# Main
# ========================

if __name__ == '__main__':
    root = Tk(className="praxis DH")  # create root window
    root.geometry("700x500-100+100")  # set dimensions for root window

    # create different frames
    main_frame = Frame(root, relief=RAISED, borderwidth=1)
    knn_settings_frame = Frame(main_frame, relief=FLAT, borderwidth=1)
    svm_settings_frame = Frame(main_frame, relief=FLAT, borderwidth=1)

    # create Checkbar for feature selection
    lbl_ft = Label(main_frame, text="Select the features", font=('Verdana', 14))
    lbl_ft.pack(side=TOP, pady=20)
    ft = Checkbar(main_frame, ['Faces', 'Objects', 'RGB', 'HSV', 'Gray'])
    ft.config(relief=FLAT, bd=2)
    ft.pack(side=TOP)

    # create Radiobar for algorithm selection
    lbl_alg = Label(main_frame, text="Choose an Algorithm", font=('Verdana', 14))
    lbl_alg.pack(side=TOP, pady=20)
    alg = Radiobar(knn_settings_frame, svm_settings_frame, parent=main_frame, picks=['kNN', 'SVM', 'C4.5 (Decision Tree)'])
    alg.config(relief=FLAT, bd=2)
    alg.pack(side=TOP)

    # create frame for test set size
    test_set_size_frame = Frame(main_frame, relief=FLAT, borderwidth=1)
    lbl_ts = Label(test_set_size_frame, text="Size of test set? (max. 6500) ", font=('Verdana', 14))
    lbl_ts.pack(side=LEFT, pady=20)
    testset = Entry(test_set_size_frame, font=('Verdana', 14))
    testset.insert(0, '6500')  # default value
    testset.pack(side=RIGHT)
    test_set_size_frame.pack(side=TOP)

    # put frames in main frame
    main_frame.pack(fill=BOTH, expand=True)

    # create frame for messages
    msg_text = StringVar()
    msg = Message()
    message = Label(main_frame, textvariable=msg_text, font=('Verdana', 14, 'italic'))
    message.pack(side=TOP)

    # create frame for kNN settings
    lbl_n = Label(knn_settings_frame, text="How many Neighbours? ", font=('Verdana', 14))
    lbl_n.pack(side=LEFT, pady=20)
    neighbours = Entry(knn_settings_frame, font=('Verdana', 14))
    neighbours.insert(0, '3')  # default value
    neighbours.pack(side=RIGHT)

    # create frame for SVM settings
    lbl_svm = Label(svm_settings_frame, text="Which Kernel? (linear, poly, rbf) ", font=('Verdana', 14))
    lbl_svm.pack(side=LEFT, pady=20)
    kernel = Entry(svm_settings_frame, font=('Verdana', 14))
    kernel.insert(0, 'linear')  # default value
    kernel.pack(side=RIGHT)

    # when starting the application, the kNN settings are shown by default
    knn_settings_frame.pack(side=TOP)

    def handle_selections(msg):
        """
        Process the user selections and invoke classify module
        :param msg: Message object
        """
        feature_selections = list(ft.state())  # list of selected features

        # set feature variables to either True or False
        faces, objects, rgb, hsv, gray = False, False, False, False, False
        if feature_selections[0] == 1:  # if a feature checkbox is selected, set it to True
            faces = True
        if feature_selections[1] == 1:
            objects = True
        if feature_selections[2] == 1:
            rgb = True
        if feature_selections[3] == 1:
            hsv = True
        if feature_selections[4] == 1:
            gray = True

        # show error message if only faces feature was selected
        if faces and not objects and not rgb and not hsv and not gray:
            msg.set("Please select at least one more feature!")

        # get the chosen algorithm
        algorithm = list(alg.state())[0]

        # get entered value for kNN settings
        neighbours_number = neighbours.get()
        if neighbours_number is not '':
            neighbours_number = int(neighbours.get())  # cast input value to integer
        else:
            neighbours_number = None  # if no inout was made

        # get entered value for SVM settings
        kernel_name = kernel.get()
        if kernel_name is not '':
            kernel_name = kernel.get()
        else:
            kernel_name = None  # if no input was made

        # get entered value for test size
        testsize = testset.get()
        if testsize is not '':
            testsize = int(testset.get())  # cast input to integer
        else:
            testsize = None  # if no input was made

        # get entered value for filename
        output_filename = filename_input.get()
        if output_filename is not '':
            output_filename = filename_input.get()
        else:
            output_filename = None  # if no input was made

        # create CSV file that only contains the selected features
        classifyHelp.create_feature_csv(faces, objects, rgb, hsv, gray)
        # classify this CSV file with the chosen algorithm
        classify.main(algorithm, msg, neighbours_number, kernel_name, testsize, output_filename)

    # create start button and input field for filename
    bottom_frame = Frame(root, relief=FLAT, borderwidth=1)
    filename_label = Label(bottom_frame, text="Output Filename: ", font=('Verdana', 14))
    filename_label.pack(side=LEFT, ipady=50)
    filename_input = Entry(bottom_frame, font=('Verdana', 14), width=15)
    filename_input.insert(0, 'docfile')
    filename_input.pack(side=LEFT)
    ext_label = Label(bottom_frame, text=".csv", font=('Verdana', 14))
    ext_label.pack(side=LEFT, ipady=50)
    start_button = Button(bottom_frame, text='Start', command=lambda: handle_selections(msg), width=35, bg='#A9A9A9',
                          font=('Verdana', 14))
    start_button.pack(side=RIGHT, padx=20)
    bottom_frame.pack(side=BOTTOM)

    # start GUI
    root.mainloop()
