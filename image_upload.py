from js import document, console, Uint8Array, window, File
from pyodide.ffi import create_proxy
import io

from PIL import Image, ImageFilter, ImageFont, ImageDraw

async def _upload_change_and_show(e):
    file_list = e.target.files
    first_item = file_list.item(0)

    array_buf = Uint8Array.new(await first_item.arrayBuffer())

    bytes_list = bytearray(array_buf)
    my_bytes = io.BytesIO(bytes_list) 

    my_image = Image.open(my_bytes)

    console.log(f"{my_image.format= } {my_image.width= } {my_image.height= }")


    font = ImageFont.truetype("Roboto-Black.ttf", 20)
    draw = ImageDraw.Draw(my_image)
    draw.text((0, 0),"Sample Text",(255,255,255), font=font)

    my_stream = io.BytesIO()
    my_image.save(my_stream, format="PNG")


    image_file = File.new([Uint8Array.new(my_stream.getvalue())], "new_image_file.png", {type: "image/png"})

    new_image = document.createElement('img')
    new_image.src = window.URL.createObjectURL(image_file)
    document.getElementById("output_upload_pillow").appendChild(new_image)

   
upload_file = create_proxy(_upload_change_and_show)
document.getElementById("file-upload-pillow").addEventListener("change", upload_file)