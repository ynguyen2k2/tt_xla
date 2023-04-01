Xin chào các bạn 
Đây là main file tt_xla thứ 4 nhóm 2
git clone <repo> ## đường link github cần clone  
thêm file vào staged 
git add <tên file>
git add .      ##upload tất cả các file trong thư mục 
git commit -m  <message>
git push  ## đối với branch main 

tạo branch 
git branch <tên branch mới>
chuyển đến branch 
git checkout <tên branch>

đối với merge file trong branch các bạn cần 

sau khi git commit xong thì

git push --set-upsteam <tên branch>
git checkout main 
git merge <tên branch >