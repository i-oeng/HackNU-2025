🎬 Unbounded Video Maker — Higgsfield API Automation
This project demonstrates how to generate AI-driven cinematic videos using the Higgsfield AI Platform — from text-to-image (Soul / Nano Banana models) to image-to-video (DoP Turbo), and finally merging the clips into one seamless video using FFmpeg.

🧠 Idea:
Since Higgsfield DoP has a duration limit, this project automatically splits the user’s prompt into smaller scenes, generates consecutive image frames, converts them into short videos, and concatenates them locally to remove time restrictions.

🚀 Features
✅ Generate realistic images from natural language prompts using Soul/Nano Banana
✅ Create smooth motion videos between consecutive images using DoP Turbo
✅ Merge all short clips into one continuous video
✅ FastAPI-powered REST API for easy front-end integration
✅ Local saving of images and videos for testing
✅ Works in series mode (no GPU parallelism needed)

🏗️ Architecture Overview
graph LR
    A[Frontend or REST Call] --> B[FastAPI /app.py]
    B --> C[Text Prompt Splitter]
    C --> D[Text-to-Image (Soul)]
    D --> E[Image Storage (local)]
    E --> F[Image-to-Video (DoP Turbo)]
    F --> G[Local Video Segments]
    G --> H[FFmpeg Concatenation]
    H --> I[Final Video in /final_videos]

Tech Stack

| Component          | Description                                               |
| ------------------ | --------------------------------------------------------- |
| **FastAPI**        | REST API to orchestrate the generation process            |
| **Higgsfield API** | Used for `/text2image/nano_banana` and `/image2video/dop` |
| **Requests**       | Lightweight async HTTP client for API calls               |
| **FFmpeg**         | Used to merge generated clips into one                    |
| **Python-dotenv**  | Loads API credentials from `.env`                         |
| **Python 3.9+**    | Tested on macOS and Linux                                 |



🧠 How It Works

Prompt splitting:
The input prompt is divided into smaller chunks (prompt_divider()), each representing a short scene.

Text-to-Image (Soul):
For each scene, the API generates an image (/text2image/nano_banana) and stores the image URL.

Image-to-Video (DoP Turbo):
Each pair of consecutive images is converted into a short video clip (/image2video/dop).

Concatenation:
All clips are merged locally using ffmpeg into a final output saved under /final_videos.
