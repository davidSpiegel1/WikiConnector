from gpt4all import GPT4All


#just checks for exit condition at the moment
def check_user_input(userInput):
    if userInput == "":
        print("empty input")
        return 1
    userInput = userInput.strip()

    return 0


def main():
    print("Creating Session...")
    model = GPT4All(model_name="Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    cont = True
    tokens = []
    #Stores outof ot gpt prompt
    with model.chat_session():
        while cont == True:
            getPrompt = input("Enter a prompt (Press Enter to quit): \n")
            checkInput = check_user_input(getPrompt) 
            print("prompt test:", getPrompt)

            match checkInput:
                case 0:
                    response = model.generate(prompt=getPrompt, temp=0)
                    print("Response:", response)
                    print()
                case 1:
                    print("Setting galse")
                    cont = False


if __name__ == "__main__":
    main()
