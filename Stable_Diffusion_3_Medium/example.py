import torch
from diffusers import StableDiffusion3Pipeline
from datetime import datetime
from time import time

start_time = time()

pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch.float16)

# choose to pipe directly to gpu or memory-optimize for cpu
memory_optimize = False
if memory_optimize:
    pipe.enable_model_cpu_offload()
else:
    pipe.to("cuda")

# set up prompts
prompt = "hacking the planet."
style = "Hyperrealistic photograph of"

full_prompt = f"{style} {prompt}"

image = pipe(
    prompt=full_prompt,
    negative_prompt="",
    num_inference_steps=1,
    height=512,
    width=512,
    guidance_scale=7.0,
).images[0]

timestring = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

image_name = f"Stable Diffusion 3 Medium\\images\\{prompt}_{timestring}.png"

image.save(image_name)

print(f"Image saved as {image_name}")
print(f"Elapsed time: {time() - start_time:.2f} seconds")