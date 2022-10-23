import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from model.config import *
import os 
# To ignore cuda warnings of no gpu
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def segmentLargeArray(inputTensor,chunksize=200000):
    # print(inputTensor)
    list_of_segments = []
    tensor_length = inputTensor.shape[1]
    for i in range(0,tensor_length+1,chunksize):
        list_of_segments.append(inputTensor[:,i:i+chunksize])
    return list_of_segments 


def predict_from_speech(file,model,processor):
    print("=> Loading the audio input to the model")
    speech_array, sampling_rate = torchaudio.load(file)
    # print(speech_array,sampling_rate)
    resampler = torchaudio.transforms.Resample(sampling_rate, 16000)
    resampled_array = resampler(speech_array).squeeze()
    if len(resampled_array.shape) == 1:
        resampled_array = resampled_array.reshape([1,resampled_array.shape[0]])
    # print(resampled_array.shape[1])
    if resampled_array.shape[1] >= 200000:
        print('The input file is longer than 10 seconds')
        print('Now Predicting ...')
        list_of_segments = segmentLargeArray(resampled_array,chunksize=50000)
        # print(list_of_segments)
        output = ''
        for segment in list_of_segments:
            logits = model(segment.to(DEVICE)).logits
            pred_ids = torch.argmax(logits,dim=-1)[0]
            output += processor.decode(pred_ids)
        print(f"Prediction:\n{output}")
    else:
        print('The input file is less than 10 seconds')
        print('Now Predicting ...')
        logits = model(resampled_array.to(DEVICE)).logits
        # print(logits)
        pred_ids = torch.argmax(logits, dim = -1)[0]
        output = processor.decode(pred_ids)
        print(f"Prediction:\n{output}")
    return output
        
        
if __name__ == "__main__":
    # can be changed to relative paths
    model_path = 'D:\Programming\Projects\major_project\Codes\ASR\wav2vec_trained_models\\nepali-wav2vec-v2\model_0.1_dropout_5_10sec' 
    processor_path = 'D:\Programming\Projects\major_project\Codes\ASR\wav2vec_trained_models\\nepali-wav2vec-v2\processor_0.1_dropout_5_10sec'
    print("=> Loading the trained model and processor")
    model = Wav2Vec2ForCTC.from_pretrained(model_path).to(DEVICE)
    processor = Wav2Vec2Processor.from_pretrained(processor_path)
    ip_file_path = input('Enter the file to test: ')
    print('=> Input received')
    basename = os.path.basename(ip_file_path)
    filename,ext = os.path.splitext(basename)
    op_file_path = f'D:\Programming\Projects\major_project\Codes\ASR\wav2vec_predictions\\{filename}.txt'
    output = predict_from_speech(ip_file_path,model,processor)        
    with open(op_file_path,'w+',encoding='utf-8') as f:
        f.write(output)
    print("=> Output has been written to a file")