
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
from os.path import splitext
from nepalimodel.predict import predict_from_speech
from pydub import AudioSegment
from pythonfiles.main import get_summary_from_text_file
from pythonfiles import tokenizer
from pythonfiles import ranker
from pydantic import BaseModel




app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    
    return {"message": "Namasate"}
# endpoint for textinput
class text(BaseModel):    
    texts: str
@app.post("/input-text")
async def create_upload_text(data: text):
    with open('static/input-text/input.txt', 'w',encoding="utf-8") as f:
        f.write(data.texts)
    filepath='static/input-text/input.txt'
    summary=get_summary_from_text_file(filepath)
    return summary
        
    
    

#endpoint for fileinput-text
############################################################################################################
@app.post("/text")
async def create_upload_file(text: UploadFile = File(...)):
    ext=text.filename.split('.').pop()
    if ext == 'txt':          
        file_location = f"static/text/{text.filename}{uuid.uuid1()}"
        with open(file_location, "wb+") as file_object:
            file_object.write(text.file.read())        
        summary=get_summary_from_text_file(file_location)
        # print(summary)
        return summary
        # return JSONResponse(content={"summary": summary})
         
        
    else:
        return {"Summary not found! Please upload a text file"}  


#endpoint for audioinput
##########################################################################################################
      
@app.post("/audio")
def create_upload_file(audio: UploadFile = File(...)):    
    ext=audio.filename.split('.').pop()
    if ext == 'flac' or ext == 'wav' or ext == 'mp3':  
        # if(ext=='wav'):
        #     song = AudioSegment.from_wav(audio.filename)
        #     song.export("testme.flac",format = "flac")
            
        
        file_location = f"static/audio/{audio.filename}{uuid.uuid1()}"
        with open(file_location, "wb+") as file_object:
            file_object.write(audio.file.read())
        transcript=predict_from_speech(file_location)
        return transcript
        # return audio
    else:
        return {"Please upload a flac or wav or mp3 file! upload failed"}

        

    
       
    