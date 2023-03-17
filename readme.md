# Automatic Nepali Speech Recognition and Summarizer (ANSRAS)
A simple system developed as major project for final year of computer which will convert Nepali speech to text and provide summary of text.

## Tasks completed
- [X] Speech Recognition Using CNN-GRU
- [X] Speech Recognition Using Wav2Vec2
- [X] Text Summarization using TextRank

## Directory Structure
- Training folder has all files needed for model training
- Web_App folder has all files needed for webapp(frontend and backend included) for real time testing

## To setup webapp in your local machine
1. Clone this repo
2. Install all the requirements from requirements.txt
```
pip install -r requirements.txt
```
2. For setting up Backend Go inside backend folder
3. Inside nepalimodel create a new folder called model_wav2vec and then download files from [here](https://huggingface.co/anish-shilpakar/wav2vec2-nepali-asr-v1/tree/main) and place the files in this folder
4. Run this command to start backend server
```
uvicorn api:app --reload
```
5. For frontend, open a new terminal and go inside the frontend folder
6. Make sure you have react installed in your computer, then run following command
```
npm install
```
7. To open the webapp run frontend server while still keeping the backend server running
```
npm start
```

## Project Members
[Anish Shilpakar](https://github.com/JuJu2181)  
[Anjaan Khadka](https://github.com/AnjaanKhadka)  
[Sudip Shrestha](https://github.com/sudips413)  
[Sachin Manandhar](https://github.com/sachin035) 


***
*Feel Free to contact us if you want to know more about how we trained and integrated these models.*