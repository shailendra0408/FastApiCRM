from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse 
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import csv
import io


app = FastAPI()

# configure CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_index():
    return FileResponse('LandingPage_1.html')

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    #print('File contents:', contents)
    print('File name:', file.filename)
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    insights = {
        'coloum_name': list(df.columns), 
        'num_row' : len(df)   
    }
    # Process CSV file contents
    return {'message': 'File uploaded and processed successfully', 'insights':insights}

    

@app.route('/upload-csv', methods=['GET'])
async def upload_csv_form():
    return '''
        <html>
            <body>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file"><br><br>
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>
    '''


