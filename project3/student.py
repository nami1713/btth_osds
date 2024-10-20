from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Hệ thống quản lý sinh viên")
root.geometry("600x800")

# Kết nối tới db
conn = sqlite3.connect('student_book.db')
c = conn.cursor()

# Tao bang de luu tru
c.execute('''
    CREATE TABLE students(
        id INTEGER PRIMARY KEY,
        first_name text,
        last_name text,
        class text,
        entry_year integer,
        average float
    )
'''
)

def them():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    # Lấy dữ liệu đã nhập
    id_value = stu_id.get()
    name_value =f_name.get()
    lastName_value = l_name.get()
    class_value = classes.get()
    entryYear_value = en_year.get()
    average_value = average.get()
    # Thực hiện câu lệnh để thêm
    c.execute('''
        INSERT INTO 
        students (id, first_name, last_name, class, entry_year, average)
        VALUES 
        (:id, :name, :last_name, :class, :entry_year, :average)
    ''',{
        'id' : id_value,
        'name' : name_value,
        'last_name' : lastName_value,
        'class': class_value,
        'entry_year': entryYear_value,
        'average': average_value,
      }
    )
    conn.commit()
    conn.close()

    # Reset form
    stu_id.delete(0, END)
    f_name.delete(0, END)
    l_name.delete(0, END)
    classes.delete(0, END)
    en_year.delete(0, END)
    average.delete(0, END)

    # Hien thi lai du lieu
    truy_van()

def xoa():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    c.execute('''DELETE FROM
                        students 
                      WHERE id=:id''',
              {'id':delete_box.get()})
    delete_box.delete(0, END)
    conn.commit()
    conn.close()
    # Hiên thi thong bao
    messagebox.showinfo("Thông báo", "Đã xóa!")
    # Hiển thị lại dữ liệu
    truy_van()


def truy_van():
    # Xóa đi các dữ liệu trong TreeView
    for row in tree.get_children():
        tree.delete(row)

    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    records = c.fetchall()

    # Hien thi du lieu
    for r in records:
        tree.insert("", END, values=(r[0], r[1], r[2]))

    # Ngat ket noi
    conn.close()
def chinh_sua():
    global editor
    editor = Tk()
    editor.title('Cập nhật bản ghi')
    editor.geometry("400x300")

    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("SELECT * FROM students WHERE id=:id", {'id':record_id})
    records = c.fetchall()

    global f_name_editor, l_name_editor, classes_editor, en_year_editor, average_editor

    f_id_editor = Entry(editor, width=30)
    f_id_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=1, column=1, padx=20)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=2, column=1)
    classes_editor = Entry(editor, width=30)
    classes_editor.grid(row=3, column=1)
    en_year_editor = Entry(editor, width=30)
    en_year_editor.grid(row=4, column=1)
    average_editor = Entry(editor, width=30)
    average_editor.grid(row=5, column=1)

    f_id_label = Label(editor, text="Mã sinh viên")
    f_id_label.grid(row=0, column=0, pady=(10, 0))
    f_name_label = Label(editor, text="Họ")
    f_name_label.grid(row=1, column=0)
    l_name_label = Label(editor, text="Tên")
    l_name_label.grid(row=2, column=0)
    classes_label = Label(editor, text="Mã lớp")
    classes_label.grid(row=3, column=0)
    en_year_label = Label(editor, text="Năm nhập học")
    en_year_label.grid(row=4, column=0)
    average_label = Label(editor, text="Điểm trung bình")
    average_label.grid(row=5, column=0)

    for record in records:
        f_id_editor.insert(0, record[0])
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        classes_editor.insert(0, record[3])
        en_year_editor.insert(0, record[4])
        average_editor.insert(0, record[5])

    edit_btn = Button(editor, text="Lưu bản ghi", command=cap_nhat)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

def cap_nhat(f_id_editor):
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    record_id = f_id_editor.get()

    c.execute("""UPDATE students SET
           first_name = :first,
           last_name = :last,
           class = :classes,
           entry_year = :entry_year,
           average = :average,
           WHERE id = :id""",
              {
                  'first': f_name_editor.get(),
                  'last': l_name_editor.get(),
                  'class': classes_editor.get(),
                  'entry': en_year_editor.get(),
                  'average': average_editor.get(),
                  'id': record_id
              })

    conn.commit()
    conn.close()
    editor.destroy()

    # Cập nhật lại danh sách bản ghi sau khi chỉnh sửa
    truy_van()


# Khung cho các ô nhập liệu
input_frame = Frame(root)
input_frame.pack(pady=10)

# Các ô nhập liệu cho cửa sổ chính
stu_id = Entry(input_frame, width=30)
stu_id.grid(row=0, column=1)
f_name = Entry(input_frame, width=30)
f_name.grid(row=1, column=1, padx=20, pady=(10, 0))
l_name = Entry(input_frame, width=30)
l_name.grid(row=2, column=1)
classes = Entry(input_frame, width=30)
classes.grid(row=3, column=1)
en_year = Entry(input_frame, width=30)
en_year.grid(row=4, column=1)
average = Entry(input_frame, width=30)
average.grid(row=5, column=1)

# Các nhãn
stu_id_label = Label(input_frame, text="Mã sinh viên")
stu_id_label.grid(row=0, column=0)
f_name_label = Label(input_frame, text="Họ")
f_name_label.grid(row=1, column=0, pady=(10, 0))
l_name_label = Label(input_frame, text="Tên")
l_name_label.grid(row=2, column=0)
classes_label = Label(input_frame, text="Mã lớp")
classes_label.grid(row=3, column=0)
en_year_label = Label(input_frame, text="Năm nhập học")
en_year_label.grid(row=4, column=0)
average_label = Label(input_frame, text="Điểm trung bình")
average_label.grid(row=5, column=0)

# Khung cho các nút chức năng
button_frame = Frame(root)
button_frame.pack(pady=10)

# Các nút chức năng
submit_btn = Button(button_frame, text="Thêm bản ghi", command=them)
submit_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(button_frame, text="Hiển thị bản ghi", command=truy_van)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
delete_box_label = Label(button_frame, text="Chọn mã sinh viên")
delete_box_label.grid(row=2, column=0, pady=5)
delete_box = Entry(button_frame, width=30)
delete_box.grid(row=2, column=1, pady=5)
delete_btn = Button(button_frame, text="Xóa bản ghi", command=xoa)
delete_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=136)
edit_btn = Button(button_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Khung cho Treeview
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Treeview để hiển thị bản ghi
columns = ("Mã sinh viên", "Họ", "Tên")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
for column in columns:
    tree.column(column, anchor=CENTER) # This will center text in rows
    tree.heading(column, text=column)
tree.pack()

# Định nghĩa tiêu đề cho các cột
for col in columns:
    tree.heading(col, text=col)

# Gọi hàm truy vấn để hiển thị bản ghi khi khởi động
truy_van()

root.mainloop()