import re
import os

def preprocess_file_content(raw_text) -> str:
    """
    Removes potential "" annotations from the beginning of lines.
    These annotations might appear if the content is fetched via certain tools
    but ideally shouldn't be in the raw file content string.
    """
    lines = raw_text.split('\n')
    actual_content_lines = []
    for line in lines:
        cleaned_line = re.sub(r'^\\s*', '', line)
        actual_content_lines.append(cleaned_line)
    return "\n".join(actual_content_lines)

def process_subtitles(srt_content_raw) -> str:
    """
    Processes SRT content to merge subtitle entries into pairs.
    - Each new entry will contain two lines of text from two original consecutive entries.
    - The timestamp of the new entry will span from the start of the first original entry
      to the end of the second original entry.
    - Groups are numbered sequentially.
    - An empty line separates each new group.
    """
    # Preprocess content (optional, but a safeguard)
    srt_content = preprocess_file_content(srt_content_raw)

    # Split entries by one or more empty lines.
    # .strip() removes leading/trailing whitespace from the whole content before splitting.
    entries = srt_content.strip().split('\n\n')
    
    parsed_entries = []
    for entry_block_text in entries:
        # Skip if the block is entirely empty or whitespace after stripping
        if not entry_block_text.strip(): 
            continue
            
        lines = entry_block_text.strip().split('\n')
        
        # Expecting at least: index, timestamp, first text line
        if len(lines) >= 3: 
            index_str = lines[0]
            timestamp_str = lines[1]
            # Text can potentially span multiple lines in the original file per entry,
            # though the example implies one. This joins them.
            text_content = "\n".join(lines[2:]) 
            
            try:
                # Validate index string (e.g., it's a number)
                int(index_str)
                
                # Validate timestamp format
                if '-->' not in timestamp_str:
                    # print(f"Warning: Malformed timestamp in entry, skipping: {timestamp_str[:30]}")
                    continue

                start_time_original, end_time_original = timestamp_str.split(' --> ')
                
                parsed_entries.append({
                    "start_time": start_time_original.strip(),
                    "end_time": end_time_original.strip(),
                    "text": text_content.strip() # Strip whitespace from text itself
                })
            except ValueError:
                # print(f"Warning: Malformed index or unable to parse entry, skipping: {entry_block_text[:50]}")
                continue
        # else:
            # print(f"Warning: Entry with insufficient lines, skipping: {entry_block_text[:50]}")


    output_srt_parts = []
    new_group_index = 1
    
    i = 0
    # Process entries in pairs
    while i + 1 < len(parsed_entries):
        entry1 = parsed_entries[i]
        entry2 = parsed_entries[i+1]
        
        # Keep initial time of the first group for the new group
        new_start_time = entry1["start_time"]
        # Use final time of the second group for the new group
        new_end_time = entry2["end_time"] 
        
        # Combine text from the two original groups, separated by a newline
        combined_text = f"{entry1['text']}\n{entry2['text']}"
        
        output_srt_parts.append(str(new_group_index))
        output_srt_parts.append(f"{new_start_time} --> {new_end_time}")
        output_srt_parts.append(combined_text)
        
        # Add an empty line between new groups, but not after the very last one.
        if i + 2 < len(parsed_entries): # Checks if another pair will be processed
            output_srt_parts.append("") 
        
        new_group_index += 1
        i += 2
        
    # Join all parts to form the final SRT string.
    final_output_str = "\n".join(output_srt_parts)
    
    # Ensure a single trailing newline if content exists, for POSIX compliance/readability
    if final_output_str:
        final_output_str = final_output_str.strip() # Remove any existing excess newlines
        if final_output_str: # If not empty after strip
            final_output_str += "\n"
             
    return final_output_str

def main() -> None:
    """Main function to run the program."""
    input_filename = input("Please enter the name of the input subtitle file (e.g., video.srt): ")

    # Derive the output filename
    base_name, _ = os.path.splitext(input_filename)
    output_filename = f"{base_name}-result.srt"

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            video_file_content = f.read()
        
        if not video_file_content.strip():
            print(f"The input file '{input_filename}' is empty or contains only whitespace. Nothing to process.")
        else:
            modified_subtitles = process_subtitles(video_file_content)
            
            with open(output_filename, 'w', encoding='utf-8') as outfile:
                outfile.write(modified_subtitles)
            print(f"Processed subtitles saved to '{output_filename}'")
            
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found. Please check the file name and path.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()