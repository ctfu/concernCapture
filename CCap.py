from Tkinter import *
import tkFileDialog
import subprocess
import os


def raise_frame(frame):
    frame.tkraise()

root = Tk()
root.title("Concern Capture")
root.geometry("450x250")

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
information = ("Author: Chuntao Fu" + "\n"
            "Supervisor: Dr. Harvey Siy" + "\n\n" +
            "This tool is created to support capturing the essence of concern in source code.")
Label(aboutFrame, text=information, justify=LEFT, wraplength=450).pack()


# docummentation frame
doc = Label(docFrame, text="This is documentation frame").pack()

# covert file frame
def convertFile(event):
    absoluteFileName = tkFileDialog.askopenfilename()
    print absoluteFileName;
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
    outFileName = "combined_" + relFileName[relFileName.index('_')+1:relFileName.index('.')]
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

combineFileChooser_label = Label(fileCombineFrame, text="Concatenate Files:", padx=50, pady=10).pack(side=LEFT)
combineFileChooser_button = Button(fileCombineFrame, text="Choose Files")
combineFileChooser_button.bind("<Button-1>", combineFiles)
combineFileChooser_button.pack(side=LEFT)

# call graph frame
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


Label(callGraphFrame, text="Call Graph Generation").pack()
genCallGraphInfo = "Select a graget file (in class1;class2;method format), generate a adjusted directed graph based on the input file. "
Label(callGraphFrame, text=genCallGraphInfo, justify=LEFT, wraplength=450).pack()

genFileChooser_label = Label(callGraphFrame, text="Target File:", pady=10).pack()
genFileChooser_button = Button(callGraphFrame, text="Gen Call Graph")
genFileChooser_button.bind("<Button-1>", genDynamicCallGraph)
genFileChooser_button.pack()

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
    outFile = open("analysis_output.txt", "w")
    result = subprocess.call(freqCommand, stdout=outFile)
    outFile.close()

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

Label(freqFrame, text="Frequency Analysis").pack()
genFreqInfo = "Select multiple files (in class1;class2;method format), generate a class frequency output based on the selected files."
Label(freqFrame, text = genFreqInfo, justify=LEFT, wraplength=450).pack()

subFrame = Frame(freqFrame)
subFrame.pack(side=BOTTOM)
calFreq_label = Label(subFrame, text="Calculate Frequency:")
calFreq_button = Button(subFrame, text="Choose Files")
freqGraph_label = Label(subFrame, text="Frequency Graph:")
freqGraph_button = Button(subFrame, text="Choose File")
calFreq_label.grid(row=0, sticky=E)
calFreq_button.bind("<Button-1>", calFrequency)
calFreq_button.grid(row=0, column=1)
freqGraph_label.grid(row=1, sticky=E)
freqGraph_button.bind("<Button-1>", genFreqCallGraph)
freqGraph_button.grid(row=1, column=1)

# LDA/LSI frame
ir = Label(irFrame, text="This is information retrieval frame").pack()

raise_frame(mainFrame)
root.mainloop()
