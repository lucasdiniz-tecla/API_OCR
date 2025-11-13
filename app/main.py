import os
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pytesseract import pytesseract


TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR\tessdata"
POPPLER_PATH = r"C:\Poppler\poppler-25.07.0\Library\bin"


pytesseract.tesseract_cmd = TESSERACT_CMD
os.environ["TESSDATA_PREFIX"] = TESSDATA_PREFIX
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Tesseract-OCR"

app = FastAPI(
    title="PDF OCR Webhook",
    description="Endpoint para receber um PDF via webhook e extrair o texto via Tesseract OCR.",
)

def perform_ocr_on_pdf(file_path: str, lang: str = 'por') -> str:
    import pytesseract
    from pdf2image import convert_from_path


    try:
        paginas = convert_from_path(
            file_path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )


        pagina = paginas[0]


        texto_extraido = pytesseract.image_to_string(
            pagina,
            lang=lang,
            config="--psm 6 --dpi 300"
        )


        return texto_extraido.strip()

    except Exception as e:
        return f"Erro durante o OCR: {e}"



@app.post("/webhook/ocr")
async def handle_ocr_webhook(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF (application/pdf).")

    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)

    try:
        with open(temp_file_path, "wb") as buffer:

            content = await file.read()
            buffer.write(content)

        extracted_text = perform_ocr_on_pdf(temp_file_path)

        return {
            "status": "success",
            "filename": file.filename,
            "extracted_text": extracted_text
        }

    finally:
        shutil.rmtree(temp_dir)
        print(f"Arquivo temporário {temp_file_path} excluído.")


