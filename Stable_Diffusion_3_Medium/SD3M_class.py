import torch
from diffusers import StableDiffusion3Pipeline
from datetime import datetime
from time import time
import os

# tips for optimizing memory usage:
# https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/stable_diffusion_3#using-a-quantized-version-of-the-t5-text-encoder

# Use huggingface_hub_gate_acceptance.py first to gain access to the model. You only need to run it once.

class ImageGenerator:
    def __init__(self):
        if torch.cuda.is_available():
            print("CUDA available")
            self.pipe = StableDiffusion3Pipeline.from_pretrained(
                "stabilityai/stable-diffusion-3-medium-diffusers",
                text_encoder_3=None,  # Removing the memory-intensive 4.7B parameter T5-XXL text encoder during inference can significantly decrease the memory requirements for SD3 with only a slight loss in performance.
                tokenizer_3=None,     # This is part of removing the T5-XXL model
                torch_dtype=torch.float16,
                ).to("cuda")
            self.pipe.enable_model_cpu_offload()  # offload the components of the model to CPU during inference in order to save memory
            # self.pipe.to("cuda")
        else:
            print("CUDA not available")
            exit()
        print("Image Generator initialized")

    def generate_image(self, prompt="Hack The Planet", style="realistic, photographic, 4k"):        
        start_time = time()
        full_prompt = f"{prompt} {style}"
        self.prompt = prompt
        print(f"Generating image for prompt: {full_prompt}")
        self.image = self.pipe(
            prompt=prompt,
            prompt_2=style,
            negative_prompt="cartoon. animation. illustration. drawing. grainy. pixelated. low resolution. low quality.",
            num_inference_steps=40, # 30 has been good
            height=1024,
            width=1024,
            guidance_scale=9.0,
            max_sequence_length=256,   # By default, the T5 Text Encoder prompt uses a maximum sequence length of 256. Longer sequences require additional resources and result in longer generation times
            num_images_per_prompt=1,
            output_type='pil' # choose between PIL.Image.Image or np.array
        ).images[0]

        print(f"Generation time: {time() - start_time:.2f} seconds")

        return self.image

    def save_image(self, path_to_save="path-to-images-directory", save_name=None):
        if save_name is None:
            save_name = self.prompt[:20]
            save_name = ''.join(e for e in save_name if e.isalnum() or e.isspace())
        timestring = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if os.path.exists(path_to_save):
            # save to the specified path if it exists
            self.image_name = f"{path_to_save}\\{save_name[:20]}_{timestring}.png"
        else:
            # save to the local directory
            self.image_name = f"images\\{save_name[:20]}_{timestring}.png"
        self.image.save(self.image_name)
        print(f"Image saved to {self.image_name}")

    def release_GPU_memory(self):
        torch.cuda.empty_cache()

if __name__ == "__main__":
    imgen = ImageGenerator()

    while True:
        prompt = input("Enter a prompt: ")
        style = input("Enter a style: ")
        if prompt == "exit":
            break
        imgen.generate_image(prompt=prompt, style=style)
        imgen.save_image()
        imgen.release_GPU_memory()