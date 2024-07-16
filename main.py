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

st.header(':blue[_AI Story Generator_] :open_book:', divider= 'rainbow')

if 'story' not in st.session_state:
    st.session_state.story = None
if 'design_prompt' not in st.session_state:
    st.session_state.design_prompt = None
if 'image_url' not in st.session_state:
    st.session_state.image_url = None

# form to generate story
with st.form(key='story_form'):
    st.write('Enter keywords to generate a story')
    msg = st.text_input(label="Some keywords to generate a story")
    submitted = st.form_submit_button(label='Submit')
    if submitted and msg != '':
        st.balloons()
        st.session_state.story = story_generator(msg)
        st.session_state.design_prompt = None
        st.session_state.image_url = None

# display the generated story
if st.session_state.story:
    st.caption('Story')
    st.write(st.session_state.story)
    # follow-up form to generate cover image
    with st.form(key='image_form'):
        st.write('Would you like to generate a cover image for this story?')
        yes = st.form_submit_button('Yes')
        if yes:
            st.session_state.design_prompt = refine_image(st.session_state.story)
            st.session_state.image_url = image_generator(st.session_state.design_prompt)

# display cover image
if st.session_state.image_url:
    st.caption('Cover Image')
    st.image(st.session_state.image_url)

if st.session_state.design_prompt:
    # follow-up form to display image prompt
    with st.form(key='design_prompt_form'):
        st.write('Would you like to see the image prompt?')
        yes = st.form_submit_button('Yes')
        if yes:
            st.caption('Design Prompt')
            st.write(st.session_state.design_prompt)
