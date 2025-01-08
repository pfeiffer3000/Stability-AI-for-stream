# Stability-AI-for-stream
 AI Image generator and LLM chatbot servers and clients

LLM chatbot:
_client_LLM_prompt_sender.py sends prompts to _server_LM2Z_1_6B_45123.py, which uses Stability AI's Zephyr 1.6B model on port 45123.

Image gen:
_client_SD3M_prompt_sender.py sends prompts to _server_SD3M_45124.py, which uses Stability AI's Stable Diffusion 3 Medium model on port 45124.

You'll need to register your computer with HuggingFace before using the Stable Diffusion 3 Medium model. You can use Stable_Diffusion_3_Medium\huggingface_hub_gate_acceptance.py to do that. You'll need to get a HuggingFace token first. They should have info about how to do that on their site.

Both of the servers are intended to run on computers that are running the AI models only--something with a GPU. The client is running on a separate computer on the same local network. However, there is no reason they can't run on the same computer, or even streamlined to run in the same program. 

I got ~30-second generation times on the image generator using an RTX 3060. The LLM server can return a response in under 10 seconds on a CPU-only computer (no GPU available).

More info at https://djpfeif.com/portfolio/ai-for-streaming/