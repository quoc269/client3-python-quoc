from datetime import timedelta
from datetime import datetime
from flask import Flask, request 
from flask.globals import session
from XL_3L_Nhan_Vien import*

DichVu = Flask(__name__, static_url_path="/Media_Nhan_vien", static_folder="Media_Nhan_vien")
DichVu.secret_key = "QuocNguyen" 

#--biến dùng chung

#--Xử lý biến cố khơi động
@DichVu.route("/")
def XL_KhoiDong():  
    khungHTML = docKhungHTML() 
    chuoiHTML = Tao_Chuoi_HTML_Dang_nhap()
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)    
    return chuoiHTML

#--Xử lý biến cố đăng nhập
@DichVu.route("/Nhan_vien/kiem-tra-dang-nhap", methods =["POST"])
def XL_DangNhapNhanVien():
    khungHTML = docKhungHTML()
    Danh_sach_Nhan_vien = Doc_Danh_sach_Nhan_vien()
    tenDangNhap = request.form["txtTenDangNhap"]
    matKhau = request.form["txtMatKhau"]
    chuoiHTML =''
    Hop_le = any([Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien
                    if Nhan_vien['Ten_Dang_nhap']== tenDangNhap and Nhan_vien['Mat_khau']==matKhau ])
    if Hop_le:
        Nhan_vien = [Nhan_vien for Nhan_vien in Danh_sach_Nhan_vien
                          if Nhan_vien['Ten_Dang_nhap']== tenDangNhap and Nhan_vien['Mat_khau']==matKhau][0]            
        session['Nguoi_dung'] = Nhan_vien
        chuoiHTML = Tao_Chuoi_HTML_Xem_Nhan_vien( Nhan_vien)
    else:
        chuoiHTML = Tao_Chuoi_HTML_Dang_nhap("","","Đăng nhập không hợp lệ")
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)
    return chuoiHTML

#--Xử lý chức năng \Nhan_vien\chuc-nang-cap-nhat
@DichVu.route("/Nhan_vien/chuc-nang-cap-nhat", methods=["POST"])
def XL_ChucNangCapNhat_Nhan_vien():
    Nhan_vien ={}   
    chuoiHTML =""
    if "Nguoi_dung" in session:
        Nhan_vien = session['Nguoi_dung']          
    khungHTML = docKhungHTML() 
    Ma_Xu_ly = request.form["Ma_Xu_ly"]
    if Ma_Xu_ly == "Cap_nhat_Dien_thoai":
        sdtMoi = request.form["txtDienThoai"]  
        Nhan_vien["Dien_thoai"] = sdtMoi
        Ghi_Nhan_vien(Nhan_vien)
        chuoiHTML = Tao_Chuoi_HTML_Xem_Nhan_vien( Nhan_vien)
        chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)
    elif Ma_Xu_ly == "Cap_nhat_Dia_chi":
        Dia_chi = request.form["txtDiaChi"]    
        Nhan_vien["Dia_chi"] = Dia_chi
        Ghi_Nhan_vien(Nhan_vien)
        chuoiHTML = Tao_Chuoi_HTML_Xem_Nhan_vien( Nhan_vien)
        chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)
    elif Ma_Xu_ly == "Cap_nhat_Hinh":
        Hinh_Nhan_vien = request.files['Hinh_Nhan_vien']
        Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh_Nhan_vien)    
        chuoiHTML = Tao_Chuoi_HTML_Xem_Nhan_vien(Nhan_vien)
        chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML) 
    elif Ma_Xu_ly == "Cap_nhat_Don_xin_nghi":
        Ngay_nop_Don_xin_nghi = request.form["Ngay_Nop_don"]  
        for dxn in Nhan_vien["Danh_sach_Don_xin_nghi"]:
            if dxn["Ngay_Nop_don"] == Ngay_nop_Don_xin_nghi:
                Ngay_Bat_dau_nghi_Chuoi = request.form["txtNgayBatDau"]
                Ngay_Bat_dau_nghi = datetime.strptime(Ngay_Bat_dau_nghi_Chuoi,"%Y-%m-%d") # dinh dang microsecond
                Ngay_Bat_dau_nghi = Ngay_Bat_dau_nghi.timestamp()
                Ngay_Nop_don = datetime.now()
                Cong_ty = Doc_Cong_ty()
                Ngay_cho_Toi_thieu_truoc_nghi = Cong_ty["Quy_dinh_Xin_nghi"]["Ngay_cho_Toi_thieu_Truoc_nghi"]
                Ngay_cho_nghi_hop_le = Ngay_Nop_don + timedelta(Ngay_cho_Toi_thieu_truoc_nghi)
                Ngay_cho_nghi_hop_le = Ngay_cho_nghi_hop_le.timestamp()
                So_ngay = int(request.form["SoNgay"])       
                Ly_do = request.form["txtLyDo"] 
                if Ngay_Bat_dau_nghi >= Ngay_cho_nghi_hop_le and So_ngay <= Cong_ty["Quy_dinh_Xin_nghi"]["Ngay_nghi_Toi_da"]:
                    dxn["Ngay_Nop_don"]= datetime.now().strftime("%Y-%m-%d-%H-%M-%S") 
                    dxn["Ngay_Bat_dau_nghi"] = Ngay_Bat_dau_nghi_Chuoi
                    dxn["So_ngay"]= So_ngay
                    dxn["Ly_do"]= Ly_do 
                    Ghi_Nhan_vien(Nhan_vien) 
                    session['Nguoi_dung'] = Nhan_vien  
                    chuoiHTML = Tao_Chuoi_HTML_Xem_Nhan_vien( Nhan_vien)
                    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)
                else:
                    chuoiHTML += f'''<div class="alert alert-danger alert-dismissible">
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                    <strong>Cập nhật đơn xin nghỉ không hợp lệ</strong> Vui lòng kiểm tra quy định của công ty.            
                    </div>'''
                    session['Nguoi_dung'] = Nhan_vien  
                    chuoiHTML += Tao_Chuoi_HTML_Xem_Nhan_vien( Nhan_vien)
                    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)   

    elif Ma_Xu_ly == "Xoa_Don_xin_nghi":
        Ngay_nop_Don_xin_nghi = request.form["Ngay_Nop_don"]  
        for Don_xin_nghi in Nhan_vien["Danh_sach_Don_xin_nghi"]:
            if Don_xin_nghi["Ngay_Nop_don"] == Ngay_nop_Don_xin_nghi:
                Nhan_vien["Danh_sach_Don_xin_nghi"].remove(Don_xin_nghi)
                Ghi_Nhan_vien(Nhan_vien) 
                session['Nguoi_dung'] = Nhan_vien  
                chuoiHTML = Tao_Chuoi_HTML_Xem_Nhan_vien( Nhan_vien)
                chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)

    else:
        Ngay_Bat_dau_nghi_Chuoi = request.form["txtNgayBatDau"]
        Ngay_Bat_dau_nghi = datetime.strptime(Ngay_Bat_dau_nghi_Chuoi,"%Y-%m-%d") # dinh dang microsecond
        Ngay_Bat_dau_nghi = Ngay_Bat_dau_nghi.timestamp()
        Ngay_Nop_don = datetime.now()
        Cong_ty = Doc_Cong_ty()
        Ngay_cho_Toi_thieu_truoc_nghi = Cong_ty["Quy_dinh_Xin_nghi"]["Ngay_cho_Toi_thieu_Truoc_nghi"]
        Ngay_cho_nghi_hop_le = Ngay_Nop_don + timedelta(Ngay_cho_Toi_thieu_truoc_nghi)
        Ngay_cho_nghi_hop_le = Ngay_cho_nghi_hop_le.timestamp()
        So_ngay = int(request.form["SoNgay"])       
        Ly_do = request.form["txtLyDo"] 
        if Ngay_Bat_dau_nghi >= Ngay_cho_nghi_hop_le and So_ngay <= Cong_ty["Quy_dinh_Xin_nghi"]["Ngay_nghi_Toi_da"]:
            Don_xin_nghi = {
                "Ngay_Nop_don": datetime.now().strftime("%Y-%m-%d-%H-%M-%S") ,
                    "Ngay_Bat_dau_nghi":Ngay_Bat_dau_nghi_Chuoi,
                    "So_ngay": So_ngay,
                    "Ly_do": Ly_do,
                    "Y_kien_Quan_ly_Don_vi": {
                        "Ngay": "",
                        "Da_co_Y_kien": False,
                        "Noi_dung": ""
                    },
                    "Y_kien_Quan_ly_Chi_nhanh": {
                        "Ngay": "",
                        "Da_co_Y_kien": False,
                        "Noi_dung": ""
                    }	
            }
            Nhan_vien["Danh_sach_Don_xin_nghi"].append(Don_xin_nghi)
            Ghi_Nhan_vien(Nhan_vien) 
            session['Nguoi_dung'] = Nhan_vien  
            chuoiHTML = Tao_Chuoi_HTML_Xem_Nhan_vien( Nhan_vien)
            chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)
        else:
            chuoiHTML += f'''<div class="alert alert-success alert-dismissible">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            <strong>Nộp đơn xin nghỉ không hợp lệ</strong> Vui lòng kiểm tra quy định của công ty.            
            </div>'''
            session['Nguoi_dung'] = Nhan_vien  
            chuoiHTML += Tao_Chuoi_HTML_Xem_Nhan_vien( Nhan_vien)
            chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)

    return chuoiHTML


#Xử lý biến cố thoát đăng nhập
@DichVu.route("/Nhan_vien/thoat-dang-nhap", methods=["POST"])
def XL_ThoatDangNhap():
    khungHTML = docKhungHTML()
    if "Nguoi_dung" in session:
         session.pop("Nguoi_dung", None)    
    chuoiHTML = Tao_Chuoi_HTML_Dang_nhap()
    chuoiHTML = khungHTML.replace("chuoiHTML", chuoiHTML)    
    return chuoiHTML
#--Xóa cache browser
@DichVu.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

#--Run chuong trinh
if __name__ == '__main__':
   DichVu.run()
