import decimal
import sys
import os
import PyQt5
from fuzzywuzzy import fuzz
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from PyQt5 import QtWidgets,uic,QtGui,QtCore
from PyQt5.QtWidgets import QListWidgetItem,QFrame,QMessageBox,QRadioButton,QHBoxLayout
from BUS.fillDataBUS import fillDataBUS

class TrangChu(QtWidgets.QMainWindow):
     def __init__(self):
          super(TrangChu,self).__init__()
          uic.loadUi("GUI/frameTrangChu.ui",self)
          self.heSoTinCay = 0
          self.heSoKhongTinCay = 0
          # self.img_base64 = None
          # self.role =None
          # self.stackedWidget.setCurrentIndex(0)
          #self.btnHSPL.clicked.connect(self.stackHSPL)
          # self.getTenDangNhap() 
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
                    similarity = fuzz.ratio(txtSearch, item.lower())  # So sánh với triệu chứng đã chuyển đổi thành chữ thường
                    if similarity >= 30:  # Chỉ hiển thị triệu chứng có độ tương đồng >= 25
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
          try:
               tam = self.luat[0]
               # print("hello",tam[2])
               khongtraloi = False
               for i in self.luat:
                    if tam[2] < i[2]:
                         tam = i
               if tam[2] > 0.6 & tam[2]< 0.7:
                    self.txtResult.setText("Có thể bạn đã mắc")
               else:
                    self.txtResult.setText("Chưa đủ dẫn chứng")
               if khongtraloi == False:
                    self.txtResult.Text += tam[1];
          except:
               pass
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
                    #fill danh sách mã triệu chứng tương ứng với hệ số dựa trên mã bệnh
                    # if len(getMa) > 0:
                    #      getMa = getMa[0]
                    for i in getMa:
                         suKienThoaMan = fillDataBUS.getsymptom(self,i)
                         #cac bệnh thoa man dựa trên mã bệnh
                         luatThoaMan = fillDataBUS.getDisease(self,i)
                         print("Luât thõa man:",luatThoaMan)
                         for i in suKienThoaMan:
                              #Khởi tạo dictionary để lưu trữ các triệu chứng
                              danhSachCauHoi = fillDataBUS.getCauHoi(self,suKienThoaMan[0][0])
                              suKien[suKienThoaMan[0][1]]=danhSachCauHoi
                         self.luat.append((luatThoaMan[0][0],luatThoaMan[0][1],suKien))
                         print("Luật:",self.luat)
                    for item1 in self.luat:
                         try:
                              key = list(self.quaTrinhSuyDien.keys())[0]
                              heSo = item1[2][key]
                              del item1[2][key]
                              self.heSoTinCay += heSo
                         except:
                              pass
                    self.luat.sort()
                    self.label_2.setWordWrap(True)
                    self.label_2.setText(str(next(iter(self.luat[0][2].values()))))  # Truy cập vào 'suKien' trong tuple
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
                    for decimal_value, symptom_list in item1[2].items():
                         print(item1[2])
                         try:
                              heSo = item1[2][key]  # Giả sử item1 là một tuple, và suKien là phần tử thứ 3 của tuple đó
                              del item1[2][key]
                              if selected == "Có":
                                   self.heSoTinCay += heSo  # Giả sử HeSoTinCay được lưu ở phần tử thứ 2 của tuple
                              else:
                                   self.heSoKhongTinCay += heSo 
                              if decimal_value> 0.9:
                                   self.txtResult.Text = "Chắc chắn bạn đã mắc " + item1.TenLuat;
                                   # QMessageBox.information("Thông báo","Cám ơn!")
                                   self.btnNext.setEnabled(False);
                              # btnKetThuc.Enabled = false;
                              # uctrlThongTinBoSung.RadCo.Enabled = false;
                              # uctrlThongTinBoSung.RadKhong.Enabled = false;
                                   return
                         
                         except:
                              pass
                         if decimal_value > 0.4:
                              luatHetHieuLuc.append(item1)
               for i in luatHetHieuLuc:
                    if i in self.luat:
                         self.luat.remove(i)
               self.luat.sort()
               # if not self.luat:
               #      # self.btnNext.setEnabled(False);
               #      self.txtResult.setText("Tạm biệt bạn!")
               # else:
               for item in self.luat:
                         # print(item)
                    for key, value in item[2].items():
                         # print(value)
                         self.label_2.setText(str(value))
                         self.radio_Co.setVisible(True) 
                         self.radio_Khong.setVisible(True)
                         # if len(self.luat) == 1:  # Nếu chỉ có một câu hỏi trong luật
                         #      self.txtResult.setText("Đã kết thúc!")
                              # self.btnNext.setEnabled(False)
                         end = False
                         # break  # Thoát khỏi vòng lặp sau khi hiển thị câu hỏi đầu tiên
                    # Kiểm tra xem có tiếp tục hiển thị câu hỏi mới hay không
               if end:
                    self.handling_stop_()
                    #      if len(self.luat) == 1:  # Nếu chỉ có một câu hỏi trong luật
                    #           self.txtResult.setText("Đã kết thúc!")
                    # # ketThucSuyDien();
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