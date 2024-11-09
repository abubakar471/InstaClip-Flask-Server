import logging
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def segment_candidates(candidates, video_file, filename):
    video_candidates_paths = []

    for index, candidate in enumerate(candidates):
        try:
            # Validate the 'discussion' field
            if "discussion" not in candidate or not isinstance(candidate["discussion"], list):
                logging.error(f"Candidate {index} has an invalid or missing 'discussion' field.")
                continue  # Skip to the next candidate if 'discussion' is invalid
            
            segment_filename = f"{filename}_{index}"
            out_path = candidate_to_video(candidate, video_file, segment_filename)
            video_candidates_paths.append(out_path)
        except Exception as e:
            logging.error(f"Error processing candidate {index}: {e}", exc_info=True)

    return video_candidates_paths

def candidate_to_video(transcription, video_file, filename):
    clips = []
    try:
        for transcribe in transcription["discussion"]:
            # Safely retrieve 'start' and 'end' values, defaulting to 0 if missing
            start = float(transcribe.get('start', 0))
            end = float(transcribe.get('end', 0))

            # Extract subclip and add to the list
            clip = VideoFileClip(video_file).subclip(start, end)
            clips.append(clip)

        # Define video resolution and output path
        height = 420
        aspect_ratio = (9, 16)
        width = int((height / aspect_ratio[1]) * aspect_ratio[0])
        out_path = f"C:/Users/AB/Downloads/{filename}.mp4"

        # Concatenate clips and write final video with specified fps
        # final_clip = concatenate_videoclips(clips, method="compose").resize(width=width, height=height)
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(out_path, fps=24, logger=None)

        # Clean up by closing each clip
        for clip in clips:
            clip.close()
        final_clip.close()

        return out_path

    except Exception as e:
        logging.error(f"Error creating video for '{filename}': {e}", exc_info=True)
        # Ensure all clips are closed in case of an error
        for clip in clips:
            clip.close()
        raise
