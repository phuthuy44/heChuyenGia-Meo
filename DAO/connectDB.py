import mysql.connector
try:
    # Kết nối đến cơ sở dữ liệu
    mydb = mysql.connector.connect(
                    host ="localhost",
                    user ="root",
                    password ="1234",
                    database ="chandoanbenh"
               )
    
    # Kiểm tra xem kết nối có thành công không
    if mydb.is_connected():
        print("Kết nối đến cơ sở dữ liệu thành công!")
    else:
        print("Kết nối đến cơ sở dữ liệu không thành công!")

except mysql.connector.Error as err:
    print("Lỗi khi kết nối đến cơ sở dữ liệu:", err)