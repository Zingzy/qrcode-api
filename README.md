# QR Code Generator API 🚀

This API is a simple Flask application that generates QR codes. It provides two endpoints for generating QR codes with different styles: `simple` and `radial`.

<details>

<summary><strong>Table of Contents</strong></summary>

- [Getting Started](#getting-started-%EF%B8%8F)
  - [Prerequisites](#prerequisites-)
  - [Running the API](#running-the-api-)
- [Endpoints](#endpoints-)
  - [Simple QR Code](#simple-qr-code-)
  - [Radial QR Code](#radial-qr-code-)
- [Additional Endpoints](#additional-endpoints-)
  - [Health Check](#health-check-)
  - [Index](#index-)

</details>

## Getting Started 🛠️

To get started with the API, follow the instructions below:

### Prerequisites 📋

Make sure you have the following dependencies installed:

* Python 3
  
* Flask
  
* Flask-Caching
  
* Flask-CORS
  
* qrcode
  
* pillow
  

You can install these dependencies using the following command:

    pip install -r requirements.txt

### Running the API 🏃

To run the API, execute the following command:

1. Clone the repository:

    git clone https://github.com/Zingzy/qrcode-generator-api.git

2. Change directory to the repository:

    cd your-repo

3. Run the Flask API:

    python app.py

The API will be accessible at http://localhost:8080.

---

# Endpoints 🚦

1. ### Simple QR Code 📎
  

**Endpoint:** `/simple`

**Method:** `GET` or `POST`

**Parameters:**

* `url` (required): The URL or text to encode into the QR code.
  
* `fill` (optional): The fill color of the QR code (default: black).
  
* `back` (optional): The background color of the QR code (default: white).
  

**Example:**

    curl -X GET "http://localhost:8080/simple?url=https://www.google.com&fill=red&back=yellow --output simple_qr.png"

2. ### Radial QR Code 🎨
  

**Endpoint:** `/radial`

**Method:** `GET` or `POST`

**Parameters:**

* `url` (required): The URL or text to encode into the QR code.
  
* `back` (optional): The background color of the QR code (default: white).
  
* `gradient1` (optional): The first color of the radial gradient in RGB format only (default: (106,26,76))
  
* `gradient2` (optional): The second color of the radial gradient in RGB format only (default: (64,53,60))
  

**Example:**

    curl -X POST "http://localhost:8080/radial?url=https://example.com&gradient1=(255,0,0)&gradient2=(0,0,255)&back=(255,255,255)" --output radial_qr.png

---

## Additional Endpoints 🌐

1. ### Health Check 🩺
  

**Endpoint:** `/health`

**Method:** `GET` or `POST`

**Response:**

    {
        "status": "OK"
    }

2. ### Index 📃
  

**Endpoint:** `/`

**Method:** `GET`

**Response:** : The response is an HTML page wherer you can generate qr codes.

---

⭕ **Note:** This README assumes that the API is running on the default host (0.0.0.0) and port (8080). Update the base URL accordingly if you choose to run the API on a different host or port.
