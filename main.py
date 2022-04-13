from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).

session = Session(profile_name="polly")
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
polly = session.client("polly")

try:
 # Request speech synthesis
    response = polly.synthesize_speech(Text="Hello world! My name is Pu Yang. I got married with vicky wen in 2016.", OutputFormat="mp3", VoiceId="Joanna")

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