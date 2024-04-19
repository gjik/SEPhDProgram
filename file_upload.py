from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
import os

app = Starlette(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
async def upload_file(request: Request):
    form = await request.form()
    if 'file' not in form:
        return JSONResponse({'error': 'No file part'}, status_code=400)
    
    file = form['file']
    if file.filename == '':
        return JSONResponse({'error': 'No selected file'}, status_code=400)
    
    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        contents = await file.read()
        with open(filename, 'wb') as f:
            f.write(contents)
        return JSONResponse({'message': 'File uploaded successfully', 'file_path': filename}, status_code=200)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
