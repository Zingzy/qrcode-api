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
    try {
        // Remove previous download link
        document.body.removeChild(document.querySelector(".qr-download-link"));
    } catch (error) {
        // Do nothing
    }

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
            document.getElementById("gradient-color-input").value || "#758156",
        ),
    );
    var gradient2Color = encodeURIComponent(
        getRgbFormat(
            document.getElementById("gradient2-color-input").value || "#67AF26",
        ),
    );

    var apiUrl;

    if (qrType === "simple") {
        apiUrl = `https://qrcode.jinxed.cf/simple?url=${encodeURIComponent(
            userInput,
        )}&fill=${fillColor}&back=${bgColor}`;
    } else {
        apiUrl = `https://qrcode.jinxed.cf/radial?url=${encodeURIComponent(
            userInput,
        )}&gradient1=${gradientColor}&gradient2=${gradient2Color}`;
    }

    // Clear previous QR code
    // document.getElementById("qr-code").innerHTML = "";
    var qrCodeContainer = document.getElementById("qr-code");
    qrCodeContainer.innerHTML = "";

    // Create QR code image element
    var qrCodeImage = document.createElement("img");
    qrCodeImage.src = apiUrl;

    // Hide loading spinner once the image is loaded
    qrCodeImage.onload = function () {
        qrCodeImage.id = "qr-img";
        document.getElementById("loading-spinner").style.display = "none";
        document.documentElement.scrollTop = document.documentElement.scrollHeight;

        var downloadElement = document.createElement("div");
        downloadElement.innerText = "Download";
        downloadElement.id = "download-link";
        downloadElement.style.display = "none";
        downloadElement.style.position = "absolute";

        var width = document.getElementById("qr-img").width;
        var height = document.getElementById("qr-img").height;
        downloadElement.style.width = width-1 + "px";
        downloadElement.style.height = height-1 + "px";

        downloadElement.style.backgroundColor = "rgba(255, 255, 255, 0.125)";
        downloadElement.style.borderRadius = "15px";
        downloadElement.style.color = "Black";
        downloadElement.style.fontSize = "30px";
        downloadElement.style.fontWeight = "bold";
        downloadElement.style.textAlign = "center";
        downloadElement.style.lineHeight = height + "px";
        downloadElement.style.cursor = "pointer";
        downloadElement.style.backdropFilter = "blur(10px)";
        downloadElement.style.transition = "all 0.3s ease-in-out";

        var link = document.createElement("a");
        link.classList.add("qr-download-link");

        var xhr = new XMLHttpRequest();
        xhr.responseType = "blob";
        xhr.onload = function () {
            var reader = new FileReader();
            reader.onloadend = function () {
                var dataURL = reader.result;
                link.href = dataURL;
            };
            reader.readAsDataURL(xhr.response);
        };
        xhr.open("GET", apiUrl);
        xhr.send();

        link.download = "qrcode.png";
        document.body.appendChild(link);

        // Show "Download" element on hover
        qrCodeContainer.addEventListener("mouseover", function () {
            downloadElement.style.display = "block";
        });

        // Hide "Download" element when not hovering
        qrCodeContainer.addEventListener("mouseout", function () {
            downloadElement.style.display = "none";
        });

        // Trigger download on click
        downloadElement.addEventListener("click", function () {
            downloadQRCode();
        });

        // Append QR code image and "Download" element to the container
        qrCodeContainer.appendChild(qrCodeImage);
        qrCodeContainer.appendChild(downloadElement);
    };

    // Append QR code image to the #qr-code div
    document.getElementById("qr-code").appendChild(qrCodeImage);
}

function downloadQRCode() {
    link = document.querySelector(".qr-download-link");
    link.click();
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
