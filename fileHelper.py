import os,shutil,math,json
from docx2pdf import convert
from PyPDF2 import PdfFileReader, PdfFileWriter

def getConfig():
        with open("./config.json") as json_data_file:
            config = json.load(json_data_file)
        missingData = []
        for key in config:
            if len(config[key].split())== 0:
                missingData.append(key)
        if len(missingData)!=0:
            print("[ERROR] Values for the following keys are missing from config \n {0}".format(missingData))
            exit(1)
        return config

def docxToPdf(inDir,file):
    convertDir = inDir+"/converted"
    if not os.path.exists(convertDir):
        os.makedirs(convertDir)
    opFileName = file.split(".")[0]+".pdf"
    convert(os.path.join(inDir, file), os.path.join(convertDir, opFileName))
    return os.path.join(convertDir, opFileName)

def splitPdf(inFile,opDir,maxFileSize):
    fileSize = os.path.getsize(inFile)
    if not os.path.exists(opDir):
        os.makedirs(opDir)
    if fileSize <= int(maxFileSize) :
        print("[Processing Files] {0} is ok".format(inFile))
        shutil.copy(inFile,os.path.join(opDir,inFile.split("/")[-1]))
    else:
        numOfSubFiles = math.ceil(fileSize / int(maxFileSize))
        print("[Processing Files] {0} is not ok, splitting it into {1} files".format(inFile,numOfSubFiles))
        with open(inFile, 'rb') as infile:
             reader = PdfFileReader(infile)
             numOfPages = reader.getNumPages()
             pagesPerFile = numOfPages / numOfSubFiles
             pagesLeft = numOfPages % numOfSubFiles
             for filenum in range(numOfSubFiles):
                writer = PdfFileWriter()
                for page in range(int(filenum*pagesPerFile),int((filenum*pagesPerFile)+pagesPerFile)):
                    writer.addPage(reader.getPage(page))
                    if page == numOfPages-1-pagesLeft :
                         writer.addPage(reader.getPage(page+pagesLeft))
                fileName = os.path.join(opDir,inFile.split("/")[-1].split(".")[0]+"_"+str(filenum)+".pdf")
                with open(fileName, "wb") as outputStream:
                    writer.write(outputStream)
           

def convertDocuments(inDir,opDir,maxFileSize): 
    files=[]
    for file in os.listdir(inDir):
        if file.endswith(".pdf"):
            files.append(os.path.join(inDir, file))
            splitPdf(os.path.join(inDir, file),opDir,maxFileSize)
        if file.endswith(".docx"):
            print("[Processing Files] Converting {0} into pdf".format(file))
            convertedFile = docxToPdf(inDir,file)
            files.append(convertedFile)
            splitPdf(convertedFile,opDir,maxFileSize)

