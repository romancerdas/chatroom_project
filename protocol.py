import json

def encode_message(message): # Converts Python object "message" into JSON string and then converts it into bytes to prep it to send over the network. 

    return json.dumps(message).encode("utf-8")



def decode_message(data): # Converts data received as bytes back into a JSON string and the decodes it back into a readable python object. 

    return json.loads(data.decode("utf-8"))