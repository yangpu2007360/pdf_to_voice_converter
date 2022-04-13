from tkinter import *
from tkinter import filedialog
import textract
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
import PyPDF2

session = Session(profile_name="polly")
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
polly = session.client("polly")

root = Tk()
root.geometry("500x300")

myLabel = Label(root, text="Hello, I can read a file for you. Please upload a pdf file.", font=("Arial", 16, "bold"),
                pady=15)

filename = ""
text = ""


def upload_file():
    global filename
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    readButton["state"] = "normal"


def connect_aws():
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(
            Text=text, OutputFormat="mp3",
            VoiceId="Joanna")

    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)
        # Access the audio stream from the response
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "speech.mp3")
            print("speech created")
            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)
        # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])


def read_file():
    global text
    print("I will read this file for you")
    file = open(f'{filename}', 'rb')
    reader = PyPDF2.PdfFileReader(file)
    print(reader.numPages)

    for num in range(0, reader.numPages):
        print(num)
        page = reader.getPage(num)
        text = text + page.extractText()
        print(text)
        print(type(text))

    connect_aws()


uploadButton = Button(root, text='Upload', command=upload_file)
readButton = Button(root, text='Read the file out loud', command=read_file)
readButton["state"] = "disabled"

myLabel.pack()
uploadButton.pack()
readButton.pack()

root.mainloop()

myLabel.pack()
root.mainloop()
