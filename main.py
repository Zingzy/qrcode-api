from flask import Flask, request, jsonify, send_file, render_template
import base64
import qrcode
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import io
import sys
import urllib.parse
from flask_caching import Cache
from flask_cors import CORS

config = {"DEBUG": True, "CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}

app = Flask(__name__)
CORS(app)

app.config.from_mapping(config)
cache = Cache(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def qr(link, gradient1=(106, 26, 76), gradient2=(64, 53, 60), bg=(255, 255, 255)):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask(bg, gradient1, gradient2),
    )
    return img


def str_to_tuple_rgb(s):
    if not s.startswith("(") or not s.endswith(")"):
        return None
    s = s.strip("()")
    parts = s.split(",")
    if len(parts) != 3:
        return None
    try:
        r, g, b = map(int, parts)
    except ValueError:
        return None
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        return None

    t = eval("(" + s + ")")
    return t


@app.route("/simple", methods=["POST", "GET"])
def generate_simple_qr():
    text = request.args.get("url")
    fill_color = request.args.get("fill", "black")
    back_color = request.args.get("back", "white")

    if not text:
        return jsonify({"error": "URL parameter is missing"}), 400
    text = urllib.parse.unquote(text).strip()

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)

    image_stream = io.BytesIO()
    qr_image.save(image_stream, format="PNG")
    image_stream.seek(0)

    return send_file(image_stream, mimetype="image/png")


@app.route("/radial", methods=["POST", "GET"])
def generate_raidal_qr():
    text = request.args.get("url")
    gradient1 = request.args.get("gradient1", "(106,26,76)")
    print(gradient1, file=sys.stdout)
    gradient2 = request.args.get("gradient2", "(64,53,60)")
    print(gradient2, file=sys.stdout)
    back = request.args.get("back", "(255, 255, 255)")

    if not text:
        return jsonify({"error": "URL parameter is missing"}), 400

    text = urllib.parse.unquote(text).strip()
    gradient1 = urllib.parse.unquote(gradient1).strip()
    gradient2 = urllib.parse.unquote(gradient2).strip()

    print(gradient1, gradient2)

    if (
        str_to_tuple_rgb(gradient1)
        and str_to_tuple_rgb(gradient2)
        and str_to_tuple_rgb(back)
    ):
        print(str_to_tuple_rgb(gradient1), str_to_tuple_rgb(gradient2))
        back = (
            (1, 1, 1) if str_to_tuple_rgb(back) == (0, 0, 0) else str_to_tuple_rgb(back)
        )
        qr_image = qr(
            text, str_to_tuple_rgb(gradient1), str_to_tuple_rgb(gradient2), back
        )
    else:
        qr_image = qr(text)

    image_stream = io.BytesIO()
    qr_image.save(image_stream, format="PNG")
    image_stream.seek(0)

    return send_file(image_stream, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080, use_reloader=False)
