# -*- coding: utf-8 -*-
import os
import sys
import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import Part
import PartDesign
import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore

class Ui_Dialog(object):
    #print('aaaaaaa')
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 550)
        Dialog.move(1000, 0)

        #水路幅
        self.label_W = QtGui.QLabel('channelWidth',Dialog)
        self.label_W.setGeometry(QtCore.QRect(30, 13, 100, 22))
        self.le_W = QtGui.QLineEdit('4000',Dialog)
        self.le_W.setGeometry(QtCore.QRect(120, 10, 60, 20))
        self.le_W.setAlignment(QtCore.Qt.AlignCenter)
        #水路高
        self.label_H = QtGui.QLabel('channelHeight',Dialog)
        self.label_H.setGeometry(QtCore.QRect(30, 38, 100, 22))
        self.le_H = QtGui.QLineEdit('6000',Dialog)
        self.le_H.setGeometry(QtCore.QRect(120, 35, 60, 20))
        self.le_H.setAlignment(QtCore.Qt.AlignCenter)
        #機長
        self.label_L = QtGui.QLabel('machineLength',Dialog)
        self.label_L.setGeometry(QtCore.QRect(30, 63, 100, 22))
        self.le_L = QtGui.QLineEdit('8915',Dialog)
        self.le_L.setGeometry(QtCore.QRect(120, 60, 60, 20))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter)
        #傾斜角
        #self.label_beta = QtGui.QLabel('tiltAngle',Dialog)
        #self.label_beta.setGeometry(QtCore.QRect(30, 88, 100, 22))
        #self.le_beta = QtGui.QLineEdit(Dialog)
        #self.le_beta.setGeometry(QtCore.QRect(180, 85, 60, 20))
        #self.le_beta.setAlignment(QtCore.Qt.AlignCenter)



        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 145, 50, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(100, 145, 50, 22))
        #Import
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(170, 145, 50, 22))

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 185, 320, 400))
        self.label_6.setText("")
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "sandScraper.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignTop)
        self.label_6.setObjectName("label_6")

        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(190, 15, 150, 23))
        self.pushButton_m.setObjectName("pushButton") 
        #質量集計
        self.pushButton_m20 = QtGui.QPushButton('massTally_csv',Dialog)
        self.pushButton_m20.setGeometry(QtCore.QRect(190, 40, 150, 23))
        self.pushButton_m2 = QtGui.QPushButton('massTally_SpreadSheet',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(190, 65, 150, 23))
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(190, 90, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(290, 90, 50, 20))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(190, 115, 80, 12))
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(290, 115, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')


        
        #self.le_C.setText('5000')
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)

        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally)
        QtCore.QObject.connect(self.pushButton_m20, QtCore.SIGNAL("pressed()"), self.massTally2)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "sandScraper", None))

    def massImput(self):
         # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g=float(self.le_mass.text())
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g
         
    def massCulc(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g0=float(self.le_gr.text())
        g=obj.Shape.Volume*g0*1000/10**9  
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            pass

    def massTally2(self):#csv
        doc = App.ActiveDocument
        objects = doc.Objects
        mass_list = []
        for obj in objects:
            if Gui.ActiveDocument.getObject(obj.Name).Visibility:
                if obj.isDerivedFrom("Part::Feature"):
                    if hasattr(obj, "mass"):
                        try:
                            mass_list.append([obj.Label, obj.dia,'1', obj.mass])
                        except:
                            mass_list.append([obj.Label, '','1', obj.mass])    

                else:
                     pass
        doc_path = doc.FileName
        csv_filename = os.path.splitext(os.path.basename(doc_path))[0] + "_counts_and_masses.csv"
        csv_path = os.path.join(os.path.dirname(doc_path), csv_filename)
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name",'Standard','Count', "Mass[kg]"])
            writer.writerows(mass_list) 
    def massTally(self):#spreadsheet
        doc = App.ActiveDocument
        # 新しいスプレッドシートを作成
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "PartList")
        spreadsheet.Label = "Parts List"
        
        # ヘッダー行を記入
        headers = ['No',"Name",'Standard', 'Count','Unit[kg]','Mass[kg]']
        for header in enumerate(headers):
            spreadsheet.set(f"A{1}", headers[0])
            spreadsheet.set(f"B{1}", headers[1])
            spreadsheet.set(f"C{1}", headers[2])
            spreadsheet.set(f"D{1}", headers[3])
            spreadsheet.set(f"E{1}", headers[4])
            spreadsheet.set(f"F{1}", headers[5])
        # パーツを列挙して情報を書き込む
        row = 2
        i=1
        s=0
        for i,obj in enumerate(doc.Objects):
            if obj.Label=='本体' or obj.Label=='本体 (mirrored)' or obj.Label[:7]=='Channel' or obj.Label[:5]=='Angle' \
                or obj.Label[:6]=='Square' or obj.Label[:7]=='Extrude' or obj.Label[:6]=='Fusion' or obj.Label[:6]=='Corner' \
                    or obj.Label[:5]=='basic' or obj.Label[:4]=='Edge' or obj.Label[:3]=='hub' or obj.Label[:7]=='_8_tube'\
                        or obj.Label[:5]=='plate' or obj.Label[:6]=='keyway' or obj.Label[:4]=='tube'\
                            or obj.Label[:6]=='HShape' or obj.Label[:5]=='color':
                pass        
            else:  
                try:
                    spreadsheet.set(f"E{row}", f"{obj.mass:.2f}")  # Unit
                    s=obj.mass+s
                    if hasattr(obj, "Shape") and obj.Shape.Volume > 0:
                        try:
                            spreadsheet.set(f"A{row}", str(row-1))  # No
                            spreadsheet.set(f"B{row}", obj.Label)   #Name
                            try:
                                spreadsheet.set(f"C{row}", obj.dia)
                            except:
                                #spreadsheet.set(f"C{row}", obj.standard)
                                pass
                            if obj.Label[:7]=='Angular':
                                n=2
                            else:
                                n=1    
                            spreadsheet.set(f"D{row}", str(n))   # count
                            g=round(obj.mass*n,2)
                            spreadsheet.set(f"F{row}", str(g))   # g

                    
                            row += 1
                        except:
                            pass    
                except:
                    pass
                spreadsheet.set(f'F{row}',str(s))
        App.ActiveDocument.recompute()
        Gui.activeDocument().activeView().viewAxometric()    
        
    def setParts(self):
        global shtSandAssy
        global Sketch_m
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label == "shtSandAssy":
                         shtSandAssy = obj
                     elif obj.Label=='Sketch_m':
                         Sketch_m=obj    

                         self.le_W.setText(shtSandAssy.getContents('W0'))  
                         self.le_L.setText(shtSandAssy.getContents('L0'))  
                         self.le_H.setText(shtSandAssy.getContents('H0'))  
                         #self.le_beta.setText(shtSandAssy.getContents('beta'))

                         


        

    def update(self):
         if shtSandAssy is None :
             App.Console.PrintError("select an object\n")
         else:
             L0=self.le_L.text()
             H0=self.le_H.text()
             W0=self.le_W.text()
    
    
             shtSandAssy.set('L0',str(L0))
             shtSandAssy.set('H0',str(H0))
             shtSandAssy.set('W0',str(W0))
    
             total_length = 0.0
             edges = Sketch_m.Geometry  # スケッチ内のジオメトリリスト
             for edge in edges:
               #if isinstance(edge, (Part.Line, Part.LineSegment, Part.Circle, Part.ArcOfCircle, Part.Ellipse, Part.ArcOfEllipse)):  # エッジのみ対象
                if isinstance(edge, (Part.LineSegment, Part.ArcOfCircle )):  # エッジのみ対象 
                   total_length += edge.length()
             
             shtSandAssy.set('pL',str(total_length))
             print(total_length) 
             
             
             App.ActiveDocument.recompute()
        
    
    def create(self): 
         fname='sandScraperAssy00.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, fname) 

         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
         Gui.SendMsgToActiveView("ViewFit")   
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
           