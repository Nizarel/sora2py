# Azure OpenAI Sora-2 Video Generator - Code Explanation

This project provides a Python-based toolkit for generating videos using Azure OpenAI's Sora-2 model. The system supports both simple single-segment video generation and advanced multi-segment video chaining with smooth transitions.

## Core Architecture

The project consists of three main Python scripts that work together to create videos of varying lengths. **video_generator.py** handles the fundamental video creation, supporting both text-to-video and image-to-video generation modes. **extract_last_frame.py** serves as a utility to capture the final frame from a video, which becomes crucial for creating continuity between segments. **chain_videos.py** orchestrates the entire process of creating longer videos by intelligently combining multiple 12-second segments.

## Video Generation Process

The video generation workflow begins with the **video_generator.py** script, which interfaces with Azure OpenAI's API using the OpenAI Python SDK v2.0+. The script loads credentials from a `.env` file and initializes a client that communicates with Azure's endpoint. What's particularly interesting here is that Azure uses the OpenAI v1 API format with a custom base URL, requiring both standard API key authentication and an additional "api-key" header for Azure compatibility.

When generating a video, the script supports two distinct modes. In text-to-video mode, it sends a text prompt directly to the API along with parameters like duration (4, 8, or 12 seconds) and resolution (up to 1920x1080). In image-to-video mode, it reads an input image file and sends it alongside the prompt, allowing Sora-2 to animate a still image or continue from a previous video's last frame. The API call is asynchronous—it returns a job ID immediately, and the script polls every 10 seconds until the status changes to "completed", "failed", or "cancelled".

## Frame Extraction for Continuity

The **extract_last_frame.py** utility plays a critical role in the chaining process. Using OpenCV (cv2), it opens a video file, determines the total frame count, seeks to the last frame, and saves it as a JPEG image. This extracted frame becomes the input image for the next segment, creating visual continuity between segments. The script includes careful error handling for cases where videos can't be opened or frames can't be read, ensuring reliability in automated workflows.

## Video Chaining Strategy

The **chain_videos.py** script implements a sophisticated approach to creating videos longer than the 12-second API limit. It calculates how many segments are needed based on the desired total duration, then generates each segment sequentially. The first segment uses pure text-to-video generation, but subsequent segments use image-to-video mode with the last frame from the previous segment as input. This creates a "daisy chain" effect where each segment naturally flows from the previous one.

The key to smooth transitions lies in the crossfade implementation using ffmpeg. Rather than simply concatenating segments, the script builds a complex ffmpeg filter that overlays segments with configurable crossfade durations (default 1.0 seconds, adjustable from 0.5 to 2.0 seconds). The filter uses the "smoothleft" transition type, which provides more natural blending than abrupt cuts. Each crossfade is positioned at the junction between segments, with careful offset calculations to ensure proper timing.

## Platform Compatibility and Encoding

A subtle but important detail throughout all scripts is the handling of UTF-8 encoding on Windows. The code explicitly reconfigures `sys.stdout` to use UTF-8 encoding and sets encoding parameters for subprocess calls. This prevents issues with emoji characters (like 🎬 and ✅) and special characters that might appear in prompts or file paths, ensuring consistent behavior across Windows, macOS, and Linux environments.

## Dependency Management and Error Handling

The project carefully validates dependencies before execution. The chain_videos script checks for the availability of video_generator.py, extract_last_frame.py, and ffmpeg before proceeding. If any are missing, it provides helpful error messages with installation instructions. Similarly, extract_last_frame.py checks for OpenCV and provides installation guidance if it's missing.

## Cleanup and Output

After successfully creating a chained video, the system automatically cleans up temporary files—both the individual segment videos and the extracted frame images. This prevents disk clutter during batch processing. The final output includes detailed information about the video creation process, including total duration, number of segments used, transition duration, and the specific method employed (image-to-video chaining with enhanced blending).

## Content Moderation Gotcha

One particularly important consideration is Azure's content moderation system. Even with minimal filter settings, the API blocks prompts containing children or minors in various contexts. This is a common stumbling block for users who might try innocent prompts like "girl swimming" only to receive moderation errors. The documentation wisely recommends using neutral subjects like animals, nature, and objects instead. This is a practical example of how real-world API usage differs from theoretical capabilities—you must design prompts with content policies in mind, not just creative vision.