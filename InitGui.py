#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************
import inspect
import os
import sys
import FreeCAD
import FreeCADGui

class sandScraperShowCommand:
    def GetResources(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        return { 
          'Pixmap': os.path.join(module_path, "icons", "sandScraper.svg"),
          'MenuText': "sandScraper",
          'ToolTip': "Show/Hide sandScraper"}

    def IsActive(self):
        import sandScraper
        sandScraper
        return True

    def Activated(self):
        try:
          import sandScraper
          sandScraper.main.d.show()
        except Exception as e:
          FreeCAD.Console.PrintError(str(e) + "\n")

    def IsActive(self):
        import sandScraper
        return not FreeCAD.ActiveDocument is None

class sandScraperWB(FreeCADGui.Workbench):
    def __init__(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        self.__class__.Icon = os.path.join(module_path, "icons", "sandScraper.svg")
        self.__class__.MenuText = "sandScraper"
        self.__class__.ToolTip = "sandScraper by Pascal"

    def Initialize(self):
        self.commandList = ["sandScraper_Show"]
        self.appendToolbar("&sandScraper", self.commandList)
        self.appendMenu("&sandScraper", self.commandList)

    def Activated(self):
        import sandScraper
        sandScraper
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
FreeCADGui.addWorkbench(sandScraperWB())
FreeCADGui.addCommand("sandScraper_Show", sandScraperShowCommand())

