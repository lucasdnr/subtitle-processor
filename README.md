# Subtitle Processor

## Description

This Python script processes subtitle files (commonly in SRT or VTT-like format, though it expects a simple numbered block structure) to reformat them. The primary function is to take subtitle entries that display one line of text per timestamped group and merge them so that each new timestamped group displays two lines of text.

Specifically, it will:
1.  Read an input subtitle file.
2.  Parse the subtitle entries (index, timestamp, and text).
3.  Combine consecutive pairs of subtitle entries into a single new entry.
    * The new entry will start with the timestamp of the first entry in the pair.
    * The new entry will end with the timestamp of the second entry in the pair.
    * The text from both original entries will be combined, with the first entry's text on the first line and the second entry's text on the second line.
    * The new entries are re-indexed sequentially (1, 2, 3...).
4.  Save the processed subtitles to a new output file. The output file will have the same name as the input file, but with "-result.srt" appended to its base name (e.g., if input is `video.srt`, output will be `video-result.srt`).

## Features

* Prompts the user for the input subtitle file name.
* Automatically generates the output file name based on the input file name.
* Handles basic SRT-like structure (index, timestamp `-->` text, separated by blank lines).
* Merges pairs of subtitle lines into a two-line format under a combined timestamp.
* Includes basic error handling for file operations (e.g., file not found).

## Prerequisites

* Python 3.x installed on your system.

## How to Use

1.  **Save the Script**: Save the Python code provided in the previous response to a file named `process_srt.py` (or any other `.py` name you prefer) on your computer.

2.  **Prepare Your Subtitle File**: Ensure the subtitle file you want to process is accessible on your computer. The script expects a format like:
    ```
    1
    00:00:00,000 --> 00:00:06,300
    First line of text.

    2
    00:00:06,300 --> 00:00:07,980
    Second line of text.

    3
    00:00:07,980 --> 00:00:09,450
    Third line of text.
    ```
    (Note: The script includes a preprocessing step to try and remove `` tags that might appear if content is copied from certain outputs, but ideally, the input file should be clean.)

3.  **Run the Script**:
    * Open a terminal or command prompt.
    * Navigate to the directory where you saved `process_srt.py`.
    * Execute the script using the command:
        ```bash
        python process_srt.py
        ```

4.  **Enter Input File Name**:
    * The script will prompt you:
        ```
        Please enter the name of the input subtitle file (e.g., video.srt or video.srt):
        ```
    * Type the full name of your input subtitle file (e.g., `my_subtitles.srt`) and press Enter. If the file is not in the same directory as the script, you might need to provide the full path to the file.

5.  **Processing and Output**:
    * The script will process the file.
    * It will automatically determine the output file name. For example, if your input was `my_subtitles.srt`, the output will be saved as `my_subtitles-result.srt` in the same directory where you ran the script.
    * You will see a confirmation message:
        ```
        Processed subtitles saved to 'my_subtitles-result.srt'
        ```
    * If there are any errors (e.g., input file not found), an error message will be displayed.