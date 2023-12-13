import qrcode.constants
from datetime import datetime, timedelta

named_colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42),
    "gray": (128, 128, 128),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "transparent": "transparent",  # Special case for transparent
}

def parse_color(color_str):

    try:
        # Check if color_str is a named color
        if color_str.lower() in named_colors:
            return named_colors[color_str.lower()]

        if color_str.startswith("#"):
            # Hex color
            color_str = color_str.lstrip("#")
            if len(color_str) == 6:
                return tuple(int(color_str[i : i + 2], 16) for i in (0, 2, 4))
            else:
                raise ValueError("Invalid hex color format")
        elif color_str.startswith("rgb(") and color_str.endswith(")"):
            # RGB color
            color_str = color_str[4:-1]
            rgb_values = [int(x.strip()) for x in color_str.split(",")]
            if len(rgb_values) == 3:
                return tuple(rgb_values)
            else:
                raise ValueError("Invalid RGB color format")
        elif color_str.startswith("(") and color_str.endswith(")"):
            # RGB color without 'rgb' prefix
            color_str = color_str[1:-1]
            rgb_values = [int(x.strip()) for x in color_str.split(",")]
            if len(rgb_values) == 3:
                return tuple(rgb_values)
            else:
                raise ValueError("Invalid RGB color format")
        else:
            # Assume hex color if no prefix is present
            if len(color_str) == 6:
                return tuple(int(color_str[i : i + 2], 16) for i in (0, 2, 4))
            else:
                raise ValueError("Invalid color format")
    except ValueError:
        raise ValueError(f"Invalid color format: {color_str}")


def suggest_qr_version(data, error_correction=qrcode.constants.ERROR_CORRECT_L):
    # Define the maximum data capacity for each version and error correction level
    max_capacity = [
        [41, 77, 127, 187, 255, 322, 370, 461, 552, 652, 772, 883, 1022, 1101, 1250, 1408],
        [34, 63, 101, 149, 202, 255, 293, 365, 432, 513, 604, 691, 796, 871, 991, 1082],
        [27, 48, 77, 111, 144, 178, 206, 258, 308, 370, 438, 506, 586, 644, 718, 808],
        [17, 34, 58, 82, 106, 139, 154, 202, 235, 288, 331, 374, 427, 468, 530, 602]
    ]

    # Find the minimum version that can accommodate the data length
    for version, capacities in enumerate(max_capacity):
        if len(data) <= capacities[error_correction]:
            return version + 1  # Versions are 1-indexed

    # If data is too large for the maximum version, return the highest version
    return len(max_capacity)


def suggest_box_size(data, border_fraction=0.5):
    # Constants for module size and border default
    box_size_factor = 50

    # Calculate the recommended box size based on the version
    recommended_box_size = max(len(data) // box_size_factor, 10)

    # Return the recommended sizes
    return recommended_box_size


def format_contact(name, phone, email=None, address=None, company=None, website=None, **kwargs):
    # Format the contact data according to the vCard specification
    contact_data = f'BEGIN:VCARD\nVERSION:3.0\nFN:{name}\n'  # Full name
    contact_data += f'ORG:{company}\n' if company else "" # Organization
    contact_data += f'ADR:;;{address};;;;\n' if address else "" # Address
    contact_data += f'TEL;TYPE=work,voice;VALUE=uri:tel:{phone}\n'  # Phone
    contact_data += f'EMAIL;TYPE=INTERNET;TYPE=WORK;TYPE=PREF:{email}\n' if email else ""  # Email
    contact_data += f"URL;TYPE=Homepage:{website}" if website else ""
    contact_data += 'END:VCARD'  # End of contact entry

    return contact_data

def format_event(title, start=None, end=None, location=None, description=None, **kwargs):

    event_data = f'BEGIN:VEVENT\nSUMMARY:{title}\n'  # Title
    try:
        start = start.strftime('%Y%m%dT%H%M%SZ')
        end = end.strftime('%Y%m%dT%H%M%SZ')
    except:
        start = end = ""

    if start:
        event_data += f'DTSTART:{start}\n'  # Start time
    if end:
        event_data += f'DTEND:{end}\n'  # End time
    if location:
        event_data += f'LOCATION:{location}\n'  # Location
    if description:
        event_data += f'DESCRIPTION:{description}\n'  # Description
    event_data += 'END:VEVENT'  # End of event entry

    return event_data

def format_bookmark(title, url, **kwargs):
    data_bookmark = f"MEBKM:URL:{url};TITLE:{title};;"
    return data_bookmark

def format_wifi(ssid, password=None, **kwargs):
    if password:
        wifi_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    else:
        wifi_data = f"WIFI:T:nopass;S:{ssid};;"
    return wifi_data

def format_bitcoin(address, amount, message=None, **kwargs):
    bitcoin_data = f"bitcoin:{address}?amount={amount}"
    if message:
        bitcoin_data += f"&message={message}"
    return bitcoin_data

def format_location(latitude, longitude, **kwargs):
    location_data = f"geo:{latitude},{longitude}"
    return location_data

def format_sms(phone, message, **kwargs):
    phone += "+1" if not "+" in phone else ""
    sms_data = f"sms:{phone}:{message}"
    return sms_data

def format_email(email, subject, message, **kwargs):
    email_data = f"mailto:{email}?subject={subject}&body={message}"
    return email_data

def format_tel(number, **kwargs):
    number += "+1" if not number.startswith("+") else ""
    tel_data = f"tel:{number}"
    return tel_data

prefix_maps = {
    "contact": format_contact,
    "event": format_event,
    "bookmark": format_bookmark,
    "wifi": format_wifi,
    "bitcoin": format_bitcoin,
    "location": format_location,
    "sms": format_sms,
    "email": format_email,
    "tel": format_tel
}

def generate_qr_code(data=None, width=None, height=None, box_size=None, border_size=4, data_type=None, data_dict={}):
    # Calculate box size based on the length of the data

    try:
        if data_type.lower() in prefix_maps.keys():
            data = prefix_maps[data_type.lower()](**data_dict)
            print(data)
    except Exception as e:
        return ValueError(e)

    if data:
        if box_size == None:
            box_size = suggest_box_size(data)
        if border_size == None:
            border_size = 4

        version = suggest_qr_version(data)
    else:
        return None

    print(f"Box Size: {box_size}")
    print(f"Border Size: {border_size}")
    print(f"Version: {version}")

    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border_size,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    if width and height:
        img = img.resize((width, height), resample=0)

    img.show()

# data_dict={
#     "name": "John Doe",
#     "phone": "1234567890",
#     "email": "johnDoe@gmail.com",
#     "address": "1234 Main St. Anytown, USA",
#     "website": "https://www.johndoe.com",
#     "company": "John Doe Inc."}

# generate_qr_code(data="Not Needed", data_type="contact", data_dict=data_dict)

# generate_qr_code(data_type="tel", data_dict={"number":"123456789"})

# generate_qr_code(data_type="event", data_dict={
#     "title": "Event Title",
#     "start": datetime.now(),
#     "end": datetime.now() + timedelta(hours=1),
#     "location": "1234 Main St. Anytown, USA",
#     "description": "This is a description of the event"})

# generate_qr_code(data_type="bookmark", data_dict={
#     "title": "Bookmark Title",
#     "url": "https://www.google.com"})

# generate_qr_code(data_type="wifi", data_dict={
#     "ssid": "Wifi",
#     "password": "87654321"})

# generate_qr_code(data_type="bitcoin", data_dict={
#     "address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
#     "amount": 0.0001,
#     "message": "Donation for project"})

# generate_qr_code(data_type="location", data_dict={
#     "latitude": 40.7128,
#     "longitude": 74.0060})

# generate_qr_code(data_type="sms", data_dict={
#     "phone": "+1234567890",
#     "message": "Hello World!"})

# generate_qr_code(data_type="email", data_dict={
#     "email": "johndoe@gmail.com",
#     "subject": "Hello World!",
#     "message": "Hello World!"})
