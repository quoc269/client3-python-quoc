from datetime import date, time
import requests
import base64
import json
from pathlib import Path
#--XỬ LÝ LƯU TRỮ

# CAC HAM XU LY LUU TRU MOI THEO CACH CUA THAY
Dia_chi_Dich_vu = 'https://data-service-quoc.herokuapp.com'
Dia_chi_Media = f'''{Dia_chi_Dich_vu}/Media'''
Loai_Nguoi_dung ="Nhan_vien"
# CAC HAM XU LY LUU TRU 
#-----Doc khung html
def docKhungHTML():
    Chuoi_HTML = ""  
    Doi_tuong_A ={"quoc":"ok"}
    Ma_so_Xu_ly = "Doc_Khung_HTML" 
    Doi_tuong_B ={}
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''  
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A) 
    Doi_tuong_B = json.loads(res.text)
    if Doi_tuong_B['Kq'] == 'OK':
        Chuoi_HTML = Doi_tuong_B['Chuoi_HTML']      
    return Chuoi_HTML
#-----Doc Cong ty
def Doc_Cong_ty():
    Cong_ty = {}
    Doi_tuong_A ={"quoc":"ok"}
    Ma_so_Xu_ly = "/Doc_Cong_ty" 
    Doi_tuong_B ={}
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''  
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A) 
    Doi_tuong_B = json.loads(res.text)
    if Doi_tuong_B['Kq'] == 'OK':
        Cong_ty = Doi_tuong_B['Cong_ty']    
    return Cong_ty
#----Doc Danh sach nhan vien 
def Doc_Danh_sach_Nhan_vien():
    Danh_sach_Nhan_vien = []
    Doi_tuong_A ={"quoc":"ok"}
    Ma_so_Xu_ly = "Doc_Danh_sach_Nhan_vien" 
    Doi_tuong_B ={}
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''  
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A) 
    Doi_tuong_B = json.loads(res.text)
    if Doi_tuong_B['Kq'] == 'OK':
        Danh_sach_Nhan_vien= Doi_tuong_B['Danh_sach_Nhan_vien'] 
    return Danh_sach_Nhan_vien

#---Ghi thong tin cap nhat
def Ghi_Nhan_vien(Nhan_vien):     
    Doi_tuong_A ={"quoc":"ok", "Nhan_vien": Nhan_vien}
    Ma_so_Xu_ly = "Ghi_Nhan_vien"     
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''  
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A) 
    Doi_tuong_B = json.loads(res.text)
    return Doi_tuong_B
#---Ghi Hình Nhân viên
def Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh):       
    Ma_so_Xu_ly = "Ghi_Hinh_Nhan_vien"     
    Dia_chi_Xu_ly = f'''{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}'''
    Chuoi_Hinh =  base64.b64encode(Hinh.read())
    Chuoi_Hinh = Chuoi_Hinh.decode('utf-8')    
    Doi_tuong_A ={"Nhan_vien": Nhan_vien, "Hinh": Chuoi_Hinh}
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A)
    Doi_tuong_B = json.loads(res.text)
    return Doi_tuong_B

##--Tạo chuỗi tiền tệ
def Tao_chuoi_Tien_te(n):
  Chuoi = '${:,}'.format(n)
  Chuoi = Chuoi.replace(",", ".")
  Chuoi = Chuoi.replace("$", "")
  return Chuoi


#--XU LY GIAO DIEN 
#------Xu ly giao dien dang nhap
def Tao_Chuoi_HTML_Dang_nhap(tenDangNhap="", matKhau="", thongBaoDangNhap=""):
    Cong_ty = Doc_Cong_ty()    
    chuoiHTML = f'''<div class= "container px-3"> <h1 class="text-danger"> {thongBaoDangNhap} </h1> </div> '''
    chuoiHTML += f'''<div class= "container px-3"> <h1 class="text-primary">Tên Công ty:  {Cong_ty["Ten"]} </h1> </div>'''
    chuoiHTML += f""" <div class= "container px-3">
        <form action="/Nhan_vien/kiem-tra-dang-nhap" method="POST">            
            <div class="form-group">
              <label class="text-primary" for="name">Tên Đăng nhập</label>
              <input type="text" class="form-control" name="txtTenDangNhap" id="name" placeholder="Nhập tên đăng nhập: NV_1, NV_2,..." >
            </div>
            <div class="form-group">
              <label class="text-primary" for="pass">Mật khẩu</label>
              <input type="password" class="form-control" name="txtMatKhau" id="pass" placeholder="Nhập mật khẩu: NV_1, NV_2,...">
            </div>
            <button type="submit" class="btn btn-primary">Đăng nhập</button>
        </form>
      </div> """
    return chuoiHTML

#---Xử lý giao diện  Xem nhân viên
def Tao_Chuoi_HTML_Xem_Nhan_vien(Nhan_vien):
    Chuoi_HTML_Danh_sach_Ngoai_ngu = ""
    for nn in Nhan_vien["Danh_sach_Ngoai_ngu"]:
      Chuoi_HTML_Danh_sach_Ngoai_ngu += f'''<span class="badge badge-primary mx-3"> {nn["Ten"]}</span> '''

    Chuoi_Don_xin_Nghi = f'''<h3 class="py-5"> <span class="badge badge-success mx-3"> Danh sách Đơn xin nghỉ:  </h3>'''
    stt = 0
    for dxn in reversed(Nhan_vien["Danh_sach_Don_xin_nghi"]) :
      stt +=1
      Y_kien_Quan_ly_Don_vi = ""
      Y_kien_Quan_ly_Chi_nhanh = ""
      Chuoi_HTML_Cap_nhat_Don_Xin_nghi = ""

      if dxn["Y_kien_Quan_ly_Don_vi"]["Da_co_Y_kien"] == True:
        Y_kien_Quan_ly_Don_vi = "Đã có ý kiến"
      else:
        Y_kien_Quan_ly_Don_vi = "Chưa có ý kiến"
        Chuoi_HTML_Cap_nhat_Don_Xin_nghi += f'''
         <div>
  <!-- Modals sua Don xin nghi --> 
              <div class="container">
        <button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#CapNhatDonXinNghi-{dxn["Ngay_Nop_don"]}">Sửa Đơn</button>

        <!-- Modal -->
          <div class="modal fade" id="CapNhatDonXinNghi-{dxn["Ngay_Nop_don"]}" role="dialog">
              <div class="modal-dialog">    
              <!-- Modal content-->
              <div class="modal-content">
                  <div class="modal-header">
                  <button type="button" class="close bg-warning" data-dismiss="modal">&times;</button>            
                  </div>
                      <div class="modal-body">                
                          <!--form cap nhat don xin nghi--> 
                      
                              <div class="container py-3">
                              <h3 class="text-danger text-center">CẬP NHẬT ĐƠN XIN NGHỈ</h3>
                                  <form action="/Nhan_vien/chuc-nang-cap-nhat" method="post">
                                      <input type="hidden" name="Ma_Xu_ly" value="Cap_nhat_Don_xin_nghi"  />
                                      <input type="hidden" name="Ngay_Nop_don" value="{dxn["Ngay_Nop_don"]}" />
                                      <div class="container py-3">                           
                                      Ngày bắt đầu nghỉ:  <input type="date" name="txtNgayBatDau" value="{dxn["Ngay_Bat_dau_nghi"]}" class="form-control"  required > 
                                      Số ngày nghỉ:  <input type="number" name="SoNgay" value="{dxn["So_ngay"]}" class="form-control"  required >
                                      Lý do: <textarea name="txtLyDo" id="" cols="30" rows="3"class="form-control"  required >{dxn["Ly_do"]}</textarea> 
                                          <p class="text-center py-2"><input type="submit" value="Cập nhật" class="btn btn-primary "></p>
                                      </div>          
                                  </form>
                              </div>
                      </div>
                          <!--/form cap nhat don xin nghi-->
                          
              
              </div>
              
              </div>
          </div>  
        </div>

<!--/Modals sua Don xin nghi --> 

<!--Modal xoa Don Xin nghi -->
     <div class="container my-2">
        <button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#XoaDonXinNghi-{dxn["Ngay_Nop_don"]}">Xóa Đơn</button>

        <!-- Modal -->
        <div class="modal fade" id="XoaDonXinNghi-{dxn["Ngay_Nop_don"]}" role="dialog">
            <div class="modal-dialog">
                <!-- Modal content-->
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close bg-warning" data-dismiss="modal">&times;</button>
                    </div>
                    <div class="modal-body">
                        <!--form xoa don xin nghi-->
                        
                            <div class="container py-3">
                                <h3 class="text-danger text-center">XÓA ĐƠN XIN NGHỈ</h3>
                                <form action="/Nhan_vien/chuc-nang-cap-nhat" method="post">
                                    <input type="hidden" name="Ma_Xu_ly" value="Xoa_Don_xin_nghi" />
                                    <input type="hidden" name="Ngay_Nop_don" value="{dxn["Ngay_Nop_don"]}" />
                                    <div class="container py-3">
                                        <label> Ngày bắt đầu nghỉ : {dxn["Ngay_Bat_dau_nghi"]} </label> <br>
                                        <label> Số ngày nghỉ: {dxn["So_ngay"]}</label> <br>
                                        <label>Lý do: {dxn["Ly_do"]}</label> <br>
                                        <p class="text-center"><input type="submit" value="Xóa Đơn" class="btn btn-primary"></p>
                                    </div>

                                </form>
                            </div>
                      
                        <!--/form xoa don xin nghi-->
                    </div>


                </div>

            </div>
        </div>
    </div>

<!--/Modal xoa Don xin nghi -->
              
             
              
          
         '''
      
      if dxn["Y_kien_Quan_ly_Chi_nhanh"]["Da_co_Y_kien"] == True:
        Y_kien_Quan_ly_Chi_nhanh = "Đã có ý kiến"
      else:
        Y_kien_Quan_ly_Chi_nhanh = "Chưa có ý kiến"

      Chuoi_Don_xin_Nghi += f''' 
      <tr>
            <td>{stt}</td>
            <td>{dxn["Ngay_Nop_don"]}</td>
            <td>{dxn["Ngay_Bat_dau_nghi"]} </td>
            <td>{dxn["So_ngay"]}</td>
            <td>{dxn["Ly_do"]}</td>
            <td>{Y_kien_Quan_ly_Don_vi} - Nội dung: {dxn["Y_kien_Quan_ly_Don_vi"]["Noi_dung"]}</td>
            <td>{Y_kien_Quan_ly_Chi_nhanh} - Nội dung: {dxn["Y_kien_Quan_ly_Chi_nhanh"]["Noi_dung"]}</td>
            <td> {Chuoi_HTML_Cap_nhat_Don_Xin_nghi} </td>
      </tr>         

       '''
    
    chuoiHTML = f'''<div class="container-fluid p-2 justify-content-end "> 
    <div>
        <h5 class="text-danger">Đang đăng nhập: {Nhan_vien["Ten_Dang_nhap"]} </h5>        
    </div>
    <div class="container-fluid">
        <form action="/Nhan_vien/thoat-dang-nhap" method="POST">               
            <button type="submit" class="btn btn-primary">Thoát Đăng nhập</button>
        </form>
      </div>
    </div>  '''
    chuoiHTML += f'''  <!--button chuc data-toggle cua nhan vien -->
    <div class="container py-3">
      <div class=" row py-3">
          <div class="col-3">
             <button class=" btn btn-danger" type="button" data-toggle="collapse" data-target="#CapNhatDienThoai" aria-expanded="false" aria-controls="collapseExample">
                 Cập nhật Điện thoại
               </button>
          </div>  
          <div class="col-3">
             <button class=" btn btn-danger" type="button" data-toggle="collapse" data-target="#CapNhatDiaChi" aria-expanded="false" aria-controls="collapseExample">
                 Cập nhật Địa chỉ
               </button>
          </div>  
          <div class="col-3">
             <button class=" btn btn-danger" type="button" data-toggle="collapse" data-target="#CapNhatHinh" aria-expanded="false" aria-controls="collapseExample">
                 Cập nhật Hình
               </button>
          </div>  
          <div class="col-3">
             <button class=" btn btn-danger" type="button" data-toggle="collapse" data-target="#NopDonXinNghi" aria-expanded="false" aria-controls="collapseExample">
                 Nộp đơn xin nghỉ
               </button>
          </div>    
         </div>
    </div>
  <!--/button chuc data-toggle cua nhan vien -->
    <!--form cap nhat dien thoai-->
    <div class="container collapse bg-secondary" id="CapNhatDienThoai">
      <div class="container text-center">
          <h3 class="text-danger text-center">CẬP ĐIỆN THOẠI NHÂN VIÊN</h3>
          <form action="/Nhan_vien/chuc-nang-cap-nhat" method="post">
              <input type="hidden" name="Ma_Xu_ly" value="Cap_nhat_Dien_thoai"  />
              <input class="form-control" type="text" name = "txtDienThoai" value="{Nhan_vien["Dien_thoai"]}" required /> <br> <br>
              <input type="submit" class="btn btn-primary mx-auto py-2" value="Cập nhật" />
          </form>
      </div>
    </div>
     <!--/form cap nhat dien thoai-->
    <!--form cap nhat dia chi-->
    <div class="container collapse bg-secondary" id="CapNhatDiaChi">
      <div class="container">
           <h3 class="text-danger text-center">CẬP NHẬT ĐỊA CHỈ NHÂN VIÊN</h3>
          <form action="/Nhan_vien/chuc-nang-cap-nhat" method="post">
           <input type="hidden" name="Ma_Xu_ly" value="Cap_nhat_Dia_chi"/>
              <textarea name="txtDiaChi" id="" cols="120" rows="3"  required > {Nhan_vien["Dia_chi"]}</textarea>   <br> <br>
              <div class="text-center py-2">
                  <input type="submit" class="btn btn-primary mx-auto" value="Cập nhật"></input>
              </div>
            
          </form>
      </div>
    </div>
     <!--/form cap nhat dia chi-->  
     <!--form cap nhat Hinh-->
     <div class="container collapse bg-secondary" id="CapNhatHinh">
      <div class="container">  
          <h3 class="text-danger text-center">CẬP NHẬT HÌNH NHÂN VIÊN</h3>
          <form method="POST" action="/Nhan_vien/chuc-nang-cap-nhat" enctype="multipart/form-data">
            <input type="hidden" name="Ma_Xu_ly" value="Cap_nhat_Hinh" />
            <p><input type="file" name="Hinh_Nhan_vien"  multiple="true" required="true"></p>
            <p class="text-center py-2"><input type="submit" value="Cập nhật" class="btn btn-primary"></p>
          </form>
      </div>
      </div>
     <!--/form cap nhat Hinh-->  
     <!--form nop don xin nghi-->
     
    <div class="container collapse bg-secondary" id="NopDonXinNghi">
      <div class="container py-3">
        <h3 class="text-danger text-center">NỘP ĐƠN XIN NGHỈ</h3>
          <form action="/Nhan_vien/chuc-nang-cap-nhat" method="post">
              <input type="hidden" name="Ma_Xu_ly" value="Nop_Don_xin_nghi" />
               <div class="container py-3">                  
                 Ngày bắt đầu nghỉ:  <input type="date" name="txtNgayBatDau" value="" class="form-control"  required > 
                 Số ngày nghỉ:  <input type="number" name="SoNgay" value="" class="form-control"  required >
                  Lý do: <textarea name="txtLyDo" id="" cols="30" rows="3"class="form-control"  required ></textarea> 
                  <p class="text-center py-2"><input type="submit" value="Nộp đơn" class="btn btn-primary"></p>
               </div>          

          </form>
      </div>
    </div>
    <!--form nop don xin nghi-->'''

    chuoiHTML += f'''<div class="container">
    <div class="row">
        <div class="col-3">
         <img src="{Dia_chi_Media}/{Nhan_vien["Ma_so"]}.png" alt="{Nhan_vien["Ma_so"]}.png" class="img-thumbnail" style="height:250px; width:200px" >
        </div>
        <div class="col-9">
         <p>Họ tên: {Nhan_vien["Ho_ten"]} - Giới tính: {Nhan_vien["Gioi_tinh"]} </p>
         <p>CMND: {Nhan_vien["CMND"]} - Ngày sinh: {Nhan_vien["Ngay_sinh"]}- Mức lương:  {Tao_chuoi_Tien_te(Nhan_vien["Muc_luong"])} </p>
         <p>Điện thoại: {Nhan_vien["Dien_thoai"]} - Email: {Nhan_vien["Mail"]}     </p>
         <p>Địa chỉ:{Nhan_vien["Dia_chi"]} - Đơn vị: {Nhan_vien["Don_vi"]["Ten"]} </p>  
         <p>Danh sách ngoại ngữ: {Chuoi_HTML_Danh_sach_Ngoai_ngu} </p>        
         <p>Số đơn xin nghỉ:  <span class="badge badge-success mx-3"> {len(Nhan_vien["Danh_sach_Don_xin_nghi"])}</span> </p>                 
        </div>
    </div>
    <div class="container">                        
          <table class="table table-striped">
            <thead>
              <tr>
                <th>STT</th>
                <th>Ngày nộp</th>
                <th>Ngày bắt đầu nghỉ</th>
                <th>Số ngày nghỉ</th>
                <th>Lý do</th>
                <th>Ý kiến của Quản lý Đơn vị - Nội dung</th>
                <th>Ý kiến của Quản lý Chi nhánh - Nội dung</th>
                <th> Cập nhật đơn xin nghỉ</>
              </tr>
            </thead>
            <tbody>
              {Chuoi_Don_xin_Nghi}
            </tbody>
          </table>
          </div>
    </div> '''
    return chuoiHTML
