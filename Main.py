from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from xml.dom import minidom
from os import environ
from nlp.GUI import Ui_MainWindow
from treetaggerwrapper import TreeTagger

excep = ["integer", "string", "boolean","real","classe"]

# put TreeTagger in C:
environ['TREETAGGER'] = "C:/TreeTagger/TreeTagger"
tagger = TreeTagger(TAGLANG='fr')

integer = "http://argouml.org/profiles/uml14/default-uml14.xmi#-84-17--56-5-43645a83:11466542d86:-8000:000000000000087C"
real = "http://argouml.org/profiles/uml14/default-uml14.xmi#-84-17--56-5-43645a83:11466542d86:-8000:000000000000087D"
string = "http://argouml.org/profiles/uml14/default-uml14.xmi#-84-17--56-5-43645a83:11466542d86:-8000:000000000000087E"
boolean = "http://argouml.org/profiles/uml14/default-uml14.xmi#-84-17--56-5-43645a83:11466542d86:-8000:0000000000000880"

#colors
inv_color = "#cc7832"
context_color = "#cc7832"
type_color = "#0080ff"
val_color = "#164412"
num_color = ""
class_color = "#a05050"

def colored(text,color="#cc7832",style=""):
    return "<span style=\"color: {};white-space:pre;{}\">{}</span>".format(color,style, text)

def getTagInfo(text):
        result = []
        for tag in tagger.tag_text(text):
            dict = {}
            tag = tag.split("\t")
            dict["word"] = tag[0].lower()
            dict["post"] = tag[1]
            dict["lemma"] = tag[2].lower()
            result.append(dict)
        return result

def getTagLemma(text):
        result= []
        for tag in tagger.tag_text(text):
            result.append(tag.split("\t")[2].lower())
        return result

def getTagWord(text):
        result= []
        for tag in tagger.tag_text(text):
            result.append(tag.split("\t")[0].lower())
        return result

def getTagPost(text):
        result= []
        for tag in tagger.tag_text(text):
            result.append(tag.split("\t")[1])
        return result

def getEqual(text,dictionnaire):
    result = " "
    for key in dictionnaire:
        for word in text.split(" "):
            if word in dictionnaire[key]:
                result += key
    return result.replace("<","&lt;")


def getContrainte(path):
    xmldoc = minidom.parse(path)
    resultat = []
    for element in xmldoc.getElementsByTagName("UML:Class"):
            for a in element.getElementsByTagName("UML:Attribute"):

                    for i in a.getElementsByTagName("UML:Enumeration"):
                        if i.getAttribute('href')==boolean:
                            type = "boolean"
                            resultat.append("<br/>"+colored("Context  : ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'), class_color)+ colored("       inv : ",inv_color,"font-weight: bold;") + a.getAttribute('name') + ' = '+colored("\"True\"",val_color) + "  or  " + a.getAttribute('name') + ' = '+colored("\"False\"",val_color) +'<br/>'+colored("       inv : ",inv_color,"font-weight: bold;") +  a.getAttribute('name') + ".oclIsTypeOf( "+colored(type,type_color)+" ) <br/>")

                    for i in a.getElementsByTagName("UML:DataType"):
                        if i.getAttribute('href') == integer:
                            type = "int"
                            resultat.append(colored("Context  : ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") + a.getAttribute('name') + " >= 0" + " and "  + a.getAttribute('name') + " <= 2147483647" "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;")+ a.getAttribute('name') + ".oclIsTypeOf("+ colored(type,type_color) + ") <br/>")

                        elif i.getAttribute('href') == real:
                            type = "real"
                            resultat.append("<br/>"+colored("Context  : ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name') + " >= 0" + " and " + a.getAttribute('name') + " <= 2147483647 <br/>"+ colored("       inv : ",inv_color,"font-weight: bold;")+ a.getAttribute('name') + ".oclIsTypeOf("+colored(type,type_color)+") <br/>")

                        elif i.getAttribute('href')==boolean:
                            type = "boolean"
                            resultat.append("<br/>"+colored("Context  : ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") + a.getAttribute('name') + "=  "+colored("\"True\"",val_color) +"<br/>"+ " or" + a.getAttribute('name') + "=  "+colored("\"True\"",val_color) +"<br/>")
                            resultat.append("<br/>"+colored("Context  : ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name') + ".oclIsTypeOf("+colored(type,type_color)+") <br/>")

                        elif i.getAttribute("href")== string:
                            type= "String"
                            resultat.append("<br/>"+colored("Context  : ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name') + ".oclIsTypeOf("+ colored(type,type_color) +")<br/>")
    return resultat

def readDatFile(file):

    with open(file,encoding='UTF-8') as f:
        result = {}
        lines = f.read().split('\n')
        for line_num in range(0,len(lines)-1,2):
            result[lines[line_num]] = [i for i in lines[line_num+1].split('|') if i != '']
        return result

def Generator(path,text,dictionnaire):
        dictionnaire = readDatFile(dictionnaire)
        result=[]
        xmldoc = minidom.parse(path)
        for element in xmldoc.getElementsByTagName("UML:Class"):
            if element.getAttribute("name").lower() not in getTagLemma(text):
                continue
            for a in element.getElementsByTagName("UML:Attribute"):
                if a.getAttribute("name").lower() not in getTagLemma(text):
                    continue
                type = a.getElementsByTagName("UML:DataType")[0] if a.getElementsByTagName("UML:DataType") else a.getElementsByTagName("UML:Enumeration")[0]
                if type.getAttribute('href') == integer:
                    type = "int"
                elif type.getAttribute('href') == string:
                    type = "String"
                elif type.getAttribute('href') == real:
                    type = "real"
                elif type.getAttribute('href') == boolean:
                    type = "boolean"
                    if  getEqual(text,dictionnaire) == '=': #si dans la phrase il existe une égalité
                        result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name')+ ' = '+colored("\"True\"",val_color) +"<br/>")
                    else : # si dans la phrase il existe une innégalité
                            result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name') + ' = '+colored("\"False\"",val_color) +"<br/>")
                    result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") + a.getAttribute('name') + ".oclIsTypeOf( "+colored(type,type_color)+" )<br/>")
                for word in getTagInfo(text):

                    if 'NUM' in word["post"]:
                        if getEqual(word["word"],dictionnaire):
                            result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name')+" "+getEqual(text,dictionnaire)+ "<br/>")
                        else:
                            result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color) + "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name')+" "+getEqual(text,dictionnaire)+word["word"]+ "<br/>")
                        result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name') + ".oclIsTypeOf ("+colored(type,type_color)+")<br/>")
                        continue
                    elif word["post"]=='NAM':
                        result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name')+" "+getEqual(text,dictionnaire)+'"'+ str(word["word"]).capitalize()+ '"' +"<br/>")
                        result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name') +".oclIsTypeOf ("+colored(type,type_color)+") <br/>")
                        continue
                    elif word["lemma"] == 'nul':
                        result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name')+""+getEqual(text,dictionnaire)+"<br/>")
                        result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +a.getAttribute('name') + ".oclIsTypeOf ("+colored(colored(type,type_color),type_color)+")<br/>")
                        continue

            if "majeur" in getTagLemma(text):
                result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ") +" âge >= 18<br/>")
                continue
            if "mineur" in getTagLemma(text):
                result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ") +" âge < 18<br/>")
                continue
        if len(result) == 0:
            return "Veuillez reformuler votre phrase !"
        return result

def getContext(path, excep=[]):
        result =[]
        xmldoc = minidom.parse(path)
        for element in xmldoc.getElementsByTagName("UML:Class"):
                if element.getAttribute('name') == '' or element.getAttribute('name') in excep:
                    continue
                result.append("<br/>"+colored("Context     ",context_color,"font-weight: bold;")+colored(element.getAttribute('name'),class_color)+ "<br/>"+colored("       inv : ",inv_color,"font-weight: bold;") +" <br/>" )
        return result

class GenApp(QMainWindow , Ui_MainWindow):
    def __init__(self, parent=None):
        super(GenApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_UI()
        self.handle_Boutons()

    def handle_Boutons(self):
        self.parcourir.clicked.connect(self.Bparcourir)
        self.contraintes.clicked.connect(self.constraints)
        self.pushButton.clicked.connect(self.Bcontrainte)
        self.context.clicked.connect(self.Bcontext)
        self.context.setEnabled(False)

    def handle_UI(self):
        self.setWindowTitle('FRàOCL')
        self.setFixedSize(823 , 553)

    def Bparcourir(self):
        fichier = QFileDialog.getOpenFileUrl(self, caption= 'Choisir un Fichier', directory='.', filter= 'Tous les fichiers(*.xmi)')
        text = str(fichier)
        fr=((text.split(',')[0].replace("(PyQt5.QtCore.QUrl('file:///",'')).strip("')"))
        self.textEdit_3.setText(fr)
        if str(self.textEdit_3)== "":
                    self.context.setEnabled(False)
        else:
                    self.context.setEnabled(True)

    def Bcontrainte(self):
        string = self.textEdit_3.toPlainText()
        resultat = Generator(string,self.NL.toPlainText(),'src/Dictionnaire_fr.txt')
        if isinstance(resultat,str) :
            resultat = colored(resultat,"red")
        bff = "".join(resultat)
        self.OCL.setText(bff)

    def Bcontext(self):
        string2 = self.textEdit_3.toPlainText()
        res = getContext(string2,excep)
        bff = "".join(res)
        self.OCL.setText(bff)

    def constraints(self):
        string = self.textEdit_3.toPlainText()
        resultat = getContrainte(string)
        bff = "".join(resultat)
        self.OCL.setText(bff)

if __name__ == '__main__':

    from sys import argv
    app = QApplication(argv)
    window = GenApp()
    window.show()
    app.exec_()
