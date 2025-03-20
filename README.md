# Slack Captions Cleaner

A simple Python script to clean up Slack Huddle captions.

## Getting Captions from Slack

1. Enable automatic captions in Slack:
   - Go to your Slack Huddle settings
   - Turn on automatic captions
   - This will generate captions for all future huddles

2. After your huddle, to save the captions:
   - WARNING: You must copy the captions (using the steps below) BEFORE you leave/close the huddle window.
   - In the captions panel, click the first message (or last message)
   - Hold Shift and click the last message (or first message) to select all captions
   - Right-click and select "Copy"
   - Open a text editor and paste the content
   - Save the file with a `.html` extension (e.g., `meeting.html`)

## Installation

1. Make sure you have `pipx` installed. If not, install it with:
   ```bash
   python -m pip install --user pipx
   python -m pipx ensurepath
   ```
   
   or

   ```
   brew install pipx
   ```

2. Clone this repository and install the package:
   ```bash
   git clone https://github.com/agileadam/slack-captions-cleaner.git
   cd slack-captions-cleaner
   pipx install .
   ```

## Usage

```bash
slack-captions-cleaner input.txt
```

The script will output the cleaned text to stdout, which means you can:

- Save the output to a file:
  ```bash
  slack-captions-cleaner input.txt > output.txt
  ```

- View the output in a pager (like `less`):
  ```bash
  slack-captions-cleaner input.txt | less
  ```

- Pipe the output to other commands:
  ```bash
  slack-captions-cleaner input.txt | grep "specific text"
  slack-captions-cleaner input.txt | wc -l  # count lines
  ```

### Options

- `-f` or `--filler-words`: Remove filler words. If no words provided, uses defaults ("Hm.", "Mhm.")
- `-r` or `--redact`: Replace specified words with "<REDACTED>"

Examples:
```bash
# Remove default filler words
slack-captions-cleaner input.txt -f

# Remove custom filler words
slack-captions-cleaner input.txt -f "Um" "Uh" "Like"

# Redact specific words
slack-captions-cleaner input.txt -r "password" "secret"

# Combine options
slack-captions-cleaner input.txt -f "Um" "Uh" -r "password" "secret"
```

When removing filler words:
- Entries containing only filler words are removed entirely
- Filler words are removed from anywhere in the message (start, middle, or end)
- If removing filler words leaves nothing behind, the entry is removed
- Filler words with periods are handled intelligently:
  - "Hm." will be removed
  - "Hm ." (with a space after the period) will be removed
  - "Hm" (without a period) will be removed
  - The rest of the message will be preserved

When redacting words:
- Each occurrence of the specified word is replaced with "<REDACTED>"
- Redaction is case-sensitive
- Multiple words can be redacted at once

## Features

- Converts copied/pasted Slack huddle captions to clean, readable text
- Preserves and formats timestamps at the start of each line (e.g., [00:12:00])
- Maintains speaker names and formats them consistently (e.g., "Speaker Name: ")
- Combines adjacent entries by the same speaker into single messages
- Distinguishes between regular messages and event notifications
- Optional removal of filler words (like "Hm.", "Mhm.") with -f flag
- Customizable list of filler words to remove
- Optional redaction of sensitive words with -r flag
- Removes empty lines and extra whitespace
- Outputs to stdout for maximum flexibility with Unix pipes and redirections