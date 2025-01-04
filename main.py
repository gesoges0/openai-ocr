from openai import OpenAI
import pprint
import base64
import click
from pathlib import Path


MESSAGE = """
## 命令
これは本を写真で撮った画像です。この画像の蛍光ペンでマーキングされた部分をテキストに変換してください。
また、右上もしくは左上にあるページ数もテキストに変換してください。
出力の形式は
```
[
    {
        "page_number": "ページ数(数値)",
        "text": "テキスト"
    },
]
```
のようにしてください。```の部分は必要ありません。1ページに複数の蛍光ペンでマーキングされている場合は、それぞれのテキストを改行してください。
```
[
    {
        "page_number": "1",
        "text": "テキスト1"
    },
    {
        "page_number": "1",
        "text": "テキスト2"
    }
]
```
のように出力してください。

## 出力
"""


@click.group()
def main():
    pass


def get_base64_image(path: Path) -> str:
    with path.open("rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


@main.command()
@click.option("--path", type=str, help="path of image file")
def ocr_one_image(path: str):
    base64_image = get_base64_image(Path(path))
    client = OpenAI()
    request = client.chat.completions.create(
        model="gpt-4o",
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
                        "text": MESSAGE,
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
    pprint.pp(request)
    print("- " * 50)
    print(request.choices[0].message.content)


if __name__ == "__main__":
    main()
