from typing import List
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Form,
)
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/file/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/file/" enctype="multipart/form-data" method="post">
<input name="file" type="file" multiple>
<input name="fileb" type="file" multiple>
<input name="token" type="hidden" value="hogehoge">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
