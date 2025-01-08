from transformers import AutoModelForCausalLM, AutoTokenizer
from time import time

tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-2-zephyr-1_6b')
model = AutoModelForCausalLM.from_pretrained(
    'stabilityai/stablelm-2-zephyr-1_6b',
    device_map="auto"
)

user_inputs = []
ai_responses = []

while True:
    print()
    input_prompt = input("> ")
    start_time = time()
    user_inputs.append(input_prompt)
    prompt = [{'role': 'user', 'content': input_prompt}]

    inputs = tokenizer.apply_chat_template(
        prompt,
        add_generation_prompt=True,
        return_tensors='pt'
    )

    tokens = model.generate(
        inputs.to(model.device),
        max_new_tokens=1024,
        temperature=0.5,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id
    )
    ai_response = tokenizer.decode(tokens[0], skip_special_tokens=False)
    ai_response_li = ai_response.split("<|assistant|>")

    print()
    print("AI response:")
    print(ai_response_li[1][:-len("<|endoftext|>")])
    print()
    end_time = time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")