import openai

openai.api_key="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"
model_engine = "text-davinci-003"

def DallE(question):
    return openai.Image.create(
    prompt=question,
        n=2,
        size="256x256")