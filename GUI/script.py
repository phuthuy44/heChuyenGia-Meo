import decimal
import random
import numpy as np
import sys
import os
import PyQt5
from fuzzywuzzy import fuzz
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from PyQt5 import QtWidgets,uic,QtGui,QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidgetItem,QFrame,QMessageBox,QRadioButton,QHBoxLayout,QGraphicsScene,QGraphicsView
from BUS.fillDataBUS import fillDataBUS
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import skfuzzy as fuzz
import fuzzywuzzy 
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
class Luat:
     def __init__(self, maLuat, tenLuat, suKien):
        self.MaLuat = maLuat
        self.TenLuat = tenLuat
        self.SuKien = suKien
        self.HeSoTinCay = 0
        self.HeSoKhongTinCay = 0
     def __lt__(self, other):
        return self.HeSoTinCay < other.HeSoTinCay
class TrangChu(QtWidgets.QMainWindow):
     def __init__(self):
          super(TrangChu,self).__init__()
          uic.loadUi("GUI/frameTrangChu.ui",self)
          self.allItem =fillDataBUS.getListSymptom(self)
          #Hàm thay thế cho comboBox
          self.hanlding_radio()
          self.disease()
          self.luat = []  # Khởi tạo biến luat ở đây
     def disease(self):
          # Thêm sự kiện textChanged cho QTextEdit
          self.fillDisease_to_plainText()
          # search_Disease(self)
          self.txtSeacrh.textChanged.connect(lambda: self.search_Disease())
          # Thêm sự kiện itemSelectionChanged cho QListWidget
          self.listWidget.itemSelectionChanged.connect(lambda:self.choose_symptom())
          #
          self.btnNext.clicked.connect(self.handling_button_next)
          self.btnStop.clicked.connect(self.handling_stop_)
          self.btnReset.clicked.connect(self.resetForm)
     def resetForm(self):
        # Reset form elements to their initial state
          self.destroy()
          parentWidget = self.parentWidget()
          if parentWidget:
               parentWidget.close()
          trangChu = TrangChu()
          trangChu.show()
          # self.luat = [] 

     def fillDisease_to_plainText(self):
          fillDisease = fillDataBUS.getListSymptom(self)
          self.listWidget.clear()
           # Tạo một mô hình dữ liệu
          for row in fillDisease:
               item = QListWidgetItem(row)
               self.listWidget.addItem(item)
     def search_Disease(self):
          txtSearch = self.txtSeacrh.text().lower()
          self.listWidget.clear()
          if not txtSearch:
               self.fillDisease_to_plainText()
          else:     
               for item in self.allItem:
                    similarity = fuzzywuzzy.fuzz.ratio(txtSearch, item.lower())  # So sánh với triệu chứng đã chuyển đổi thành chữ thường
                    if similarity >= 30:  # Chỉ hiển thị triệu chứng có độ tương đồng >= 30
                         list_item = QListWidgetItem(item)
                         self.listWidget.addItem(list_item)
     def choose_symptom(self):
          # Lấy mục được chọn từ QListWidget
          selected_item = self.listWidget.currentItem()
          # selected_item = selected_item.copy()
          # Hiển thị mục được chọn lên ComboBox
          if selected_item:
               self.comboBox.clear()
               self.comboBox.insertItem(0, selected_item.text())

     def hanlding_radio(self):
          self.radio_Co = QtWidgets.QRadioButton("Có")
          self.radio_Co.setStyleSheet("color: yellow; font: 20px;font-weight:bold")
          self.radio_Co.setChecked(True)
          self.radio_Khong = QtWidgets.QRadioButton("Không")
          self.radio_Khong.setStyleSheet("color: yellow; font: 20px;font-weight:bold")
          self.layout_H= QHBoxLayout()
          self.layout_H.addWidget(self.radio_Co)
          self.layout_H.addWidget(self.radio_Khong)
          self.layout.addLayout(self.layout_H)
          self.radio_Co.setVisible(False)
          self.radio_Khong.setVisible(False)

     def handling_stop_(self):
          self.btnNext.setEnabled(False)
          self.btnStop.setEnabled(False)
          self.radio_Co.setEnabled(False)
          self.radio_Co.setEnabled(False)
          tam = self.luat[0]
          print("tAM:",tam.SuKien)
          data = fillDataBUS.getInformation(self,tam.MaLuat)
          # print("Data:",data[0][2])
          message = ""
          try:
               # print("hello",tam[2])
               for i in self.luat:
                    if tam.HeSoTinCay < i.HeSoTinCay:
                         tam = i
               if 0 <= tam.HeSoTinCay < 0.25:
                    message = "Tôi nghĩ tôi gần như không chắc là của mèo của bạn đã mắc : "
               elif 0.25 <= tam.HeSoTinCay < 0.5:
                    message = "Tôi nghĩ mèo của bạn có thể mắc: "
               elif 0.5 <= tam.HeSoTinCay < 0.75:
                    message = "Tôi nghĩ mèo của bạn rất có thể đã mắc: "
               elif 0.75 <= tam.HeSoTinCay < 0.9:
                    message = "Tôi nghĩ mèo của bạn gần như chắc chắn đã mắc: "
               self.txtResult.setText(message + tam.TenLuat+"\n => Hãy xem thông tin về bệnh này")
               self.textEdit_NguyenNhan.setText(data[0][2])
               self.textEdit_3.setText(data[0][3])
               self.textEdit_4.setText(data[0][4])  
               symtom_ten = fillDataBUS.getSymptom_ten(self,tam.MaLuat)  
               # quality = ctrl.Antecedent(np.arange(0,0.25,0.5,0.75,0.9,1), tam.TenLuat) 
               # quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
               # self.scene = QGraphicsScene()
               # self.view = QGraphicsView(self.scene)
               # self.setCentralWidget(self.graphicsView)
               # Vẽ biểu đồ cho biến đầu vào
               # print
               fig, ax = plt.subplots()
               x = np.linspace(0,1,100)
               y= fuzz.trimf(x, [0, 0.125,0.25])
               y_1= fuzz.trimf(x, [0.125, 0.25,0.5])
               y_2 = fuzz.trimf(x, [0.25,0.5,0.75])
               y_3= fuzz.trimf(x, [0.25, 0.5, 0.75])
               y_4= fuzz.trimf(x, [0.5, 0.75, 1])
               # ax.plot(x,y)
               ax.plot(x, y, label='Không bao giờ xảy ra', color='gray') 
               ax.plot(x, y_1, label='Ít khi xảy ra', color='red')
               ax.plot(x, y_2, label='Không đặc trưng', color='yellow') 
               ax.plot(x, y_3, label='Thường xảy ra', color='blue') 
               ax.plot(x, y_4, label='Chắc chắn xảy ra', color='black')
               
               for i in symtom_ten:
                    random_value = random.uniform(0, 1)
                    # ax.scatter(random_value,i[1], marker='o', color='black')  # Đánh dấu hệ số y
                    # # Vẽ đường thẳng từ điểm đánh dấu xuống trục x
                    # ax.plot([random_value, random_value], [0, i[1]], color='black', linestyle='--', linewidth=0.5)
                    # ax.annotate(i[1], (i[1], random_value), xytext=(5, 5), textcoords='offset points')
                    ax.scatter(i[1],i[1], marker='o', color='black')  # Đánh dấu hệ số y
                    # Vẽ đường thẳng từ điểm đánh dấu xuống trục x
                    ax.plot([i[1], i[1]], [0, i[1]], color='black', linestyle='-', linewidth=1)
                    ax.plot([0, i[1]], [i[1], i[1]], color='black', linestyle='-', linewidth=1)

                    ax.annotate(i[0], (i[1],i[1]), xytext=(2, 2), textcoords='offset points')
                    # ax.fill_between(x, 0.25, y, alpha=1)
               # for name, value in symtom_ten:
               #      ax.scatter(0, value, marker='o', color='black')
                    # ax.annotate(f'{value}', xy=(0, value), xytext=(value, 0.1), arrowprops=dict(facecolor='black', arrowstyle='->'))

               # ax.set_xlabel('Biến Đầu Vào',fontsize=12)
               # ax.set_ylabel('Hệ Số',fontsize=12)
               ax.set_title('Triệu chứng của ' + tam.TenLuat,fontsize=12)
               ax.grid(True)
               ax.legend()
               # Xóa nhãn số trên trục y
               ax.set_yticklabels([])
               # ax.set_ylim([0, 1])
               # plt.show()
               plt.savefig('temp_chart.png')
               # plt.close()  # Đóng đối tượng biểu đồ trước khi xóa tệp ảnh
               # os.remove('temp_chart.png')
               chart_image = QPixmap('temp_chart.png')
               # chart_pixmap = QPixmap.fromImage(chart_image)
               # chart_pixmap.fill(PyQt5.transparent) 
               self.label_3.setPixmap(chart_image)
          except:
               pass
               self.txtResult.setText("Chưa đủ dẫn chứng để kết luận ")

     def handling_button_next(self):
          self.quaTrinhSuyDien={}
          suKien ={}
          if not self.luat and not self.quaTrinhSuyDien:
               if not self.comboBox.currentText():
                    QMessageBox.warning(self, 'Cảnh báo', 'Bạn chưa chọn triệu chứng thường xuất hiện ở mèo của bạn!')
               else:
                    # self.label_2.setVisible(False)
                    self.listWidget.setEnabled(False)
                    self.comboBox.setVisible(False)
                    suKienThoaMan = fillDataBUS.getTrieuChung(self,self.comboBox.currentText())
                    self.quaTrinhSuyDien={suKienThoaMan[0][1]:suKienThoaMan[0][0]}
                    self.txtSuyDien.setPlainText("=> Triệu chứng đầu tiên: " + suKienThoaMan[0][1])
                    #Khởi tạo danh sách các luật
                    #fill danh sách mã bệnh dựa trên mã triệu chứng
                    getMa = fillDataBUS.getMa(self,suKienThoaMan[0][0])
                    # print("Mã triệu chứng :",suKienThoaMan[0][0])
                    #fill danh sách mã triệu chứng tương ứng với hệ số dựa trên mã bệnh
                    # if len(getMa) > 0:
                    #      getMa = getMa[0]
                    # print("Mã:",getMa)
                    for i in getMa:
                         suKienThoaMan = fillDataBUS.getsymptom(self,i)
                         #cac bệnh thoa man dựa trên mã bệnh
                         luatThoaMan = fillDataBUS.getDisease(self,i)
                         print("Luât thõa man:",suKienThoaMan)
                         for i in suKienThoaMan:
                              #Khởi tạo dictionary để lưu trữ các triệu chứng
                              danhSachCauHoi = fillDataBUS.getCauHoi(self,i[0])
                              print("Câu hỏi:",danhSachCauHoi)
                              suKien[float(i[1])]=danhSachCauHoi
                              # suKien[danhSachCauHoi[0].split()[0]] = float(i[1])
                              # print(tuple(danhSachCauHoi[0][:-1]))
                              # print("Test",danhSachCauHoi[0][0])
                         # self.luat.append((luatThoaMan[0][0],luatThoaMan[0][1],suKien))
                         l = Luat(int(luatThoaMan[0][0]), luatThoaMan[0][1], suKien)
                         self.luat.append(l)
                         # print("Luật:",self.luat[0].SuKien.values())
                    for item1 in self.luat:
                         try:
                              key = next(iter(self.quaTrinhSuyDien))
                              heSo = item1.SuKien[key]
                              item1.SuKien.pop(key)
                              item1.HeSoTinCay += heSo
                         except:
                              pass
                    self.luat.sort()
                    self.label_2.setWordWrap(True)
                    print(self.luat[0].SuKien)
                    # print()
                    # self.label_2.setText(str(next(iter(self.luat[0][2].values()))))  # Truy cập vào 'suKien' trong tuple
                    self.label_2.setText(str(next(iter(self.luat[0].SuKien.values()))))
                    self.radio_Co.setVisible(True)
                    self.radio_Khong.setVisible(True)
          else:
               end = True
               selected = "Có" if self.radio_Co.isChecked() else "Không"
               key = self.label_2.text()
               self.quaTrinhSuyDien[key]=selected
               cauHoi = list(self.quaTrinhSuyDien.items())[-1][0]
               traLoi = list(self.quaTrinhSuyDien.items())[-1][1]
               self.txtSuyDien.setPlainText(self.txtSuyDien.toPlainText() + "\n" + "Câu hỏi: " + cauHoi + "   Bạn trả lời: " + traLoi)
               luatHetHieuLuc = []
               for item1 in self.luat:
                    try:
                         heSo = item1.SuKien[key]
                         item1.SuKien.pop(key)
                         if selected == "Có":
                              item1.HeSoTinCay += heSo
                         else:
                              item1.HeSoKhongTinCay += heSo
                         if item1.HeSoTinCay >= 0.9:
                              self.txtResult.config(text=f"Chắc chắn bạn đã mắc {item1.TenLuat}")
                              self.btnNext.config(state="disabled")
                              self.btnStop.config(state="disabled")
                              self.radio_Co.config(state="disabled")
                              self.radio_Khong.config(state="disabled")
                              return
                    except:
                         pass
                    if item1.HeSoKhongTinCay > 0.4:
                         luatHetHieuLuc.append(item1)
                         print("HẾT HIỆU LƯC:",luatHetHieuLuc)
               for item in luatHetHieuLuc:
                    self.luat.remove(item)
               self.luat.sort()
               for item in self.luat:
                    for i, key in enumerate(item.SuKien):
                         try:
                              # self.setCauHoi(key)
                              self.label_2.setText(str(next(iter(key))[0]))
                              self.radio_Co.setVisible(True)
                              self.radio_Khong.setVisible(True)
                              end = False
                              break
                         except:
                              pass
                    if not end:
                         break
               if end:
                    self.handling_stop_()
               
app = QtWidgets.QApplication(sys.argv)
trangChu = TrangChu()
widget = QtWidgets.QStackedWidget()
widget.addWidget(trangChu)
#widget.setFixedHeight(500)
#widget.setFixedWidth(800)
widget.resize(trangChu.width(),trangChu.height())
widget.show()
trangChu.setParent(widget)
#formLogin.show()
try:
     sys.exit(app.exec_())
except:
     print("Exiting!")
#app.exec()
# query.close() 