import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from DAO.fillDataDAO import fillData

class fillDataBUS:
     def _init_(self):
          pass
     def getListSymptom(self):
          list = fillData()
          return list.fill_symptom()
     def getTrieuChung(self,tenBenh):
          return fillData.fill_symptom_question(tenBenh)
     def getMa(self,ten):
          return fillData.getMaLuat(ten)
     def getsymptom(self,ten):
          return fillData.getSymptom(ten)
     def getDisease(self,ten):
          return fillData.getDisease(ten)
     def getCauHoi(self,ten):
          return fillData.getCauHoi(ten)
     def getInformation(self,ten):
          return fillData.getInformation(ten)
     def getSymptom_ten(self,ten):
          return fillData.getSymptom_ten(ten)