from openai import OpenAI
import pprint
import base64

client = OpenAI()

image_path = "./example.jpeg"

with open(image_path, "rb") as image_file:  # 画像ファイルまでのパス
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

completion = client.chat.completions.create(
    model="gpt-4o",  # モデルの指定
    messages=[
        {
            "role": "system",
            "content": "You are an excellent secretary who responds in Japanese.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """\
## 命令
この画像に表示されている文字を教えて下さい。
書かれている文字以外は応答しないでください。

## Output
""",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
            ],
        },
    ],
)

print("- " * 50)
pprint.pp(completion)
print("- " * 50)
print(completion.choices[0].message.content)
