from gpt4all import GPT4All

model = GPT4ALL("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
model.generate("What is the capitaol of france?")
print(output)

