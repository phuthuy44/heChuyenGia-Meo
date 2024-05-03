import sys
import os
import mysql
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from DAO.connectDB import mydb
class fillData:
     def _init_(self):
          pass
     def fill_symptom(self):
          list = []
          try:
               query = mydb.cursor()
               sql ="SELECT DISTINCT s.Name_symptom from symptom AS s  left join symptom_and_disaese AS a  ON s.uniqueID = a.symptom_ID  order BY a.reliability_coefficients DESC"
               query.execute(sql)
               rows= query.fetchall()
               for row in rows:
                    disease=row[0]
                    list.append(disease)
               print(list)
          except mysql.connector.errors.InternalError as e:
               print("Error executing MySQL query:", e)
          finally:
               query.close()
               # mydb.close()
          return list
     def fill_symptom_question(tenTrieuChung):
          result_set=[]
          sql= "SELECT * from symptom where name_symptom = %s"
          val=(tenTrieuChung,)
          try:
               query = mydb.cursor()
               query.execute(sql,val)
               result_set = query.fetchall()
               print(result_set)
          except mysql.connector.errors.InternalError as e:
               print("Error executing MySQL query:", e)
          finally:
               query.close()
          return result_set
     def getMaLuat(ten):
          sql = "SELECT DISTINCT disease_ID FROM symptom_and_disaese WHERE symptom_ID = %s"
          val = (ten,)
          try:
               query = mydb.cursor()
               query.execute(sql, val)
               results = query.fetchall()
               print(sql, val)
               mydb.commit()
               return [result[0] for result in results] if results else []
          except mysql.connector.errors.InternalError as e:
               print("Error executing MySQL query:", e)
          finally:
               query.close()
          return []
     def getSymptom(ten):
          sql = "SELECT symptom_ID, reliability_coefficients FROM symptom_and_disaese WHERE disease_ID = %s"
          val = (ten,)
          try:
               query = mydb.cursor()
               query.execute(sql, val)
               results = query.fetchall()
               print(sql, val)
               mydb.commit()
               return results
          except mysql.connector.errors.InternalError as e:
               print("Error executing MySQL query:", e)
          finally:
               query.close()
          return []
     def getDisease(ten):
          sql = "SELECT * FROM disease WHERE uniqueID = %s"
          val = (ten,)
          try:
               query = mydb.cursor()
               query.execute(sql, val)
               results = query.fetchall()
               print(sql, val)
               mydb.commit()
               return results
          except mysql.connector.errors.InternalError as e:
               print("Error executing MySQL query:", e)
          finally:
               query.close()
          return []
     def getCauHoi(cauhoi):
          sql = "SELECT question FROM symptom WHERE uniqueID = %s"
          val = (cauhoi,)
          try:
               query = mydb.cursor()
               query.execute(sql, val)
               results = query.fetchall()
               print(sql, val)
               mydb.commit()
               return [result[0] for result in results] if results else []
          except mysql.connector.errors.InternalError as e:
               print("Error executing MySQL query:", e)
          finally:
               query.close()
          return []
     def getInformation(ten):
          list=[]
          sql= "SELECT * from information_disease WHERE disease_ID = %s"
          val=(ten,)
          try:
               query = mydb.cursor()
               query.execute(sql,val)
               rows= query.fetchall()
               for row in rows:
                    disease=(row[0],row[1],row[2],row[3],row[4])
                    list.append(disease)
               print(list)
          except mysql.connector.errors.InternalError as e:
               print("Error executing MySQL query:", e)
          finally:
               query.close()
          return list
     def getSymptom_ten(ten):
          list=[]
          sql= "SELECT DISTINCT s.Name_symptom, d.reliability_coefficients FROM symptom AS s LEFT JOIN symptom_and_disaese AS d ON s.uniqueID = d.symptom_ID WHERE d.disease_ID = %s"
          val=(ten,)
          try:
               query = mydb.cursor()
               query.execute(sql,val)
               rows= query.fetchall()
               for row in rows:
                    disease=(row[0],row[1])
                    list.append(disease)
               print(list)
          except mysql.connector.errors.InternalError as e:
               print("Error executing MySQL query:", e)
          finally:
               query.close()
          return list
