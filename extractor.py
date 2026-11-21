
from pathlib import Path
from PIL import Image, ExifTags
from pypdf import PdfReader
from docx import Document


def extract_image_metadata(file_path):
    file_path = Path(file_path)
    metadata = {}

    with Image.open(file_path) as image:
        metadata["File Name"] = file_path.name
        metadata["Format"] = image.format
        metadata["Width"] = image.width
        metadata["Height"] = image.height

        exif = image.getexif()

        # Extract readable EXIF fields
        for tag_id, value in exif.items():
            tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))

            # GPS metadata is decoded separately below
            if tag_name == "GPSInfo":
                continue

            metadata[tag_name] = str(value)

        # Decode GPS IFD information
        try:
            gps_ifd = exif.get_ifd(0x8825)
        except (KeyError, TypeError, ValueError):
            gps_ifd = {}

        if gps_ifd:
            gps_tags = {}

            for tag_id, value in gps_ifd.items():
                tag_name = ExifTags.GPSTAGS.get(
                    tag_id, str(tag_id)
                )
                gps_tags[tag_name] = value

            metadata["GPSInfo"] = str(gps_tags)

            # Extract individual GPS fields
            for field in ["GPSLatitude", "GPSLongitude"]:
                if field in gps_tags:
                    metadata[field] = str(gps_tags[field])

    return metadata


def extract_pdf_metadata(file_path):
    metadata = {}

    reader = PdfReader(file_path)

    metadata["File Name"] = Path(file_path).name
    metadata["Format"] = "PDF"
    metadata["Pages"] = len(reader.pages)

    if reader.metadata:
        for key, value in reader.metadata.items():
            metadata[str(key)] = str(value)

    return metadata


def extract_docx_metadata(file_path):
    metadata = {}

    document = Document(file_path)
    properties = document.core_properties

    metadata["File Name"] = Path(file_path).name
    metadata["Format"] = "DOCX"

    fields = {
        "Author": properties.author,
        "Title": properties.title,
        "Subject": properties.subject,
        "Keywords": properties.keywords,
        "Last Modified By": properties.last_modified_by,
        "Created": properties.created,
        "Modified": properties.modified,
        "Revision": properties.revision
    }

    for key, value in fields.items():
        if value is not None and value != "":
            metadata[key] = str(value)

    return metadata

