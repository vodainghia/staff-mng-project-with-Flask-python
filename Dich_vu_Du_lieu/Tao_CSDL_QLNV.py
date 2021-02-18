import sys

#thêm đường dẫn chứa file JSON_XL_3L có đầy đủ phương thức để hỗ trợ tạo CSDL vào system variables:
sys.path.append("G:\\IT\\1.HCMUS\\1.Mon-hoc\\CTT504-PTTKPM\\1888049-VoDaiNghia-QLNV\\Ung_dung_cua_Quan_ly_Chi_nhanh")

for x in sys.path:
    print(x)

import JSON_XL_3L
import json
import sqlite3

Ten_CSDL = "QLNV.sqlite"
Thu_muc_Du_lieu = "..\Dich_vu_Du_lieu"
Duong_dan_CSDL = f"{Thu_muc_Du_lieu}\\{Ten_CSDL}"

def Tao_Cau_truc_CSDL_QLNV():
    Ket_noi = sqlite3.connect(Duong_dan_CSDL)
    Lenh = f"CREATE TABLE if not exists CONGTY(Ma_so, Chuoi_JSON)"
    Ket_noi.execute(Lenh)
    Lenh = f"CREATE TABLE if not exists NHANVIEN(Ma_so, Chuoi_JSON)"
    Ket_noi.execute(Lenh)
    Lenh = f"CREATE TABLE if not exists QUANLYDONVI(Ma_so, Chuoi_JSON)"
    Ket_noi.execute(Lenh)
    Lenh = f"CREATE TABLE if not exists QUANLYCHINHANH(Ma_so, Chuoi_JSON)"
    Ket_noi.execute(Lenh)
    Ket_noi.commit()
    Ket_noi.close()

def Chuyen_Du_lieu_CSDL_QLNV():
    Ket_noi = sqlite3.connect(Duong_dan_CSDL)
    Cong_ty = JSON_XL_3L.Doc_Cong_ty()
    Ma_so = Cong_ty["Ma_so"]
    Chuoi_JSON = json.dumps(Cong_ty, indent = 4)
    Lenh = f"INSERT INTO CONGTY VALUES('{Ma_so}', '{Chuoi_JSON}')"
    Ket_noi.execute(Lenh)
    Ket_noi.commit()

    Danh_sach_Nhan_vien = JSON_XL_3L.Doc_Danh_sach_Nhan_vien()
    for Nhan_vien in Danh_sach_Nhan_vien:
        Ma_so = Nhan_vien["Ma_so"]
        Chuoi_JSON = json.dumps(Nhan_vien, indent = 4)
        Lenh = f"INSERT INTO NHANVIEN VALUES('{Ma_so}', '{Chuoi_JSON}')"
        Ket_noi.execute(Lenh)
        Ket_noi.commit()

    Danh_sach_Quan_ly_Don_vi = JSON_XL_3L.Doc_Danh_sach_Quan_ly_Don_vi()
    for Quan_ly_Don_vi in Danh_sach_Quan_ly_Don_vi:
        Ma_so = Quan_ly_Don_vi["Ma_so"]
        Chuoi_JSON = json.dumps(Quan_ly_Don_vi, indent = 4)
        Lenh = f"INSERT INTO QUANLYDONVI VALUES('{Ma_so}', '{Chuoi_JSON}')"
        Ket_noi.execute(Lenh)
        Ket_noi.commit()
    
    Danh_sach_Quan_ly_Chi_nhanh = JSON_XL_3L.Doc_Danh_sach_Quan_ly_Chi_nhanh()
    for Quan_ly_Chi_nhanh in Danh_sach_Quan_ly_Chi_nhanh:
        Ma_so = Quan_ly_Chi_nhanh["Ma_so"]
        Chuoi_JSON = json.dumps(Quan_ly_Chi_nhanh, indent = 4)
        Lenh = f"INSERT INTO QUANLYCHINHANH VALUES('{Ma_so}', '{Chuoi_JSON}')"
        Ket_noi.execute(Lenh)
        Ket_noi.commit()

    Ket_noi.close()

Tao_Cau_truc_CSDL_QLNV()
Chuyen_Du_lieu_CSDL_QLNV()
