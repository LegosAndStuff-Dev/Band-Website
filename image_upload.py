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
    W = my_image.width
    H = my_image.height


    font_size = int(H/30)
    font_size_comp = int(60)
    font_size_event_type = font_size+5
    font_size_location = int(H/30)
    font = ImageFont.truetype("./Roboto-Black.ttf", font_size)
    fontComp = ImageFont.truetype("./Roboto-Black.ttf", font_size_comp)
    fontEventType = ImageFont.truetype("./Roboto-Black.ttf", font_size_event_type)
    draw = ImageDraw.Draw(my_image)

    text = Element("input-comp").element.value
    w, h = draw.textsize(text, fontComp)

    draw.text(((W-w)-10, 10), text, (255, 255, 255), font=fontComp)

    text = Element("input-type").element.value
    w, h = draw.textsize(text, fontEventType)

    draw.text(((W-w)-10, 5+10+font_size_comp), text, (255, 255, 255), font=fontEventType)


    spotsNotOpen = True
    i = 0

    while spotsNotOpen:
        i += 1

        if Element(f"input-{i}").element == None:
            spotsNotOpen = False
        else:
            text = Element(f"input-{i}").element.value
            w, h = draw.textsize(text, font)

            if "(red)" in text:
                text = text.removesuffix(" (red)")
                w, h = draw.textsize(text, font)
                
                draw.text(((W-w)-10, (20+font_size_comp)+(i*(font_size+5))+25), text, (165,7,7), font=font)

            else:
                draw.text(((W-w)-10, (20+font_size_comp)+(i*(font_size+5))+25), text,(255,255,255), font=font)

    x0, y0 = (365, 670)
    x1, y1 = (740, 740)

    draw.rounded_rectangle((x0, y0, x1, y1), 20, (186,210,234))
    W_rect = (x1-x0)
    H_rect = (y1-y0)

    w, h = draw.textsize("Location", font)

    draw.text((((W_rect-w)/2)+x0, (y0+5)), "Location", (16,57,109), font=font)

    fontLocation = ImageFont.truetype("./Roboto-Black.ttf", font_size_location)

    text = Element(f"input-location").element.value
    w, h = draw.textsize(text, fontLocation)

    if w > 350:
        goodSize = True

        while goodSize:
            fontLocation = ImageFont.truetype("./Roboto-Black.ttf", font_size_location)
            w, h = draw.textsize(text, fontLocation)

            if w > 350:
                font_size_location -= 1
                console.log(f"W - {w}, {font_size_location}")

            else:
                goodSize = False
                draw.text(((W_rect-w)/2+x0, (y0 + 40)), text, (16,57,109), font=fontLocation)

    else:
        draw.text(((W_rect-w)/2+x0, (y0 + 40)), text, (16,57,109), font=fontLocation)

    spotsNotOpen = True
    i = 0

    while spotsNotOpen:
        i += 1

        if Element(f"input-{i}-cap").element == None:
            spotsNotOpen = False
        else:
            text = Element(f"input-{i}-cap").element.value
            console.log(text)
            w, h = draw.textsize(text, font)

            if "Lincoln" in text:
                draw.text((10, (20+font_size_comp)+(i*(font_size+5))+25), text, (165,7,7), font=font)

            else:
                draw.text((10, (20+font_size_comp)+(i*(font_size+5))+25), text,(255,255,255), font=font)


    my_stream = io.BytesIO()
    my_image.save(my_stream, format="PNG")


    image_file = File.new([Uint8Array.new(my_stream.getvalue())], "new_image_file.png", {type: "image/png"})

    new_image = document.createElement('img')
    new_image.src = window.URL.createObjectURL(image_file)
    document.getElementById("output_upload_pillow").appendChild(new_image)

upload_file = create_proxy(_upload_change_and_show)
document.getElementById("file-upload-pillow").addEventListener("change", upload_file)