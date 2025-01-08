''' 
This functions as a chatbot class.
It currently has no history.
It responds to user input with a simple string response.
'''

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
# from time import time

tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-2-zephyr-1_6b')
model = AutoModelForCausalLM.from_pretrained(
    'stabilityai/stablelm-2-zephyr-1_6b',
    device_map="auto",
    torch_dtype=torch.float32, # use this for cpu
    # torch_dtype="auto"  # set this to "auto" for use with gpu
)

class Chatbot:
    def __init__(self):
        self.name = "stablelm-2-zephyr-1_6b"
        # self.user_inputs = []
        # self.ai_responses = []
    
    def chat(self, input_prompt):
        # start_time = time()

        # directions = "Respond in one sentence that is humorous. Respond as if you were an internet troll. Respond like a bot on Twitch. Focus on the next sentence."
        prompt = [{'role': 'user', 'content': input_prompt}]

        inputs = tokenizer.apply_chat_template(
            prompt,
            add_generation_prompt=True,
            return_tensors='pt'
        )

        tokens = model.generate(
            inputs.to(model.device),
            max_new_tokens=256,
            temperature=0.5,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id
        )
        ai_response = tokenizer.decode(tokens[0], skip_special_tokens=False)
        response = ai_response.split("<|assistant|>")[1][:-len("<|endoftext|>")].strip()

        return response

if __name__ == "__main__":
    chatbot = Chatbot()

    while True:
        print()
        input_prompt = input("> ")
        response = chatbot.chat(input_prompt)
        print(response)