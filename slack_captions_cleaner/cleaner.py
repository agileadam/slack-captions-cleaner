#!/usr/bin/env python
from bs4 import BeautifulSoup
import re
import sys
import argparse

def convert_html_to_text(html_content, remove_fillers=False, filler_words=None, redact_words=None):
    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.find_all('div', {'class': 'c-virtual_list__item'})
    
    output_text = ""
    prev_speaker = None
    prev_message_type = None  # "message" or "event"
    current_message = ""
    current_timestamp = None
    
    if filler_words is None:
        filler_words = ["Hm.", "Mhm."]
    
    for item in items:
        timestamp_element = item.find('span', {'class': 'p-huddle_event_log__timestamp'})
        if timestamp_element:
            current_timestamp = timestamp_element.text.strip()
        
        name_element = item.find('div', {'class': 'p-huddle_event_log__member_name'})
        if name_element:
            name = name_element.text.strip()
            
            transcription = item.find('span', {'class': 'p-huddle_event_log__transcription'})
            meta_text = item.find('span', {'class': 'p-huddle_event_log__meta_text'})
            
            if transcription:
                message_type = "message"
                content = transcription.text.strip()
                
                if remove_fillers:
                    # Skip if the entire message is just a filler word
                    if content in filler_words:
                        continue
                    
                    # Remove filler words from anywhere in the message
                    words = content.split()
                    filtered_words = []
                    for word in words:
                        # Check if the word is a filler word (with or without a period)
                        is_filler = False
                        for filler in filler_words:
                            if word == filler or word == filler + "." or word == filler + ". ":
                                is_filler = True
                                break
                        if not is_filler:
                            filtered_words.append(word)
                    content = " ".join(filtered_words).strip()
                    
                    # Skip if we removed all words
                    if not content:
                        continue
                
                if redact_words:
                    for word in redact_words:
                        content = content.replace(word, "<REDACTED>")
                        
            elif meta_text:
                message_type = "event"
                content = meta_text.text.strip()
            else:
                continue
            
            if prev_speaker != name or prev_message_type != message_type:
                if prev_speaker:
                    if prev_message_type == "message":
                        output_text += f"{current_timestamp} {prev_speaker}: {current_message}\n\n"
                    else:  # event
                        output_text += f"{current_timestamp} {prev_speaker} {current_message}\n\n"
                
                current_message = content
                prev_speaker = name
                prev_message_type = message_type
            else:
                current_message += f" {content}"
    
    if prev_speaker:
        if prev_message_type == "message":
            output_text += f"{current_timestamp} {prev_speaker}: {current_message}\n\n"
        else:  # event
            output_text += f"{current_timestamp} {prev_speaker} {current_message}\n\n"
    
    return output_text

def main():
    parser = argparse.ArgumentParser(description='Convert Slack HTML conversation to plain text.')
    parser.add_argument('input_file', help='HTML file to convert')
    parser.add_argument('-f', '--filler-words', nargs='*', default=None,
                        help='Remove filler words. If no words provided, uses defaults ("Hm", "Mhm").')
    parser.add_argument('-r', '--redact', nargs='+', default=None,
                        help='Replace specified words with "<REDACTED>"')
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # If -f was used but no words provided, use defaults
        remove_fillers = args.filler_words is not None
        filler_words = args.filler_words if args.filler_words else ["Hm", "Mhm"]
        
        text_content = convert_html_to_text(
            html_content, 
            remove_fillers=remove_fillers, 
            filler_words=filler_words,
            redact_words=args.redact
        )
        print(text_content, end='')
        
        if remove_fillers:
            print(f"Filler words were removed from the conversation: {', '.join(filler_words)}", file=sys.stderr)
        if args.redact:
            print(f"Words were redacted from the conversation: {', '.join(args.redact)}", file=sys.stderr)
        
    except FileNotFoundError:
        print(f"Error: The file '{args.input_file}' was not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
