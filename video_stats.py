import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
maxResults = 50

# Function to retrieve the upload playlist ID for a given YouTube channel handle
# Returns the playlist ID as a string
def get_playlist_id():

    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        # Get the channel details from the YouTube API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response and extract the channel's upload playlist ID
        data = response.json()
        # The JSON representation of the response data with indentation for readability
        json.dumps(data, indent=4)

        channel_items = data["items"][0]
        channel_playlistsId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        
        return channel_playlistsId
    except requests.exceptions.RequestException as e:
        raise e

# Function to retrieve the list of videos from the upload playlist for a given YouTube channel handle
# Returns a list of video IDs as strings

def get_videos_id(playlist_id):

    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            for item in data.get("items",[]):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            pageToken = data.get("nextPageToken")

            if not pageToken:
                break
        return video_ids

    except requests.exceptions.RequestException as e:
        raise e

def extract_video_data(video_ids):

    extracted_data = []

    def batch_get_video_details(video_id_list,batch_size):
        for video_id in range(0, len(video_id_list), batch_size):
            # Yield a batch of video IDs from the list, up to the specified batch size
            yield video_id_list[video_id : video_id + batch_size]
        

    try:
        for batch in batch_get_video_details(video_ids, maxResults):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    "video_id" : video_id,
                    "title" : snippet['title'],
                    "publishedAt" : snippet['publishedAt'],
                    "duration" : contentDetails['duration'],
                    "viewCount" : statistics.get('viewCount', None),
                    "likeCount" : statistics.get('likeCount', None),
                    "commentCount" : statistics.get('commentCount', None)
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e


# Main execution block for the video_stats script
if __name__ == "__main__":
    # This will call the function and print the result if needed
    playlist_id = get_playlist_id()
    video_ids = get_videos_id(playlist_id)
    print(extract_video_data(video_ids))
