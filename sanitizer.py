
from pathlib import Path
from PIL import Image
from datetime import datetime
from pypdf import PdfReader, PdfWriter
from docx import Document


def sanitize_image(file_path):
    file_path = Path(file_path)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / (
        file_path.stem + "_clean" + file_path.suffix
    )

    with Image.open(file_path) as image:
        image.load()

        # Rebuild a new image using pixel data only
        clean_image = Image.new(image.mode, image.size)
        clean_image.putdata(list(image.getdata()))

        clean_image.save(output_path)

    return output_path


def sanitize_pdf(file_path):
    file_path = Path(file_path)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / (
        file_path.stem + "_clean.pdf"
    )

    if output_path.exists():
        raise FileExistsError(
            "Cleaned PDF already exists. "
            "Move or rename it before sanitizing again."
        )

    reader = PdfReader(file_path)

    if reader.is_encrypted:
        raise ValueError(
            "Encrypted PDFs are not supported."
        )

    writer = PdfWriter()

    # Copy pages without copying the source
    # document-level metadata dictionary
    writer.append_pages_from_reader(reader)

    writer.write(output_path)

    return output_path


def sanitize_docx(file_path):
    file_path = Path(file_path)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / (
        file_path.stem + "_clean.docx"
    )

    if output_path.exists():
        raise FileExistsError(
            "Cleaned DOCX already exists. "
            "Move or rename it before sanitizing again."
        )

    document = Document(file_path)
    properties = document.core_properties

    # Clear identifying core properties
    properties.author = ""
    properties.last_modified_by = ""
    properties.title = ""
    properties.subject = ""
    properties.keywords = ""
    properties.comments = ""
    properties.category = ""
    properties.content_status = ""
    properties.identifier = ""
    properties.language = ""
    properties.version = ""

    # Replace existing dates with a neutral date
    neutral_date = datetime(2000, 1, 1)

    if properties.created is not None:
        properties.created = neutral_date

    if properties.modified is not None:
        properties.modified = neutral_date

    if properties.last_printed is not None:
        properties.last_printed = neutral_date

    properties.revision = 1

    document.save(output_path)

    return output_path
