import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"

def get_playlist_id():

    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        # Get the channel details from the YouTube API
        response = requests.get(url)

        # Parse the JSON response and extract the channel's upload playlist ID
        data = response.json()
        # The JSON representation of the response data with indentation for readability
        json.dumps(data, indent=4)

        channel_items = data["items"][0]
        channel_playlistsId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        
        return channel_playlistsId
    except requests.RequestException as e:
        raise e

# Main execution block for the video_stats script
if __name__ == "__main__":
    # This will call the function and print the result if needed
    print("get_paylist_id will be executed")
    print(get_playlist_id())
