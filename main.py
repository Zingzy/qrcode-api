from flask import Flask, request, jsonify, send_file, render_template
import base64
import qrcode
from qrcode.image.styles.moduledrawers.pil import (
    RoundedModuleDrawer,
    HorizontalBarsDrawer,
    CircleModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
    GappedSquareModuleDrawer,
)
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import (
    RadialGradiantColorMask,
    SquareGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask,
    ImageColorMask,
    SolidFillColorMask,
)
import io
import sys
import urllib.parse
# from flask_caching import Cache
from flask_cors import CORS
from utils import *
import json

# config = {"DEBUG": True, "CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}

app = Flask(__name__)
CORS(app)

# app.config.from_mapping(config)
# cache = Cache(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/health", methods=["GET", "POST"])
def heath():
    return jsonify({"status": "ok"})


@app.route("/classic", methods=["POST", "GET"])
def generate_simple_qr():
    text = request.values.get("text")
    fill = request.values.get("fill", "black")
    back = request.values.get("back", "white")
    size = request.values.get("size", None)
    data_format = request.values.get("format", None)
    formatting_dict = request.values.get("formattings", None)

    if not text and not data_format:
        return jsonify({"error": "Text parameter is missing"}), 400

    if data_format:
        if not formatting_dict:
            return jsonify({"error": "Formattings parameter is missing"}), 400

        try:
            formatting_dict = urllib.parse.unquote(formatting_dict).strip()
            formatting_dict = json.loads(formatting_dict)
        except Exception as e:
            print(e, file=sys.stdout)
            return jsonify({"error": "Invalid formatting Input"}), 400

        if data_format.lower() in prefix_maps.keys():
            try:
                text = prefix_maps[data_format.lower()](**formatting_dict)
                print(text)
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        else:
            return jsonify({"error": "Invalid data format"}), 400

    if size:
        try:
            size = int(size)
            if size > 1000:
                return jsonify({"error": "Size is too large"}), 400
            if size < 10:
                return jsonify({"error": "Size is too small"}), 400
        except:
            return jsonify({"error": "Invalid size"}), 400

    if not data_format or not formatting_dict:
        try:
            text = urllib.parse.unquote(text).strip()
        except:
            return jsonify({"error": "Invalid text Input"}), 400

    fill_color = urllib.parse.unquote(fill)
    back_color = urllib.parse.unquote(back)

    try:
        fill_color_rgb = parse_color(fill_color)
        back_color_rgb = parse_color(back_color)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if fill_color_rgb == "transparent":
        fill_color_rgb = (0, 0, 0)

    version = suggest_qr_version(text)
    box_size = suggest_box_size(text)

    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    try:
        qr_image = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask= SolidFillColorMask(back_color_rgb, fill_color_rgb),
        )
    except Exception as e:
        return jsonify({"error": f"Error generating QR code: {str(e)}"}), 500

    if size:
        qr_image = qr_image.resize((size, size), resample=0)

    # Stream the image directly to the response
    image_stream = io.BytesIO()
    qr_image.save(image_stream, format="PNG")
    image_stream.seek(0)

    return send_file(image_stream, mimetype="image/png")


@app.route("/gradient", methods=["POST", "GET"])
def generate_raidal_qr():
    text = request.values.get("text")
    gradient1 = request.values.get("gradient1", "(106,26,76)")
    gradient2 = request.values.get("gradient2", "(64,53,60)")
    back_color = request.values.get("back", "(255, 255, 255)")
    size = request.values.get("size", None)
    data_format = request.values.get("format", None)
    formatting_dict = request.values.get("formattings", None)

    if not text and not data_format:
        return jsonify({"error": "Text parameter is missing"}), 400

    if data_format:
        if not formatting_dict:
            return jsonify({"error": "Formattings parameter is missing"}), 400

        try:
            formatting_dict = urllib.parse.unquote(formatting_dict).strip()
            formatting_dict = json.loads(formatting_dict)
        except Exception as e:
            print(e, file=sys.stdout)
            return jsonify({"error": "Invalid formatting Input"}), 400

        if data_format.lower() in prefix_maps.keys():
            try:
                text = prefix_maps[data_format.lower()](**formatting_dict)
                print(text)
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        else:
            return jsonify({"error": "Invalid data format"}), 400

    if size:
        try:
            size = int(size)
            if size > 1000:
                return jsonify({"error": "Size is too large"}), 400
            if size < 10:
                return jsonify({"error": "Size is too small"}), 400
        except:
            return jsonify({"error": "Invalid size"}), 400

    if not data_format or not formatting_dict:
        try:
            text = urllib.parse.unquote(text).strip()
        except:
            return jsonify({"error": "Invalid text Input"}), 400

    try:
        text = urllib.parse.unquote(text).strip()
        gradient1 = urllib.parse.unquote(gradient1).strip()
        gradient2 = urllib.parse.unquote(gradient2).strip()
        back_color = urllib.parse.unquote(back_color).strip()
    except:
        return jsonify({"error": "Invalid text Input"}), 400

    try:
        gradient1 = parse_color(gradient1)
        gradient2 = parse_color(gradient2)
        back_color = parse_color(back_color)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    version = suggest_qr_version(text)
    box_size = suggest_box_size(text)

    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    try:
        qr_image = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=SquareModuleDrawer(),
            color_mask=VerticalGradiantColorMask(back_color, gradient1, gradient2),
        )
    except Exception as e:
        return jsonify({"error": f"Error generating QR code: {str(e)}"}), 500

    if size:
        qr_image = qr_image.resize((size, size), resample=0)

    image_stream = io.BytesIO()
    qr_image.save(image_stream, format="PNG")
    image_stream.seek(0)

    return send_file(image_stream, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080, use_reloader=True)
