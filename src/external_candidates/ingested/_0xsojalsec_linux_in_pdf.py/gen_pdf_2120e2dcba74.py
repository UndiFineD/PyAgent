# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-linux-in-pdf\gen_pdf.py
import sys

from pdfrw import PdfWriter
from pdfrw.objects.pdfarray import PdfArray
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfstring import PdfString


def create_script(js):
    action = PdfDict()
    action.S = PdfName.JavaScript
    action.JS = "try {" + js + "} catch (e) {app.alert(e.stack || e)}"
    return action


def create_page(width, height):
    page = PdfDict()
    page.Type = PdfName.Page
    page.MediaBox = PdfArray([0, 0, width, height])

    page.Resources = PdfDict()
    page.Resources.Font = PdfDict()
    page.Resources.Font.F1 = PdfDict()
    page.Resources.Font.F1.Type = PdfName.Font
    page.Resources.Font.F1.Subtype = PdfName.Type1
    page.Resources.Font.F1.BaseFont = PdfName.Courier

    return page


def create_field(name, x, y, width, height, value="", f_type=PdfName.Tx):
    annotation = PdfDict()
    annotation.Type = PdfName.Annot
    annotation.Subtype = PdfName.Widget
    annotation.FT = f_type
    annotation.Ff = 2
    annotation.Rect = PdfArray([x, y, x + width, y + height])
    annotation.T = PdfString.encode(name)
    annotation.V = PdfString.encode(value)

    annotation.BS = PdfDict()
    annotation.BS.W = 0

    appearance = PdfDict()
    appearance.Type = PdfName.XObject
    appearance.SubType = PdfName.Form
    appearance.FormType = 1
    appearance.BBox = PdfArray([0, 0, width, height])
    appearance.Matrix = PdfArray([1.0, 0.0, 0.0, 1.0, 0.0, 0.0])

    return annotation


def create_text(x, y, size, txt):
    return f"""
  BT
  /F1 {size} Tf
  {x} {y} Td ({txt}) Tj
  ET
  """


def create_button(name, x, y, width, height, value):
    button = create_field(name, x, y, width, height, f_type=PdfName.Btn)
    button.AA = PdfDict()
    button.Ff = 65536
    button.MK = PdfDict()
    button.MK.BG = PdfArray([0.90])
    button.MK.CA = value
    return button


def create_key_buttons(keys_info):
    buttons = []
    for info in keys_info:
        key = info["key"]
        name = "button_" + key
        value = info.get("value") or key
        button = create_button(
            name, info["x"], info["y"], info["width"], info["height"], value
        )
        button.AA = PdfDict()
        if info.get("toggle"):
            button.AA.D = create_script(f"button_toggle('{key}')")
        else:
            button.AA.D = create_script(f"button_down('{key}')")
            button.AA.U = create_script(f"button_up('{key}')")

        buttons.append(button)
    return buttons


def create_keys_row(keys, x, y, width, height, gap):
    buttons = []
    for i, key in enumerate(keys):
        name = "button_" + key
        new_x = x + i * (width + gap)
        button = create_button(name, new_x, y, width, height, key.upper())
        button.AA = PdfDict()
        if key == "'":
            key = "\\'"
        button.AA.D = create_script(f"button_down('{key}')")
        button.AA.U = create_script(f"button_up('{key}')")
        buttons.append(button)
    return buttons


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        js = f.read()

    width = 360
    height = 200
    scale = 2

    writer = PdfWriter()
    page = create_page(width * scale - 8, height * scale + 220)
    page.AA = PdfDict()
    page.AA.O = create_script(js)

    fields = []
    for i in range(0, height):
        field = create_field(
            f"field_{i}", 0, i * scale + 220, width * scale - 8, scale, ""
        )
        fields.append(field)
    for i in range(0, 25):
        field = create_field(f"console_{i}", 8, 8 + i * 8, 200, 8, "")
        fields.append(field)

    fields.append(create_field("speed_indicator", 582, 170, 97, 12, "Loading..."))
    fields.append(create_field("key_status", 220, 50, 200, 12, "Pressed:"))
    input_field = create_field(
        f"key_input", 500, 50, 179, 12, "Type here for keyboard inputs."
    )
    input_field.AA = PdfDict()
    input_field.AA.K = create_script("key_pressed(event.change)")
    fields.append(input_field)

    fields += create_key_buttons(
        [
            dict(key="Esc", x=220, y=170, width=20, height=12),
            dict(key="`", x=220, y=148, width=12, height=16),
            dict(key="Backspace", value="<----", x=550, y=148, width=50, height=16),
            dict(key="Tab", x=220, y=128, width=24, height=16),
            dict(key="\\", x=562, y=128, width=38, height=16),
            dict(key="CapsLock", value="Caps", x=220, y=108, width=30, height=16),
            dict(key="Enter", x=542, y=108, width=58, height=16),
            dict(key="Shift", x=220, y=88, width=44, height=16, toggle=True),
            dict(key="RShift", x=530, y=88, width=70, height=16),
            dict(key="Ctrl", x=220, y=68, width=36, height=16, toggle=True),
            dict(key="Alt", x=260, y=68, width=36, height=16, toggle=True),
            dict(key="Space", x=300, y=68, width=174, height=16),
            dict(
                key="RAlt", value="Alt", x=480, y=68, width=36, height=16, toggle=True
            ),
            dict(key="ContextMenu", value="Menu", x=522, y=68, width=36, height=16),
            dict(
                key="RCtrl", value="Ctrl", x=564, y=68, width=36, height=16, toggle=True
            ),
            dict(key="Home", x=608, y=148, width=32, height=16),
            dict(key="Insert", value="Ins", x=608, y=128, width=32, height=16),
            dict(key="Delete", value="Del", x=608, y=108, width=32, height=16),
            dict(key="End", x=646, y=148, width=32, height=16),
            dict(key="PgUp", x=646, y=128, width=32, height=16),
            dict(key="PgDn", x=646, y=108, width=32, height=16),
            dict(key="ArrowUp", value="^", x=633, y=88, width=20, height=16),
            dict(key="ArrowLeft", value="<", x=608, y=68, width=20, height=16),
            dict(key="ArrowDown", value="v", x=633, y=68, width=20, height=16),
            dict(key="ArrowRight", value=">", x=658, y=68, width=20, height=16),
        ]
    )
    fields += create_keys_row([f"F{i}" for i in range(1, 13)], 246, 170, 22, 12, 6)
    fields += create_keys_row("1234567890-=", 238, 148, 20, 16, 6)
    fields += create_keys_row("qwertyuiop[]", 250, 128, 20, 16, 6)
    fields += create_keys_row("asdfghjkl;'", 256, 108, 20, 16, 6)
    fields += create_keys_row("zxcvbnm,./", 270, 88, 20, 16, 6)

    page.Contents = PdfDict()
    page.Contents.stream = "\n".join(
        [
            create_text(220, 190, 24, "LinuxPDF"),
            create_text(
                220, 22, 8, "Source code: https://github.com/ading2210/linuxpdf"
            ),
            create_text(
                220, 10, 8, "Note: This PDF only works in Chromium-based browsers."
            ),
            create_text(520, 22, 8, "To send keystrokes to the VM, use the"),
            create_text(520, 10, 8, "buttons or type in the box above."),
            create_text(220, 36, 8, "=" * 100),
        ]
    )

    page.Annots = PdfArray(fields)
    writer.addpage(page)
    writer.write(sys.argv[2])
