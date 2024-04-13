from PIL import Image

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
    print("Dữ liệu đã trích xuất từ ảnh:")
    print(text)

# Ví dụ sử dụng
image_path = "avatar.png"  # Đường dẫn đến ảnh bạn muốn giấu dữ liệu
text_to_hide = "Quỳnh đần"
hide_text_in_image(image_path, text_to_hide)

# Trích xuất dữ liệu từ ảnh đã giấu
hidden_image_path = "avatar.png"  # Đường dẫn đến ảnh đã giấu dữ liệu
retrieve_text_from_image(hidden_image_path)
