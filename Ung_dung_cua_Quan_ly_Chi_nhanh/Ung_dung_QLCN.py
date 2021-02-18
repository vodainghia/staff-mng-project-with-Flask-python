"""
Họ và tên SV: VÕ ĐẠI NGHĨA
MSSV: 1888049
Đề đồ án: QUẢN LÝ NHÂN VIÊN
"""
#--Khai báo sử dụng thư viện hàm
from datetime import date
from flask import Flask, Markup, request, session
#Muốn sử dụng CSDL Json thì comment dòng số 11, bỏ comment dòng số 9
#from JSON_XL_3L import *
#Muốn sử dụng CSDL SQLite thì comment dòng số 9, bỏ comment dòng số 11
from SQLITE_XL_3L import *

#--Khai báo và cấu hình ứng dụng
Ung_dung = Flask(__name__, static_url_path = "/Media", static_folder = "..\\Media")
Ung_dung.secret_key = "123456789"

#--Khai báo và khởi động Biến toàn cục
Chuoi_HTML_Khung = Doc_Khung_HTML()
Cong_ty = Doc_Cong_ty()

@Ung_dung.route("/", methods = ["GET"])
def XL_Khoi_dong():
    #--Biến nguồn: Chuoi_HTML_Khung

    #--Biến đích:
    Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLCN_1", "QLCN_1")
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Dang_nhap", methods = ["POST"])
def XL_Dang_nhap():
    #--Biến nguồn: Chuoi_HTML_Khung, Danh_sach_Chi_nhanh, Ten_Dang_nhap, Mat_khau
    Danh_sach_Quan_ly = Doc_Danh_sach_Quan_ly_Chi_nhanh()
    Ten_Dang_nhap = request.form.get("Th_Ten_Dang_nhap")
    Mat_khau = request.form.get("Th_Mat_khau")
    #--Biến đích: Quan_ly, Danh_sach_Nhan_vien
    Chuoi_HTML = ""
    Hop_le = any([Quan_ly for Quan_ly in Danh_sach_Quan_ly 
        if Quan_ly["Ten_Dang_nhap"] == Ten_Dang_nhap and Quan_ly["Mat_khau"] == Mat_khau])
    if Hop_le:
        Quan_ly = [Quan_ly for Quan_ly in Danh_sach_Quan_ly
            if Quan_ly["Ten_Dang_nhap"] == Ten_Dang_nhap and Quan_ly["Mat_khau"] == Mat_khau][0]
        session["Quan_ly"] = Quan_ly
        Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Chi_nhanh(Quan_ly)
        Danh_sach_Don_vi_Trong_Chi_nhanh = Doc_Danh_sach_Don_vi_Trong_Chi_nhanh(Cong_ty, Quan_ly)
        Chuoi_HTML = Tao_Chuoi_Thuc_don_Nguoi_dung(Quan_ly) + Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien, Danh_sach_Don_vi_Trong_Chi_nhanh)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

#****************** Xử lý Biến cố Chọn Chức năng Người dùng*************************
@Ung_dung.route("/Chon_chuc_nang", methods = ["POST"])
def XL_Quan_ly_Chon_chuc_nang():
	#===== Biến nguồn
    Quan_ly = session.get("Quan_ly")
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Chi_nhanh(Quan_ly)
    Danh_sach_Don_vi_Trong_Chi_nhanh = Doc_Danh_sach_Don_vi_Trong_Chi_nhanh(Cong_ty, Quan_ly)
    Danh_sach_Ngoai_ngu = Cong_ty["Danh_sach_Ngoai_ngu"]
    Ma_so_Chuc_nang = request.form.get("Th_Ma_so_Chuc_nang")
	#===== Tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_Thuc_don_Nguoi_dung(Quan_ly)
    if (Ma_so_Chuc_nang == "Quan_ly_Nhan_vien"):
        Chuoi_HTML += Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien, Danh_sach_Don_vi_Trong_Chi_nhanh)
    elif (Ma_so_Chuc_nang == "Bao_cao_Don_vi"):
        Bao_cao = Lap_Bao_cao_Don_vi(Danh_sach_Don_vi_Trong_Chi_nhanh, Danh_sach_Nhan_vien)
        Chuoi_HTML += Tao_Chuoi_HTML_Bao_cao_Don_vi(Bao_cao)
    elif (Ma_so_Chuc_nang == "Bao_cao_Ngoai_ngu"):
        Bao_cao = Lap_Bao_cao_Ngoai_ngu(Danh_sach_Ngoai_ngu, Danh_sach_Nhan_vien)
        Chuoi_HTML += Tao_Chuoi_HTML_Bao_cao_Ngoai_ngu(Bao_cao)
    Chuoi_HTML = Chuoi_HTML_Khung.replace('Chuoi_HTML', Chuoi_HTML)
    return Chuoi_HTML

#****************** Biến cố khi người dùng tra cứu*************************
@Ung_dung.route("/Tra_cuu", methods = ["POST"])
def XL_Tra_cuu():
    #--Biến nguồn: Chuoi_HTML_Khung, Quan_ly, Chuoi_Tra_cuu
    Quan_ly = session.get("Quan_ly")
    Chuoi_Tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
    Danh_sach_Don_vi_Trong_Chi_nhanh = Doc_Danh_sach_Don_vi_Trong_Chi_nhanh(Cong_ty, Quan_ly)
    #--Biến đích: Danh_sach_Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Chi_nhanh(Quan_ly)
    Danh_sach_Nhan_vien_Xem = Tra_cuu_Nhan_vien(Danh_sach_Nhan_vien, Chuoi_Tra_cuu)
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_Thuc_don_Nguoi_dung(Quan_ly) + Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Danh_sach_Don_vi_Trong_Chi_nhanh)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Chuyen_Don_vi", methods = ["POST"])
def XL_Chuyen_Don_vi():
    #--Biến nguồn: Chuoi_HTML_Khung, Quan_ly, Ma_so_Nhan_vien, Dien_thoai
    Quan_ly = session["Quan_ly"]
    Danh_sach_Don_vi_Trong_Chi_nhanh = Doc_Danh_sach_Don_vi_Trong_Chi_nhanh(Cong_ty, Quan_ly)
    Ma_so_Nhan_vien = request.form.get("Th_Ma_so_Nhan_vien")
    Ma_so_Don_vi = request.form.get("Th_Ma_so_Don_vi")
    
    #--Biến đích: Danh_sach_Nhan_vien, Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Chi_nhanh(Quan_ly)
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    for Don_vi in Danh_sach_Don_vi_Trong_Chi_nhanh:
        if Don_vi["Ma_so"] == Ma_so_Don_vi:
            Nhan_vien["Don_vi"] = Don_vi
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_Thuc_don_Nguoi_dung(Quan_ly) + Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Danh_sach_Don_vi_Trong_Chi_nhanh)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Cho_Y_Kien_Don_xin_nghi", methods = ["POST"])
def XL_Cho_Y_Kien_Don_xin_nghi():
    #--Biến nguồn: Chuoi_HTML_Khung, Nhan_vien, Dia_chi
    Quan_ly = session["Quan_ly"]
    Danh_sach_Don_vi_Trong_Chi_nhanh = Doc_Danh_sach_Don_vi_Trong_Chi_nhanh(Cong_ty, Quan_ly)
    Ma_so_Nhan_vien = request.form.get("Th_Ma_so_Nhan_vien")
    Lan_nghi = request.form.get("Th_Lan_nghi")
    Cho_Y_Kien_Don_xin_nghi = request.form.get("Th_Y_kien_cua_QLCN_Noi_dung")
    #--Biến đích: Danh_sach_Nhan_vien, Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Chi_nhanh(Quan_ly)
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    for Don_Xin_nghi in Nhan_vien["Cac_Don_xin_nghi"]:
        if Don_Xin_nghi["STT"] == int(Lan_nghi):
            Don_Xin_nghi["Y_kien_cua_QLCN"]["Noi_dung"] = Cho_Y_Kien_Don_xin_nghi
            Don_Xin_nghi["Y_kien_cua_QLCN"]["Ngay"] = str(date.today())
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_Thuc_don_Nguoi_dung(Quan_ly) + Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Danh_sach_Don_vi_Trong_Chi_nhanh)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML