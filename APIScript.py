import google.generativeai as genai
import os
import time

# --- Configuration ---
# You can change the model if needed, e.g., "gemini-1.5-pro-latest" for more complex tasks
MODEL_NAME = "gemini-2.0-flash-001"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
print(f"API Key found: {'Yes' if GEMINI_API_KEY else 'No'}")


def analyze_video_gestures(video_paths):
    """
    Analyzes co-speech gestures in a list of video files using the Gemini API.

    Args:
        video_paths (list): A list of paths to video files.
    """
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set it before running the script.")
        print("Example (in terminal): export GEMINI_API_KEY='YOUR_API_KEY'")
        return

    try:
        # Configure the Gemini client library
        genai.configure(api_key=GEMINI_API_KEY)
        # Initialize the generative model
        model = genai.GenerativeModel(MODEL_NAME)
        print(f"Successfully initialized Gemini client with model: {MODEL_NAME}\n")
    except Exception as e:
        print(f"Error initializing Gemini client or model: {e}")
        return

    if not video_paths:
        print("No video paths provided in the 'videos_to_analyze' list.")
        return

    for video_path in video_paths:
        video_filename = os.path.basename(video_path)
        print(f"--- Processing video: {video_filename} ---")

        if not os.path.exists(video_path):
            print(f"Error: Video file not found at '{video_path}'")
            print("Skipping this video.\n")
            continue

        uploaded_file_resource = None  # To keep track of the file for deletion
        try:
            # 1. Upload the video file
            # The API automatically detects the MIME type.
            # Videos can take some time to upload depending on size and network.
            print(f"Uploading '{video_filename}'... This might take a moment.")
            uploaded_file_resource = genai.upload_file(path=video_path,
                                                       display_name=video_filename)
            print(
                f"Successfully uploaded: '{video_filename}' (File URI: {uploaded_file_resource.uri}, Name: {uploaded_file_resource.name})")

            # 2. Prepare the prompt with the video and the question
            # The prompt is a list of parts for a single user turn
            prompt_parts = [
                uploaded_file_resource,  # Pass the File object directly
                "Using linguistic terminology, can you classify the co-speech gesture in this clip in two sections: 1) the action being performed, and 2) the co speech gesture category the gesture belongs to?"
            ]

            # 3. Generate content (get classification)
            print("Asking Gemini to classify gestures...")
            # Adding a small delay before making the generate_content call,
            # sometimes helps ensure the file is fully ready after upload.
            time.sleep(2)  # Optional: Adjust or remove as needed

            response = model.generate_content(prompt_parts)

            # 4. Print the filename and Gemini's response
            print(f"\nVideo File: {video_filename}")
            if response.parts:
                print(f"Gemini's Response:\n{response.text}")
            else:
                # This case handles scenarios where the response might be empty
                # or blocked due to safety filters or other reasons.
                print("Gemini's Response: No content parts received.")
                if response.prompt_feedback:
                    print(f"  Reason (Prompt Feedback): {response.prompt_feedback}")
                if hasattr(response, 'candidates') and response.candidates:
                    for candidate in response.candidates:
                        if not candidate.content.parts:  # Check if parts are empty for this candidate
                            print(f"  Candidate Finish Reason: {candidate.finish_reason}")
                            if candidate.safety_ratings:
                                print(f"  Safety Ratings: {candidate.safety_ratings}")

        except Exception as e:
            print(f"An error occurred while processing '{video_filename}': {e}")
            # If the response object exists and has prompt_feedback, print it for more details
            if 'response' in locals() and hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                print(f"  Prompt Feedback details: {response.prompt_feedback}")

        finally:
            # 5. Delete the uploaded file from the server
            if uploaded_file_resource:
                try:
                    print(f"Attempting to delete uploaded file '{uploaded_file_resource.name}' from server...")
                    # Ensure the file is processed before deleting
                    # A short delay might be useful if immediate deletion causes issues,
                    # though typically not required after generate_content completes.
                    time.sleep(1)  # Optional
                    genai.delete_file(uploaded_file_resource.name)
                    print(f"Successfully deleted '{uploaded_file_resource.name}' from server.")
                except Exception as e:
                    print(f"Error deleting file '{uploaded_file_resource.name}' for '{video_filename}': {e}")
            print("-" * (len(f"--- Processing video: {video_filename} ---") + 4) + "\n")


if __name__ == "__main__":
    print("Co-Speech Gesture Analysis with Gemini API")
    print("=========================================\n")
    print("Important: Ensure you have the following before running:")
    print("1. Python installed.")
    print("2. The 'google-generativeai' library installed (pip install google-generativeai).")
    print("3. Your GEMINI_API_KEY environment variable set.")
    print("   (e.g., run 'export GEMINI_API_KEY=\"YOUR_API_KEY\"' in your terminal session)\n")

    # --- List of video files to process ---
    # !!! EDIT THIS LIST with paths to your video files !!!
    # Example:
    # videos_to_analyze = [
    #     "/path/to/your/video1.mp4",
    #     "another_video_in_current_directory.mov",
    #
    # ]
    # For testing, use short and small video files.
    videos_to_analyze = [
        "/Users/Kate/Documents/CWRU/RedHen/fulldatasetellen/30videos_vivitanno/11-11-1_shrug.mp4",
        "/Users/Kate/Documents/CWRU/RedHen/fulldatasetellen/30videos_vivitanno/11-11-2_twohandbeat.mp4",
        "/Users/Kate/Documents/CWRU/RedHen/fulldatasetellen/30videos_vivitanno/11-11-3_objloc(proximal).mp4",
        "/Users/Kate/Documents/CWRU/RedHen/fulldatasetellen/30videos_vivitanno/11-11-4_from(head).mp4",
        "/Users/Kate/Documents/CWRU/RedHen/fulldatasetellen/30videos_vivitanno/11-11-5_iconic(progression).mp4"
    ]

    if not videos_to_analyze:
        print("The 'videos_to_analyze' list in the script is currently empty.")
        print("Please edit the script and add the full paths to your video files.\n")
        # Example of how to add files if you're editing the script:
        # videos_to_analyze.append("my_test_video.mp4") # Assuming it's in the same directory

    if videos_to_analyze:
        analyze_video_gestures(videos_to_analyze)
    else:
        print("No video files specified for analysis. Exiting.")
