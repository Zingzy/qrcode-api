function toggleColorOptions() {
    var qrType = document.getElementById("qr-type").value;

    // Hide all color options
    document.getElementById("fill-color").style.display = "none";
    document.getElementById("background-color").style.display = "none";
    document.getElementById("gradient-color").style.display = "none";
    document.getElementById("gradient2-color").style.display = "none";

    // Show relevant color options based on QR code type
    if (qrType === "simple") {
        document.getElementById("fill-color").style.display = "flex";
        document.getElementById("background-color").style.display = "flex";
    } else if (qrType === "radial") {
        document.getElementById("gradient-color").style.display = "flex";
        document.getElementById("gradient2-color").style.display = "flex";
    }
}

// Call the function on page load to set the initial state
toggleColorOptions();

function generateQRCode() {
    // Display loading spinner
    document.getElementById("loading-spinner").style.display = "flex";

    var userInput = document.getElementById("qr-input").value;
    var qrType = document.getElementById("qr-type").value;
    var fillColor = encodeURIComponent(
        document.getElementById("fill-color-input").value || "#000000",
    );
    var bgColor = encodeURIComponent(
        document.getElementById("background-color-input").value || "#ffffff",
    );
    var gradientColor = encodeURIComponent(
        getRgbFormat(
            document.getElementById("gradient-color-input").value || "#6a1a4c",
        ),
    );
    var gradient2Color = encodeURIComponent(
        getRgbFormat(
            document.getElementById("gradient2-color-input").value || "#40353c",
        ),
    );

    var apiUrl;

    if (qrType === "simple") {
        apiUrl = `https://jinxedqrcode.forcc1.repl.co/simple?url=${encodeURIComponent(
            userInput,
        )}&fill=${fillColor}&back=${bgColor}`;
    } else {
        apiUrl = `https://jinxedqrcode.forcc1.repl.co/radial?url=${encodeURIComponent(
            userInput,
        )}&gradient1=${gradientColor}&gradient2=${gradient2Color}`;
    }

    // Clear previous QR code
    document.getElementById("qr-code").innerHTML = "";

    // Create QR code image element
    var qrCodeImage = document.createElement("img");
    qrCodeImage.src = apiUrl;

    // Hide loading spinner once the image is loaded
    qrCodeImage.onload = function () {
        document.getElementById("loading-spinner").style.display = "none";
    };

    // Append QR code image to the #qr-code div
    document.getElementById("qr-code").appendChild(qrCodeImage);
}

function getRgbFormat(hexColor) {
    var shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    hexColor = hexColor.replace(shorthandRegex, function (m, r, g, b) {
        return r + r + g + g + b + b;
    });

    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hexColor);
    var rgbFormat = result
        ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16),
        }
        : null;

    return rgbFormat ? `(${rgbFormat.r}, ${rgbFormat.g}, ${rgbFormat.b})` : null;
}
