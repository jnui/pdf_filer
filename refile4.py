import os
import shutil
from pdf2image import convert_from_path
import pytesseract
import time
import ast

def convert_pdf_to_images(file_path):
    print(f"Converting PDF to images: {file_path}")
    return convert_from_path(file_path)

def extract_text_from_images(images):
    print("Extracting text from images...")
    full_text = ''
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text
    return full_text

def find_address_in_text(text, address):
    # Convert both text and address to lowercase for case-insensitive comparison
    return address.lower() in text.lower()

def load_address_list(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        # Read the content of the file and evaluate it as a Python expression
        content = file.read()
        address_list = ast.literal_eval(content)
    return address_list

def organize_pdfs_by_address(source_directory, address_list):
    file_count = 0
    match_count = 0
    
    # Create "DID NOT MATCH" directory if it doesn't exist
    did_not_match_folder = os.path.join(source_directory, 'DID NOT MATCH')
    if not os.path.exists(did_not_match_folder):
        os.makedirs(did_not_match_folder)
        
    for filename in os.listdir(source_directory):
        if filename.endswith('.pdf'):
            file_count += 1
            file_path = os.path.join(source_directory, filename)
            print(f"Processing file: {filename}")
            
            images = convert_pdf_to_images(file_path)
            text = extract_text_from_images(images)
            
            addresses_matched = []
            for name, address in address_list:
                if find_address_in_text(text, address):
                    print(f" matched {address}")
                    folder_name = f"{name} {address}"
                    destination_folder = os.path.join(source_directory, folder_name)
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    addresses_matched.append(destination_folder)
                    
            if addresses_matched:
                match_count += len(addresses_matched)
                print(f" found {match_count} matches")
                for destination_folder in addresses_matched:
                    # Copy to all matched destinations
                    shutil.copy(file_path, os.path.join(destination_folder, filename))
                    print(f"Copied {filename} to folder: {destination_folder}")
                
                # After copying to all folders, delete the original file
                os.remove(file_path)
                print(f"Deleted original file: {filename}")
                
            else:
                # Move the file to the "DID NOT MATCH" folder
                shutil.move(file_path, os.path.join(did_not_match_folder, filename))
                print(f"Moved {filename} to DID NOT MATCH folder.")
            
        print(f"==================")
        
    return file_count, match_count

if __name__ == "__main__":
    # Start the timer
    start_time = time.time()

    # Example usage
    source_directory = 'scans'
    address_file = 'list.txt'
    
    # Load address list from file
    address_list = load_address_list(address_file)
    
    # Organize PDFs and get counts
    file_count, match_count = organize_pdfs_by_address(source_directory, address_list)

    # End the timer
    end_time = time.time()
    time_taken = end_time - start_time

    # Calculate minutes and seconds from the time_taken
    minutes = int(time_taken // 60)
    seconds = int(time_taken % 60)

    # Print summary
    print(f"Script finished, {file_count} files scanned, {match_count} matches found, time taken {minutes} minutes {seconds} seconds")
