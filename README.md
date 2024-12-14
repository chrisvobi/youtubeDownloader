# YouTube Downloader

A simple Python-based YouTube video downloader that allows users to download videos or audio from YouTube.
Also works with playlists.

## Features

- Download YouTube videos.
- Extract and download audio only.

## Prerequisites

Before running the project, make sure you have the following installed:

1. **Python** (>= 3.6):  
   The project is written in Python. You can download it from [here](https://www.python.org/downloads/).

2. **ffmpeg**:  
   This project requires `ffmpeg` for processing audio and video formats. Follow the instructions below to install it on your system:

   - **Windows**:
     1. Download `ffmpeg` from the official website: [FFmpeg Downloads](https://ffmpeg.org/download.html).
     2. Extract the ZIP file and place it in a folder (e.g., `C:\ffmpeg`).
     3. Add the `bin` directory to your system's PATH:
        - Right-click on "This PC" and select "Properties".
        - Click on "Advanced system settings", then "Environment Variables".
        - Under "System variables", find and select `Path`, then click "Edit".
        - Add the path to the `bin` directory of `ffmpeg` (e.g., `C:\ffmpeg\bin`) and click "OK".

   - **macOS**:
     1. Install `Homebrew` if you haven't already: [Homebrew Website](https://brew.sh).
     2. Run the following command in the terminal:
        ```bash
        brew install ffmpeg
        ```

   - **Linux**:
     1. On Debian/Ubuntu-based systems, you can install `ffmpeg` using:
        ```bash
        sudo apt update
        sudo apt install ffmpeg
        ```
     2. For other distributions, use the appropriate package manager for your system.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/chrisvobi/youtubeDownloader.git
   ```

2. Navigate to the project directory:

   ```bash
   cd youtubeDownloader
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script:

   ```bash
   python main.py
   ```

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request. Ensure your code follows proper coding standards and includes comments where necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for personal and educational use only. Downloading copyrighted content from YouTube without permission is against YouTube's Terms of Service.
