### Text to Image ###

# Installation #

!pip install openai
!pip install gradio

# Imports #

import gradio as gr
import json
import openai

# Key #

data = "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"
openai.api_key = data

# ChatGPT API function #

def chatgpt_api(input_text):
  messages = [
  {"role":"system", "content":"You are a helpful assistant."}]
  
  if input_text:
      messages.append(
        {"role":"user", 
         "content": 'Summarize this text "{}" into a short concise Dall-e2 prompt'.format(input_text)}
      )
      chat_completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo", messages=messages
      )
  reply = chat_completion.choices[0].message.content
  return reply
  
  
# Dall-e2 API function #

def dall_e_api(dalle_prompt): 

    dalle_response = openai.Image.create(
            prompt = dalle_prompt,
            size="512x512"
        )
    image_url = dalle_response['data'][0]['url']
    return image_url
    

# Whisper API #

def transcribe(input_audio):
    
    audio_file = open(input_audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    dalle_prompt = chatgpt_api(transcript["text"])
    image_url = dall_e_api(dalle_prompt)
    return transcript["text"], image_url
    
# Gradio Interface #

output_1 = gr.Textbox(label="Speech to Text")
output_2 = gr.Image(label="DALL-E Image")

speech_interface = gr.Interface(fn = whisper_transcribe,
                                inputs = gr.Audio(source="microphone", type="filepath"),
                                outputs = [output_1, output_2],
                                title = "Generate Images using Voice")
speech_interface.launch(debug=True)

