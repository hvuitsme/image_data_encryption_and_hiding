import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def binary_to_text(binary_string):
    """Chuyển đổi chuỗi nhị phân thành văn bản"""
    text = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        text += chr(int(byte, 2))
    return text

def text_to_binary(text):
    """Chuyển đổi văn bản thành chuỗi nhị phân"""
    binary_string = ""
    for char in text:
        binary_string += format(ord(char), '08b')
    return binary_string

def hide_text_in_image(image_path, text):
    """Giấu văn bản vào ảnh bằng phương pháp LSB"""
    img = Image.open(image_path)
    binary_text = text_to_binary(text)
    binary_text += '1111111111111110'  # Thêm dấu hiệu kết thúc tin vào cuối
    text_length = len(binary_text)

    width, height = img.size
    pixels = img.load()

    if text_length > width * height:
        raise ValueError("Kích thước dữ liệu lớn hơn kích thước của ảnh")

    index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Thay đổi bit cuối cùng của các kênh màu để giấu dữ liệu
            if index < text_length:
                r &= ~1  # Xóa bit cuối
                r |= int(binary_text[index])
                index += 1

            if index < text_length:
                g &= ~1
                g |= int(binary_text[index])
                index += 1

            if index < text_length:
                b &= ~1
                b |= int(binary_text[index])
                index += 1

            pixels[x, y] = (r, g, b)

    img.save("hidden_image.png")
    status_var.set("Đã giấu dữ liệu vào ảnh thành công!")
    print("Đã giấu dữ liệu vào ảnh thành công!")

def retrieve_text_from_image(image_path):
    """Trích xuất văn bản đã giấu từ ảnh"""
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()

    binary_text = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_text += str(r & 1)
            binary_text += str(g & 1)
            binary_text += str(b & 1)

    # Tìm dấu hiệu kết thúc tin và loại bỏ các bit thừa
    end_marker_index = binary_text.find('1111111111111110')
    binary_text = binary_text[:end_marker_index]

    text = binary_to_text(binary_text)
    status_var.set("Dữ liệu đã trích xuất từ ảnh:")
    data_var.set(text)
    print("Dữ liệu đã trích xuất từ ảnh:")
    print(text)

def browse_image():
    """Chọn một ảnh từ máy tính và hiển thị đường dẫn"""
    filename = filedialog.askopenfilename(title="Chọn ảnh", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")))
    entry_image.delete(0, tk.END)
    entry_image.insert(0, filename)
    # Hiển thị ảnh trong một góc của form
    display_image(filename)

def display_image(filename):
    """Hiển thị hình ảnh hoặc thông báo khi không có ảnh"""
    try:
        img = Image.open(filename)
        img.thumbnail((200, 200))  # Thay đổi kích thước ảnh để phù hợp với giao diện
        img = ImageTk.PhotoImage(img)
        label_image_display.config(image=img)
        label_image_display.image = img  # Giữ tham chiếu để tránh bị thu hồi bởi garbage collector
        label_image_display.config(width=200, height=200)
        label_image_display.config(text="")
    except FileNotFoundError:
        label_image_display.config(image="")
        label_image_display.image = None
        label_image_display.config(text="Không có hình ảnh")
        label_image_display.config(width=200, height=200)

def encode_and_hide():
    """Mã hoá văn bản vào ảnh và lưu ảnh đã giấu dữ liệu"""
    image_path = entry_image.get()
    text_to_hide = entry_text.get()
    hide_text_in_image(image_path, text_to_hide)

def decode_and_show():
    """Trích xuất văn bản đã giấu từ ảnh và hiển thị"""
    hidden_image_path = "hidden_image.png"  # Đường dẫn đến ảnh đã giấu dữ liệu
    retrieve_text_from_image(hidden_image_path)

# Tạo giao diện
root = tk.Tk()
root.title("Mã hoá và giấu dữ liệu trong ảnh")

left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.pack(side=tk.LEFT)

right_frame = tk.Frame(root, padx=10, pady=10)
right_frame.pack(side=tk.RIGHT)

label_status = tk.Label(left_frame, text="Trạng thái:")
label_status.grid(row=0, column=0, sticky="w")

status_var = tk.StringVar()
status_var.set("")
label_status_display = tk.Label(left_frame, textvariable=status_var)
label_status_display.grid(row=0, column=1, sticky="w")

label_image = tk.Label(left_frame, text="Đường dẫn ảnh:")
label_image.grid(row=1, column=0, sticky="w")

entry_image = tk.Entry(left_frame, width=50)
entry_image.grid(row=1, column=1)

button_browse = tk.Button(left_frame, text="Chọn ảnh", command=browse_image)
button_browse.grid(row=1, column=2)

label_text = tk.Label(left_frame, text="Văn bản cần giấu:")
label_text.grid(row=2, column=0, sticky="w")

entry_text = tk.Entry(left_frame, width=50)
entry_text.grid(row=2, column=1)

button_encode = tk.Button(left_frame, text="Mã hoá và giấu dữ liệu", command=encode_and_hide)
button_encode.grid(row=3, column=0, columnspan=3)

label_image_display = tk.Label(right_frame, width=70, height=70)
label_image_display.grid(row=0, column=0, columnspan=2, padx=40)

label_data = tk.Label(right_frame, text="Dữ liệu trích xuất:")
label_data.grid(row=1, column=0, sticky="w")

data_var = tk.StringVar()
data_var.set("")
label_data_display = tk.Label(right_frame, textvariable=data_var)
label_data_display.grid(row=1, column=1, columnspan=2)

button_decode = tk.Button(right_frame, text="Trích xuất và hiển thị dữ liệu", command=decode_and_show)
button_decode.grid(row=2, column=0, columnspan=3)

# # Thay đổi kích thước và căn giữa cửa sổ
# root.geometry("800x400+400+200")  # Thay đổi kích thước và vị trí xuất hiện của cửa sổ (width x height + x_offset + y_offset)

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Tính toán vị trí cho cửa sổ
window_width = 800
window_height = 400
x_offset = (screen_width - window_width) // 2
y_offset = (screen_height - window_height) // 2

# Thay đổi kích thước và vị trí của cửa sổ
root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

root.mainloop()
