class Luat:
     def __init__(self, maLuat, tenLuat, suKien):
        self.maLuat = maLuat
        self.tenLuat = tenLuat
        self.suKien = suKien
        self.heSoTinCay = 0
        self.heSoKhongTinCay = 0

     def __lt__(self, other):
        return self.heSoTinCay > other.heSoTinCay
