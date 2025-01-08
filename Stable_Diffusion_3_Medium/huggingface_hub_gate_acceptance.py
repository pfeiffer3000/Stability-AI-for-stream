# use this to register a new computer with Hugging Face so that SD3 will work
# SD3 is 'gated' by Hugging Face, so you need to register your computer with them

HUGGINGFACE_TOKEN = "your token goes here"

from huggingface_hub import login
login(token=HUGGINGFACE_TOKEN)