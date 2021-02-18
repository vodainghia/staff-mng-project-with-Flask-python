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
Ung_dung = Flask(__name__, static_url_path="/Media", static_folder="..\\Media")
Ung_dung.secret_key = "123456789"

#--Khai báo và khởi động Biến toàn cục 
Chuoi_HTML_Khung = Doc_Khung_HTML()
Cong_ty = Doc_Cong_ty()

@Ung_dung.route("/", methods = ["GET"])
def XL_Khoi_dong():
    #--Biến nguồn: Chuoi_HTML_Khung
    
    #--Biến đích:
    Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLDV_1", "QLDV_1")
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Dang_nhap", methods = ["POST"])
def XL_Dang_nhap():
    #--Biến nguồn: Chuoi_HTML_Khung, Danh_sach_Don_vi, Ten_Dang_nhap, Mat_khau
    Danh_sach_Quan_ly_Don_vi = Doc_Danh_sach_Quan_ly_Don_vi()
    Ten_Dang_nhap = request.form.get("Th_Ten_Dang_nhap")
    Mat_khau = request.form.get("Th_Mat_khau")
    #--Biến đích: Quan_ly, Danh_sach_Nhan_vien
    Chuoi_HTML = ""
    Hop_le = any([Quan_ly for Quan_ly in Danh_sach_Quan_ly_Don_vi
        if Quan_ly["Ten_Dang_nhap"] == Ten_Dang_nhap and Quan_ly["Mat_khau"] == Mat_khau])
    if Hop_le:
        Quan_ly = [Quan_ly for Quan_ly in Danh_sach_Quan_ly_Don_vi
            if Quan_ly["Ten_Dang_nhap"] == Ten_Dang_nhap and Quan_ly["Mat_khau"] == Mat_khau][0]
        session["Quan_ly"] = Quan_ly
        Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Don_vi(Quan_ly)
        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien, Cong_ty)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Tra_cuu", methods = ["POST"])
def XL_Tra_cuu():
    #--Biến nguồn: Chuoi_HTML_Khung, Quan_ly, Chuoi_Tra_cuu
    Quan_ly = session.get("Quan_ly")
    Chuoi_Tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
    #--Biến đích: Danh_sach_Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Don_vi(Quan_ly)
    Danh_sach_Nhan_vien_Xem = Tra_cuu_Nhan_vien(Danh_sach_Nhan_vien, Chuoi_Tra_cuu)
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Cong_ty)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Cap_nhat_Dien_thoai", methods = ["POST"])
def XL_Cap_nhat_Dien_thoai():
    #--Biến nguồn: Chuoi_HTML_Khung, Quan_ly, Ma_so_Nhan_vien, Dien_thoai
    Quan_ly = session["Quan_ly"]
    Ma_so_Nhan_vien = request.form.get("Th_Ma_so_Nhan_vien")
    Dien_thoai = request.form.get("Th_Dien_thoai")
    #--Biến đích: Danh_sach_Nhan_vien, Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Don_vi(Quan_ly)
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    Nhan_vien["Dien_thoai"] = Dien_thoai
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Cong_ty)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Cap_nhat_Dia_chi", methods = ["POST"])
def XL_Cap_nhat_Dia_chi():
    #--Biến nguồn: Chuoi_HTML_Khung, Quan_ly, Ma_so_Nhan_vien, Dia_chi
    Quan_ly = session["Quan_ly"]
    Ma_so_Nhan_vien = request.form.get("Th_Ma_so_Nhan_vien")
    Dia_chi = request.form.get("Th_Dia_chi")
    #--Biến đích: Danh_sach_Nhan_vien, Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Don_vi(Quan_ly)
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    Nhan_vien["Dia_chi"] = Dia_chi
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Cong_ty)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML
    
@Ung_dung.route("/Cap_nhat_Hinh", methods = ["POST"])
def XL_Cap_nhat_Hinh():
    #--Biến nguồn: Chuoi_HTML_Khung, Quan_ly, Ma_so_Nhan_vien, Hinh
    Quan_ly = session["Quan_ly"]
    Ma_so_Nhan_vien = request.form.get("Th_Ma_so_Nhan_vien")
    Hinh = request.files["Th_Hinh"]
    #--Biến đích: Danh_sach_Nhan_vien, Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Don_vi(Quan_ly)
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Cong_ty)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Bo_sung_Ngoai_ngu", methods = ["POST"])
def XL_Bo_sung_Ngoai_ngu():
    #--Biến nguồn: Chuoi_HTML_Khung, Quan_ly, Ma_so_Nhan_vien, Dia_chi
    Quan_ly = session["Quan_ly"]
    Ma_so_Nhan_vien = request.form.get("Th_Ma_so_Nhan_vien")
    Ma_so_Ngoai_ngu = request.form.get("Th_Ma_so_Ngoai_ngu")
    #--Biến đích: Danh_sach_Nhan_vien, Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Don_vi(Quan_ly)
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    for Ngoai_ngu in Cong_ty["Danh_sach_Ngoai_ngu"]:
        if Ngoai_ngu["Ma_so"] == Ma_so_Ngoai_ngu:
            Nhan_vien["Danh_sach_Ngoai_ngu"].append(Ngoai_ngu)
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Cong_ty)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Huy_Ngoai_ngu", methods = ["POST"])
def XL_Huy_Ngoai_ngu():
    #--Biến nguồn: Chuoi_HTML_Khung, Quan_ly, Ma_so_Nhan_vien, Dia_chi
    Quan_ly = session["Quan_ly"]
    Ma_so_Nhan_vien = request.form.get("Th_Ma_so_Nhan_vien")
    Ma_so_Ngoai_ngu = request.form.get("Th_Ma_so_Ngoai_ngu")
    #--Biến đích: Danh_sach_Nhan_vien, Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Don_vi(Quan_ly)
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    for Ngoai_ngu in Nhan_vien["Danh_sach_Ngoai_ngu"]:
        if Ngoai_ngu["Ma_so"] == Ma_so_Ngoai_ngu:
            Nhan_vien["Danh_sach_Ngoai_ngu"].remove(Ngoai_ngu)
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Cong_ty)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML

@Ung_dung.route("/Cho_Y_Kien_Don_xin_nghi", methods = ["POST"])
def XL_Cho_Y_Kien_Don_xin_nghi():
    #--Biến nguồn: Chuoi_HTML_Khung, Nhan_vien, Dia_chi
    Quan_ly = session["Quan_ly"]
    Ma_so_Nhan_vien = request.form.get("Th_Ma_so_Nhan_vien")
    Lan_nghi = request.form.get("Th_Lan_nghi")
    Cho_Y_Kien_Don_xin_nghi = request.form.get("Th_Y_kien_cua_QLDV_Noi_dung")
    #--Biến đích: Danh_sach_Nhan_vien, Nhan_vien, Danh_sach_Nhan_vien_Xem
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien_Theo_Don_vi(Quan_ly)
    Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien if Nhan_vien["Ma_so"] == Ma_so_Nhan_vien][0]
    for Don_Xin_nghi in Nhan_vien["Cac_Don_xin_nghi"]:
        if Don_Xin_nghi["STT"] == int(Lan_nghi):
            Don_Xin_nghi["Y_kien_cua_QLDV"]["Noi_dung"] = Cho_Y_Kien_Don_xin_nghi
            Don_Xin_nghi["Y_kien_cua_QLDV"]["Ngay"] = str(date.today())
    Ghi_Nhan_vien(Nhan_vien)
    Danh_sach_Nhan_vien_Xem = [Nhan_vien]
    #--Xử lý tạo kết xuất
    Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien_Xem, Cong_ty)
    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML