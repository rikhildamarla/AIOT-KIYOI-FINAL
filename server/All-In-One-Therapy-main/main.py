import google.generativeai as genai


GOOGLE_API_KEY = "AIzaSyDO3yKGP_m1bhXwBFJVeJrgdDmVigVDu98"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

initial_prompt = (
    "You are a highly experienced psychotherapist with many years of experience. "
    "You are here to provide emotional support and guidance. Your responses should be "
    "empathetic, validating, and comforting. Always respond as if you are speaking to a client in a therapy session."
)

def generate_response(user_input):
    try:

        prompt = f"{initial_prompt}\nClient: {user_input}\nTherapist:"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"


print("Hi, I am your therapist! How can I help you today?")
quit = False

while not quit:
    user_input = input()
    if user_input.lower() == "quit":
        quit = True
    else:
        response = generate_response(user_input)
        print(response)
