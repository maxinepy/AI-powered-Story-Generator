# imports
import streamlit as st
from openai import OpenAI

# statics

# methods
def story_generator(prompt):
  story_response = client.chat.completions.create(
      model = 'gpt-3.5-turbo',
      messages = [
          {
              "role": 'system',
              "content": '''You are a bestseller story writer. You will take user's prompt and generate a 100 word short story for adults age 20-30'''
          }, 
          {
              "role": "user",
              "content": f'{prompt}'
          }
      ],
      max_tokens = 400,
      temperature = 0.5
  )

  story = story_response.choices[0].message.content
  return story

def refine_image(story):
  design_response = client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {
            "role": 'system',
            "content": '''Based on the story given. You will design a detailed image prompt for the cover of this story. 
            The image prompt should include the theme of the story with relevant color, suitable for adults.
            The output should be within 100 characters.
            '''
        }, 
        {
            "role": "user",
            "content": f'{story}'
        }
    ],
    max_tokens = 400,
    temperature = 0.5
)

  design_prompt = design_response.choices[0].message.content
  return design_prompt

def image_generator(story):
  cover_response = client.images.generate(
      model = 'dall-e-2',
      prompt = f"{story}",
      size = "256x256",
      quality = 'standard',
      n = 1 # number of images
  )

  image_url = cover_response.data[0].url
  return image_url 

api_key = st.secrets['OPENAI_SECRET']
client = OpenAI(api_key = api_key)

with st.form(key=' '):
  st.write('This is for user to key in information')
  msg = st.text_input(label="Some keywords to generate a story")
  submitted = st.form_submit_button(label='Submit')
  if submitted:
    st.balloons()
    story = story_generator(msg)
    st.caption('Story')
    st.write(story)
    design_prompt = refine_image(story)
    st.caption('Design Prompt')
    st.write(design_prompt)
    image_url = image_generator(design_prompt)
    if image_url is not None:
      st.caption('Image')
      st.image(image_url)
