import os
import sys
import shutil
import requests
# import webbrowser

import warnings
warnings.filterwarnings("ignore")


READ_PATH = "Files"
SAVE_PATH = "Processed"
REQUEST_URL = "https://api.deepai.org/api/CNNMRF"


def main():
    
    args_1: tuple = ("--style", "-sy")
    args_2: tuple = ("--file", "-f")
    
    style_image_filename: str = None
    filename: str = None

    if args_1[0] in sys.argv: style_image_filename = sys.argv[sys.argv.index(args_1[0]) + 1]
    if args_1[1] in sys.argv: style_image_filename = sys.argv[sys.argv.index(args_1[1]) + 1]

    if args_2[0] in sys.argv: filename = sys.argv[sys.argv.index(args_2[0]) + 1]
    if args_2[1] in sys.argv: filename = sys.argv[sys.argv.index(args_2[1]) + 1]


    assert style_image_filename is not None, "No Style Image Specified"
    assert filename is not None, "No Image Specified"

    assert style_image_filename in os.listdir(READ_PATH), "Style Image Not Found"
    assert filename in os.listdir(READ_PATH), "Image Not Found"
    
    response = requests.post(
        url=REQUEST_URL,
        files={
            "style" : open(os.path.join(READ_PATH, style_image_filename), "rb"),
            "content" : open(os.path.join(READ_PATH, filename), "rb"),
        },
        headers={
            "api-key" : os.environ["DEEPAI_KEY"],
        }
    )

    # webbrowser.open(response.json()["output_url"])
    
    download = requests.get(response.json()["output_url"], stream=True)
    if download.status_code == 200:
        with open(os.path.join(SAVE_PATH, "Stylized.jpg"), "wb") as f:
            shutil.copyfileobj(download.raw, f)
    else:
        print("Image couldn't be retrieved")


if __name__ == "__main__":
    sys.exit(main() or 0)
