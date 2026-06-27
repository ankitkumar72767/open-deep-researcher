import easyocr

reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path):

    try:
        result = reader.readtext(
            image_path,
            detail=0
        )

        return "\n".join(result)

    except Exception as e:
        return f"OCR Error: {e}"