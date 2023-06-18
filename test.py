# import the opencv library
import asyncio
import base64
import io
import traceback

import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from hume import HumeStreamClient
from hume.models.config import FaceConfig
from PIL import Image

from utilities import download_file, print_emotions

filepath = download_file("https://storage.googleapis.com/hume-test-data/image/obama.png")
vid = cv2.VideoCapture(0)
async def main():
    client = HumeStreamClient("h0CGCavYvDdMOG19WKzNDhkLvXZ3CkGUEz7wGR31IdGrZoXG")
    config = FaceConfig(identify_faces=True)
    print("I'm in main 3")
    async with client.connect([config]) as socket:
        print("I'm in main 4")
        while(1):
            print("I'm in main 5")
            # Enable face identification to track unique faces over the streaming session
            ret, frame = vid.read()
            print(ret)
            im = Image.fromarray(frame.astype("uint8"))
            rawBytes = io.BytesIO()
            im.save(rawBytes, "PNG")
            rawBytes.seek(0)  # return to the start of the file
            display = base64.b64encode(rawBytes.read())
            # cv2.imshow('frame', frame)
            # im.show(display)
            print("Size: ", len(display))
            print("Waiting for result")
            result = await socket.send_bytes(display)
            # print(result)
            print("Got result")
            try:
                emotions = result["face"]["predictions"][0]["emotions"]
                print_emotions(emotions)
            except:
                pass
            if cv2.waitKey(1) & 0xFF == ord('q'):
                vid.release()
                cv2.destroyAllWindows()
                break
        vid.release()
        cv2.destroyAllWindows()
asyncio.run(main())