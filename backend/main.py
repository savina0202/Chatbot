from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse,JSONResponse
import uvicorn
import whisper
from transformers import pipeline
import pyttsx3
from pydub import AudioSegment #convert PCM WAV to wav
import io, json
from pydantic import BaseModel 
from llm.loadllm import llm_call
from llm.prompting import SYSTEM_INSTRUCTION
from llm.route_llm_output import route_llm_output
import logging
from utils.logs import enable_log

enable_log("backend")

# Define Global Variables
app = FastAPI(title="Voice Search LLM Agent", description="API for voice agent functionalities")

asr_model = whisper.load_model("small")
conversation_history = []


def transcribe_audio(audio_bytes):

    # Auto-detect format
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    wav_path = "input.wav"
    audio.export(wav_path, format="wav")
    with open("input.wav", "wb") as f:
        f.write(audio_bytes)
    result = asr_model.transcribe("input.wav")
    return result["text"]

def generate_response(user_text):

    conversation_history.append({"role": "user", "text": user_text})

    # Construct prompt from history
    prompt = ""
    for turn in conversation_history[-5:]:
        prompt += f"{turn['role']}: {turn['text']}\n"
    
    # Add a clear instruction for the model
    #prompt += "assistant: "

    prompt = f"{SYSTEM_INSTRUCTION}\nuser: {user_text}\nassistant: " ## added by savina
    print(f"Prompt: {prompt}\n")
    print("*" * 20)

    outputs = llm_call(prompt, max_new_tokens=100)

    bot_response = outputs
    
    return bot_response

def synthesize_speech(text):
    filename="response.wav"
    tts_engine = pyttsx3.init()
    tts_engine.save_to_file(text, filename)
    tts_engine.runAndWait()

    return filename

@app.get("/")  
def root():
    return {"Api":"Voice Search LLM Agent"}


@app.get("/chathist/")
def get_chat_history():
    return JSONResponse(content=conversation_history)

@app.post("/clear_history/")
def clear_chat_history():
    global conversation_history
    conversation_history = []
    return JSONResponse(content={"message": "Chat history cleared successfully"})

@app.post("/voice-query/")
#async def voice_query_endpoint(request: QueryRequest):
async def voice_query_endpoint(audio: UploadFile = File(...)):
    # Assume request has 'text': the user's query string
    #user_text = request.text
    audio_bytes = await audio.read()

    user_text = transcribe_audio(audio_bytes)
    logging.info(f"User text: {user_text}")

    llm_response = generate_response(user_text)
    logging.info(f"LLM response: {llm_response}")

    # Process LLM output and possibly call tools
    reply_text, func = route_llm_output(llm_response)
    conversation_history.append({"role": "assistant", "text": llm_response})
    conversation_history.append({"role": "assistant", "text": reply_text})
    logging.info(f"Reply text: {reply_text}, called function: {func}")

    print("*"*20)
    print(f"Reply text from route_llm_output: {reply_text}\n")
    print("*"*20)

    # Convert reply_text to speech (TTS) and return it
    audio_path = synthesize_speech(reply_text)
    # 在响应 header 中加入 reply_text
    headers = {"X-Response-Text": reply_text}
    if func:
        headers["X-Tool-Name"] = str(func)
    return FileResponse(path=audio_path, media_type="audio/wav", filename=audio_path, headers=headers)




if __name__ == "__main__":

    print("Starting Voice Agent API...")

    print("API will be available at: http://localhost:8002")

    print("Interactive docs at: http://localhost:8002/docs")

    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)

