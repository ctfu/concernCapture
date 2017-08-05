from Tkinter import *
import tkFileDialog
import subprocess
from tkintertable import TableCanvas, TableModel
import os


def raise_frame(frame):
    frame.tkraise()

root = Tk()
root.title("Concern Capture")
root.geometry("450x380")

# stack fram stack up
frames = []
mainFrame = Frame(root)
aboutFrame = Frame(root)
docFrame = Frame(root)
fileConvertFrame = Frame(root)
fileCombineFrame = Frame(root)
callGraphFrame = Frame(root)
freqFrame = Frame(root)
irFrame = Frame(root)
frames.append(mainFrame)
frames.append(aboutFrame)
frames.append(docFrame)
frames.append(fileConvertFrame)
frames.append(fileCombineFrame)
frames.append(callGraphFrame)
frames.append(freqFrame)
frames.append(irFrame)

for frame in frames:
    frame.grid(row=0, column=0, sticky='news')

# drop-down menu
menu = Menu(root)
root.config(menu=menu)

introMenu = Menu(menu)
menu.add_cascade(label="Concern Capture", menu=introMenu)
introMenu.add_command(label="Generate Trace", command=lambda:raise_frame(mainFrame))
introMenu.add_command(label="About", command=lambda:raise_frame(aboutFrame))
introMenu.add_command(label="Documentation", command=lambda:raise_frame(docFrame))

fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Convert File", command=lambda:raise_frame(fileConvertFrame))
fileMenu.add_command(label="Combine Files", command=lambda:raise_frame(fileCombineFrame))

analysisMenu = Menu(menu)
menu.add_cascade(label="Analysis", menu=analysisMenu)
analysisMenu.add_command(label="Dynamic Call Graph", command=lambda:raise_frame(callGraphFrame))
analysisMenu.add_command(label="Frequency Analysis", command=lambda:raise_frame(freqFrame))
analysisMenu.add_command(label="LDA/LSI", command=lambda:raise_frame(irFrame))

# javashot generate program trace menu
def genCallTrace(event):
    javashotPath = javashotE_entry.get()
    projectPath = projectE_entry.get()
    command = []
    command.append("java")
    command.append("-javaagent:" + javashotPath)
    command.append("-jar")
    command.append(projectPath)
    print(command)
    subprocess.call(command)

javashotP_label = Label(mainFrame, text="Javashot Path:")
projectP_label =  Label(mainFrame, text="Project Path:")
javashotE_entry = Entry(mainFrame, bd = 3)
projectE_entry = Entry(mainFrame, bd=3)
javashotP_label.grid(row=0, sticky=E, padx=(50,0), pady=(50,0))
javashotE_entry.grid(row=0, column=1, pady=(50,0))
projectP_label.grid(row=1, sticky=E, padx=(50,0))
projectE_entry.grid(row=1, column=1)

genTrace_buttion = Button(mainFrame, text="Generate Call Trace")
genTrace_buttion.bind("<Button-1>", genCallTrace)
genTrace_buttion.grid(row=2, column=1)

# about frame
information ="Author: Chuntao Fu\n"\
            "Supervisor: Dr. Harvey Siy\n\n"\
            'I am a graduate student in Computer Science at University of Nebraska at Omaha.'\
            'This tool is created for the support of my thesis "Tool Support in Capturing the Essense of Concern in Source Code".'\
            'The tool allows you either works on dynamic program analysis with Javashot from scratch or perform the analysis with prepared files'\
            'in the right format. It provides functionalities including structural analysis that based on dynamic call graph genertion and'\
            'textual analysis that based on Information Retrieval techniques. It achieves the purpose of providing automatic support for'\
            'minimized related code subset capturing from an given software concern.'
Label(aboutFrame, text=information, justify=LEFT, wraplength=450).pack()


# docummentation frame
doc = Label(docFrame, text="This is documentation frame").pack()

# covert file frame
def convertFile(event):
    absoluteFileName = tkFileDialog.askopenfilename()
    print(absoluteFileName)
    commandLine = 'sed "s/\\\\$/_/g" | sed "s/->/;/g" | sed "s/\[/;/g" | sed "s/\]//g" | grep -v digraph | grep -v "^[}]$"'
    fileNameTokens = absoluteFileName.split("/")
    relFileName = fileNameTokens[len(fileNameTokens)-1]
    outFileName = "converted_" + relFileName[relFileName.index('_')+1:relFileName.index('.')]
    print(outFileName)
    dir_path = "convert/"
    if not os.path.isdir("./" + dir_path):
        os.makedirs("convert/")
    outFile = open(os.path.join(dir_path, outFileName + ".txt"), "w")
    result = subprocess.call('sed "s/\./_/g" ' + absoluteFileName + " | " + commandLine, shell=True,  stdout=outFile)
    print(result)
    outFile.close()

Label(fileConvertFrame, text="File Converstion").pack()
convertFileInfo = "Select a target file (in .dot format), convert it to the format of: (class1;class2;method)."
Label(fileConvertFrame, text=convertFileInfo, justify=LEFT, wraplength=450).pack()

convertFileChooser_label = Label(fileConvertFrame, text="Target File:", pady=10).pack()
convertFileChooser_button = Button(fileConvertFrame, text="Choose File")
convertFileChooser_button.bind("<Button-1>", convertFile)
convertFileChooser_button.pack()

# combine file frame
def combineFiles(event):
    fileNames = tkFileDialog.askopenfilenames()
    fileNameTokens = fileNames[0].split("/")
    relFileName = fileNameTokens[len(fileNameTokens)-1]
    outFileName = "combined_" + "combine" + str(len(fileNames))
    print(outFileName)
    combineCommand = []
    combineCommand.append("cat")
    fileNameList = list(fileNames)
    for f in fileNameList:
        combineCommand.append(f)
    dir_path = "combine/"
    if not os.path.isdir("./" + dir_path):
        os.makedirs("combine/")
    outFile = open(os.path.join(dir_path, outFileName + ".txt"), "w")
    result = subprocess.call(combineCommand, stdout=outFile)
    print(result)
    outFile.close()

Label(fileCombineFrame, text="Concatenate Multiple Files ").pack()
combineFileInfo = "Select multiple files and combine them into a single file."
Label(fileCombineFrame, text=combineFileInfo, justify=LEFT, wraplength=450).pack()

combineFileChooser_label = Label(fileCombineFrame, text="Concatenate Files:", padx=20, pady=30).pack()
combineFileChooser_button = Button(fileCombineFrame, text="Choose Files")
combineFileChooser_button.bind("<Button-1>", combineFiles)
combineFileChooser_button.pack()

# call graph & dominator tree frame
def genDynamicCallGraph(event):
    absoluteFileName = tkFileDialog.askopenfilename()
    print(absoluteFileName)
    fileNameTokens = absoluteFileName.split("/")
    relFileName = fileNameTokens[len(fileNameTokens)-1]
    outFileName = "tracer_" + relFileName[relFileName.index('_')+1:relFileName.index('.')] + ".dot"
    tracerCommand = []
    tracerCommand.append("python")
    tracerCommand.append("./scripts/tracer.py")
    tracerCommand.append(absoluteFileName)
    outFile = open(outFileName, "w")
    result = subprocess.call(tracerCommand, stdout=outFile)
    outFile.close()
    graphCommand = []
    graphCommand.append("dot")
    graphCommand.append("-Tpdf")
    graphCommand.append("-O")
    graphCommand.append(outFileName)
    result = subprocess.call(graphCommand)
    print(result)
    subprocess.call("open " + outFileName + ".pdf", shell=True)

def genDomTree(event):
    absoluteFileName = tkFileDialog.askopenfilename()
    fileNameTokens = absoluteFileName.split("/")
    relFileName = fileNameTokens[len(fileNameTokens)-1]
    outFileName = "tracerDom_" + relFileName[relFileName.index('_')+1:relFileName.index('.')] + ".dot"
    tracerDomCommand = []
    tracerDomCommand.append("python")
    tracerDomCommand.append("./scripts/tracerDom.py")
    tracerDomCommand.append(absoluteFileName)
    outFile = open(outFileName, "w")
    result = subprocess.call(tracerDomCommand, stdout=outFile)
    outFile.close()
    graphCommand = []
    graphCommand.append("dot")
    graphCommand.append("-Tpdf")
    graphCommand.append("-O")
    graphCommand.append(outFileName)
    result = subprocess.call(graphCommand)
    print(result)
    subprocess.call("open " + outFileName + ".pdf", shell=True)

Label(callGraphFrame, text="Call Graph Generation").pack()
genCallGraphInfo = "Select a graget file (in class1;class2;method format), generate a adjusted directed graph based on the input file. "
Label(callGraphFrame, text=genCallGraphInfo, justify=LEFT, wraplength=450).pack()

genFileChooser_label = Label(callGraphFrame, text="Target File:", pady=10).pack()
genFileChooser_button = Button(callGraphFrame, text="Gen Call Graph")
genFileChooser_button.bind("<Button-1>", genDynamicCallGraph)
genFileChooser_button.pack()

domTreeFileChooser_button = Button(callGraphFrame, text="Gen Dominator Tree")
domTreeFileChooser_button.bind("<Button-1>", genDomTree)
domTreeFileChooser_button.pack();

# Frequency analysis frame
# 1. combine all files in one execution senerio into one single file
# 2. calculate the frequency distrubution over mutilple execution scenarios
def calFrequency(event):
    files = tkFileDialog.askopenfilenames()
    fileList = list(files)
    print(fileList)
    freqCommand = []
    freqCommand.append("python")
    freqCommand.append("./scripts/frequency.py")
    for f in fileList:
        freqCommand.append(f)
    outFile = open("frequency_output.txt", "w")
    result = subprocess.call(freqCommand, stdout=outFile)
    outFile.close()

# open a new window to view the frequency output
def viewFreqOutput(event):
    top = Toplevel()
    analysis = {}
    f = open("frequency_output.txt")
    for line in f:
        record = {}
        tokens = line.rstrip('\n').split(' ')
        if tokens[0] not in analysis:
            record["Label"] = tokens[0]
            record["Frequency"] = tokens[1]
            analysis[tokens[0]] = record
    # print(analysis)
    model = TableModel()
    model.importDict(analysis)
    table = TableCanvas(top, model=model)
    table.createTableFrame()
    top.mainloop()

# generate frequency colored graph based on the frequency analysis output for one execution scenario
def genFreqCallGraph(event):
    absoluteFileName = tkFileDialog.askopenfilename()
    print(absoluteFileName)
    fileNameTokens = absoluteFileName.split("/")
    relFileName = fileNameTokens[len(fileNameTokens)-1]
    outFileName = "tracerFreq_" + relFileName[relFileName.index('_')+1:relFileName.index('.')] + ".dot"
    tracerCommand = []
    tracerCommand.append("python")
    tracerCommand.append("./scripts/tracerFreq.py")
    tracerCommand.append(absoluteFileName)
    outFile = open(outFileName, "w")
    result = subprocess.call(tracerCommand, stdout=outFile)
    outFile.close()
    graphCommand = []
    graphCommand.append("dot")
    graphCommand.append("-Tpdf")
    graphCommand.append("-O")
    graphCommand.append(outFileName)
    result = subprocess.call(graphCommand)
    print(result)
    subprocess.call("open " + outFileName + ".pdf", shell=True)

def genFreqDomTree(event):
    absoluteFileName = tkFileDialog.askopenfilename()
    fileNameTokens = absoluteFileName.split("/")
    relFileName = fileNameTokens[len(fileNameTokens)-1]
    outFileName = "tracerDomFreq_" + relFileName[relFileName.index('_')+1:relFileName.index('.')] + ".dot"
    tracerDomCommand = []
    tracerDomCommand.append("python")
    tracerDomCommand.append("./scripts/tracerDomFreq.py")
    tracerDomCommand.append(absoluteFileName)
    outFile = open(outFileName, "w")
    result = subprocess.call(tracerDomCommand, stdout=outFile)
    outFile.close()
    graphCommand = []
    graphCommand.append("dot")
    graphCommand.append("-Tpdf")
    graphCommand.append("-O")
    graphCommand.append(outFileName)
    result = subprocess.call(graphCommand)
    print(result)
    subprocess.call("open " + outFileName + ".pdf", shell=True)

Label(freqFrame, text="Frequency Analysis").pack()
genFreqInfo = "Select multiple files (in class1;class2;method format), generate a class frequency output based on the selected files."
Label(freqFrame, text = genFreqInfo, justify=LEFT, wraplength=450).pack()

subFrame = Frame(freqFrame)
subFrame.pack()
calFreq_label = Label(subFrame, text="Calculate Frequency:")
calFreq_button = Button(subFrame, text="Choose Files")
freqOutput_label = Label(subFrame, text="View Frequency Output:")
freqOutput_button = Button(subFrame, text="View Output")
freqGraph_label = Label(subFrame, text="Frequency Call Graph:")
freqGraph_button = Button(subFrame, text="Choose File")
freqDomTree_label = Label(subFrame, text="Frequency Dome Tree:")
freqDomTree_button = Button(subFrame, text="Choose File")
calFreq_label.grid(row=0, sticky=E, pady=(30, 0))
calFreq_button.bind("<Button-1>", calFrequency)
calFreq_button.grid(row=0, column=1, pady=(30, 0))
freqOutput_label.grid(row=1, sticky=E)
freqOutput_button.bind("<Button-1>", viewFreqOutput)
freqOutput_button.grid(row=1, column=1)
freqGraph_label.grid(row=2, sticky=E)
freqGraph_button.bind("<Button-1>", genFreqCallGraph)
freqGraph_button.grid(row=2, column=1)
freqDomTree_label.grid(row=3, sticky=E)
freqDomTree_button.bind("<Button-1>", genFreqDomTree)
freqDomTree_button.grid(row=3, column=1)

# LDA/LSI frame
def getAnalysisType():
    global analysisType
    print(str(var.get()))
    if str(var.get()) == "1":
        analysisType = "LDA"
        ldaTopic_entry.config(state="normal")
        ldaTopicWord_entry.config(state="normal")
        ldaDecay_entry.config(state="normal")
        ldaPasses_entry.config(state="normal")
        ldaIteration_entry.config(state="normal")
        lsiTopic_entry.delete(0, END)
        lsiDecay_entry.delete(0, END)
        lsiIteration_entry.delete(0, END)
        lsiQuery_Entry.delete(0, END)
        lsiTopic_entry.config(state="disabled")
        lsiOnePass_checkbox.config(state="disabled")
        lsiDecay_entry.config(state="disabled")
        lsiIteration_entry.config(state="disabled")
        lsiQuery_Entry.config(state="disabled")

    else:
        analysisType = "LSI"
        ldaTopic_entry.delete(0, END)
        ldaTopicWord_entry.delete(0, END)
        ldaDecay_entry.delete(0, END)
        ldaPasses_entry.delete(0, END)
        ldaIteration_entry.delete(0, END)
        ldaTopic_entry.config(state="disabled")
        ldaTopicWord_entry.config(state="disabled")
        ldaDecay_entry.config(state="disabled")
        ldaPasses_entry.config(state="disabled")
        ldaIteration_entry.config(state="disabled")
        lsiTopic_entry.config(state="normal")
        lsiOnePass_checkbox.config(state="normal")
        lsiDecay_entry.config(state="normal")
        lsiQuery_Entry.config(state="normal")
    print(analysisType)

def getLSIPassStatus():
    global lsiOnePass
    if str(var1.get()) == "1":
        lsiOnePass = "False"
        lsiIteration_entry.config(state="normal")
    else:
        lsiOnePass = "True"
        lsiIteration_entry.config(state="disabled")

def populateData(type):
    top = Toplevel()
    analysis = {}
    if type == "LDA":
        with open("./analysis/LDA_output.txt") as f:
            next(f)
            index = 0
            for line in f:
                tokens = line.rstrip('\n').split(':')
                topicWords = tokens[1].split('+')
                print(topicWords)
                for w in topicWords:
                    record = {}
                    tw = w.split('*')
                    record["Topic ID"] = tokens[0]
                    record["Probability"] = tw[0]
                    word = tw[1].replace('"', '').replace('"', '')
                    record["Word"] = word
                    analysis[index] = record
                    index = index + 1
    else:
        with open("./analysis/LSI_output.txt") as f:
            next(f)
            index = 0
            for line in f:
                record = {}
                tokens = line.rstrip('\n').split(':')
                record["Document Name"] = tokens[0]
                record["Document ID"] = tokens[1]
                record["Probability"] = tokens[2]
                analysis[index] = record
                index = index + 1
    model = TableModel()
    model.importDict(analysis)
    table = TableCanvas(top, model=model)
    table.createTableFrame()
    top.mainloop()

def irAnalysis(evnet):
    absoluteFileName = tkFileDialog.askopenfilename()
    print(absoluteFileName)
    analysisCommand = []
    analysisCommand.append("python3")
    analysisCommand.append("./scripts/ir.py")
    analysisCommand.append(absoluteFileName)
    analysisCommand.append(analysisType)
    topicNumber = "0"
    if analysisType == "LDA":
        topicNumber = ldaTopic_entry.get()
        topicWords = ldaTopicWord_entry.get()
        ldaDecay = "0.5"
        ldaPass = "1"
        ldaIteration = "50"
        if len(ldaDecay_entry.get()) != 0:
            ldaDecay = ldaDecay_entry.get()
        if len(ldaPasses_entry.get()) != 0:
            ldaPass = ldaPasses_entry.get()
        if len(ldaIteration_entry.get()) != 0:
            ldaIteration = ldaIteration_entry.get()
        analysisCommand.append(topicNumber)
        analysisCommand.append(topicWords)
        analysisCommand.append(ldaDecay)
        analysisCommand.append(ldaPass)
        analysisCommand.append(ldaIteration)
    else:
        topicNumber = lsiTopic_entry.get()
        lsiDecay = "1.0"
        lsiIteration = "2"
        if len(lsiDecay_entry.get()) != 0:
            lsiDecay = lsiDecay_entry.get()
        if lsiOnePass == "False":
            if len(lsiIteration_entry.get()) != 0:
                lsiIteration = lsiIteration_entry.get()
        lsiQuery = lsiQuery_Entry.get()
        analysisCommand.append(topicNumber)
        analysisCommand.append(lsiOnePass)
        analysisCommand.append(lsiDecay)
        analysisCommand.append(lsiIteration)
        analysisCommand.append(lsiQuery)
    dir_path = "analysis/"
    if not os.path.isdir("./" + dir_path):
        os.makedirs("analysis/")
    outFile = open(os.path.join(dir_path, analysisType + "_output" + ".txt"), "w")
    result = subprocess.call(analysisCommand, stdout=outFile)
    print(result)
    populateData(analysisType)
    outFile.close()


var = IntVar()
var1 = IntVar()
analysisType = "LDA"
lsiOnePass = "True"
irTypeFrame = Frame(irFrame)
irTypeFrame.pack()
Label(irTypeFrame, text="LDA / LSI Analysis").pack()
irType_label = Label(irTypeFrame, text="Type of analysis:")
irType_label.pack(side=LEFT)
irType_radio1 = Radiobutton(irTypeFrame, text="LDA", variable=var, value=1, command=getAnalysisType)
irType_radio1.pack(side=LEFT)
irType_radio2 = Radiobutton(irTypeFrame, text="LSI", variable=var, value=2, command=getAnalysisType)
irType_radio2.pack()

irSubframe = Frame(irFrame)
irSubframe.pack(side=BOTTOM)
ldaType_label = Label(irSubframe, text="For LDA:")
ldaTopic_label = Label(irSubframe, text="Topic Numbers:")
ldaTopic_entry = Entry(irSubframe, bd=2)
ldaTopicWord_label = Label(irSubframe, text="Topic Words:")
ldaTopicWord_entry = Entry(irSubframe, bd=2)
ldaDecay_label = Label(irSubframe, text="Decay(0-1)")
ldaDecay_entry = Entry(irSubframe, bd = 2)
ldaDecay_entry.insert(END, "0.5")
ldaDecay_entry.config(state="disabled")
ldaPasses_label = Label(irSubframe, text="Pass Numbers")
ldaPasses_entry = Entry(irSubframe, bd = 2)
ldaPasses_entry.insert(END, "1")
ldaPasses_entry.config(state="disabled")
ldaIteration_label = Label(irSubframe, text="Iteration Numbers")
ldaIteration_entry = Entry(irSubframe, bd = 2)
ldaIteration_entry.insert(END, "50")
ldaIteration_entry.config(state="disabled")
ldaType_label.grid(row=0, column=0)
ldaTopic_label.grid(row=1, sticky=E)
ldaTopic_entry.grid(row=1, column=1)
ldaTopicWord_label.grid(row=2, sticky=E)
ldaTopicWord_entry.grid(row=2, column=1)
ldaDecay_label.grid(row=3, sticky=E)
ldaDecay_entry.grid(row=3, column=1)
ldaPasses_label.grid(row=4, sticky=E)
ldaPasses_entry.grid(row=4, column=1)
ldaIteration_label.grid(row=5, sticky=E)
ldaIteration_entry.grid(row=5, column=1)
lsiType_label = Label(irSubframe, text="For LSI:")
lsiOnePass_checkbox = Checkbutton(irSubframe, text="Multi-Pass", variable=var1, onvalue=1, offvalue = 0, command=getLSIPassStatus)
lsiTopic_label = Label(irSubframe, text="Topic Numbers:")
lsiTopic_entry = Entry(irSubframe, bd=2)
lsiDecay_label = Label(irSubframe, text="Decay(0-1)")
lsiDecay_entry = Entry(irSubframe, bd = 2)
lsiDecay_entry.insert(END, "1.0")
lsiDecay_entry.config(state="disabled")
lsiIteration_label = Label(irSubframe, text="Power Iteration")
lsiIteration_entry = Entry(irSubframe, bd = 2)
lsiIteration_entry.insert(END, "2")
lsiIteration_entry.config(state="disabled")
lsiIteration_entry.config(state="disabled")
lsiQuery_label = Label(irSubframe, text="Search Query:")
lsiQuery_Entry = Entry(irSubframe, bd=2)
lsiType_label.grid(row=6, column=0)
lsiOnePass_checkbox.grid(row=6, column=1)
lsiTopic_label.grid(row=7, sticky=E)
lsiTopic_entry.grid(row=7, column=1)
lsiDecay_label.grid(row=8, sticky=E)
lsiDecay_entry.grid(row=8, column=1)
lsiIteration_label.grid(row=9, sticky=E)
lsiIteration_entry.grid(row=9, column=1)
lsiQuery_label.grid(row=10, sticky=E)
lsiQuery_Entry.grid(row=10, column=1)
irAnalysis_button =Button(irSubframe, text="Start Analysis")
irAnalysis_button.bind("<Button-1>", irAnalysis)
irAnalysis_button.grid(row=11, column=1)


raise_frame(mainFrame)
root.mainloop()
