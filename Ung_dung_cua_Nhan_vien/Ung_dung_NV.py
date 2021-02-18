"""
Họ và tên SV: VÕ ĐẠI NGHĨA
MSSV: 1888049
Đề đồ án: QUẢN LÝ NHÂN VIÊN
"""
#--Khai báo sử dụng thư viện hàm
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

@Ung_dung.route("/", methods = ["GET"])
def XL_Khoi_dong():
    #--Biến nguồn: Chuoi_HTML_Khung

    #--Biến đích:
    Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_2", "NV_2")
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Dang_nhap", methods = ["POST"])
def XL_Dang_nhap():
    #--Biến nguồn: Chuoi_HTML_Khung, Danh_sach_Nhan_vien, Ten_Dang_nhap, Mat_khau
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien()
    Ten_Dang_nhap = request.form.get("Th_Ten_Dang_nhap")
    Mat_khau = request.form.get("Th_Mat_khau")
    #--Biến đích: Nhan_vien, Danh_sach_Nhan_vien_Xem
    Chuoi_HTML = ""
    Hop_le = any([Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien 
        if Nhan_vien["Ten_Dang_nhap"] == Ten_Dang_nhap and Nhan_vien["Mat_khau"] == Mat_khau])
    if Hop_le:
        Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien
            if Nhan_vien["Ten_Dang_nhap"] == Ten_Dang_nhap and Nhan_vien["Mat_khau"] == Mat_khau][0]
        session["Nhan_vien"] = Nhan_vien
        Danh_sach_Nhan_vien_Xem = [Nhan_vien]
        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Cap_nhat_Dien_thoai", methods = ["POST"])
def XL_Cap_nhat_Dien_thoai():
    #--Biến nguồn: Chuoi_HTML_Khung, Nhan_vien, Dien_thoai
    Nhan_vien = session["Nhan_vien"]
    Dien_thoai = request.form.get("Th_Dien_thoai")
    #--Biến đích: Nhan_vien, Danh_sach_Nhan_vien_Xem
    Nhan_vien["Dien_thoai"] = Dien_thoai
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    session["Nhan_vien"] = Nhan_vien
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML
    
@Ung_dung.route("/Cap_nhat_Dia_chi", methods = ["POST"])
def XL_Cap_nhat_Dia_chi():
    #--Biến nguồn: Chuoi_HTML_Khung, Nhan_vien, Dia_chi
    Nhan_vien = session["Nhan_vien"]
    Dia_chi = request.form.get("Th_Dia_chi")
    #--Biến đích: Nhan_vien, Danh_sach_Nhan_vien_Xem
    Nhan_vien["Dia_chi"] = Dia_chi
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    session["Nhan_vien"] = Nhan_vien
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Cap_nhat_Hinh", methods = ["POST"])
def XL_Cap_nhat_Hinh():
    #--Biến nguồn: Chuoi_HTML_Khung, Nhan_vien, Hinh
    Nhan_vien = session["Nhan_vien"]
    Hinh = request.files["Th_Hinh"]
    #--Biến đích: Nhan_vien, Danh_sach_Nhan_vien_Xem
    Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    session["Nhan_vien"] = Nhan_vien
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Nop_Don_xin_nghi", methods = ["POST"])
def XL_Nop_Don_xin_nghi():
    #--Biến nguồn: Chuoi_HTML_Khung, Nhan_vien, Dia_chi
    Nhan_vien = session["Nhan_vien"]
    Ngay_Bat_dau = request.form.get("Th_Ngay_Bat_dau")
    So_ngay = request.form.get("Th_So_ngay")
    Ly_do = request.form.get("Th_Ly_do")
    #--Biến đích: Nhan_vien, Danh_sach_Nhan_vien_Xem
    Nhan_vien = Tao_Don_Xin_nghi(Nhan_vien, Ngay_Bat_dau, So_ngay, Ly_do)
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    session["Nhan_vien"] = Nhan_vien
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML