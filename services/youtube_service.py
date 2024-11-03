# services/youtube_service.py
from pytube import YouTube

def get_video_info(url):
    """
    Fetches information about the video, including available resolutions.
    
    Args:
        url (str): The URL of the YouTube video.
        
    Returns:
        dict: Contains the video title and a dictionary of available resolutions with their itags.
    """
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, file_extension="mp4")
    resolutions = {stream.resolution: stream.itag for stream in streams}
    return {"title": yt.title, "resolutions": resolutions}

def download_video(url, itag):
    """
    Downloads the video from YouTube at the specified resolution.
    
    Args:
        url (str): The URL of the YouTube video.
        itag (int): The itag of the video stream to download.
    
    Returns:
        str: The file path of the downloaded video.
    """
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(itag)
    file_path = stream.download()
    return file_path
