import instaloader
from pytube import YouTube

def download_instagram_post():
    L = instaloader.Instaloader()
    post_url = input("Enter the Instagram post URL: ").strip()
    try:
        shortcode = post_url.split("/")[-2]  # Extract shortcode from URL
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target="instagram_downloads")
        print("Instagram post downloaded successfully in 'instagram_downloads' folder.")
    except Exception as e:
        print("Error downloading Instagram post:", e)

def download_youtube_video():
    url = input("Enter the YouTube video URL: ").strip()
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path="youtube_downloads")
        print("YouTube video downloaded successfully in 'youtube_downloads' folder.")
    except Exception as e:
        print("Error downloading YouTube video:", e)

def main():
    while True:
        print("\nDownload Menu:")
        print("1. Download Instagram Post")
        print("2. Download YouTube Video")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            download_instagram_post()
        elif choice == '2':
            download_youtube_video()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
