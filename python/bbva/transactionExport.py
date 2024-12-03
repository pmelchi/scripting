import os
from pypdf import PdfReader

parts = []
print_next = 0

visitors = ["visitor_page_start"]

# This visitor looks for the start of the transaction details
def visitor_page_start(text, cm, tm, font_dict, font_size):
    global parts
    global print_next

    if print_next > 0:
        print (text)
        print (cm)
        print (tm)
        parts.append(text)
        print_next -= 1

    if text == "Detalle de Movimientos Realizados":
        print (text)
        print (cm)
        print(tm)
        print_next = 2


# This function opens a PDF file with password and walks through all pages
def open_encrypted_pdf(file_path: str, password: str) -> PdfReader:
    """
    Opens a password-protected PDF file.
    
    Args:
        file_path (str): Path to the PDF file
        password (str): Password to decrypt the PDF
        
    Returns:
        PdfReader: Decrypted PDF reader object
        
    Raises:
        Exception: If file cannot be opened or decrypted
    """
    try:
        reader = PdfReader(file_path)
        
        if reader.is_encrypted:
            try:
                reader.decrypt(password)
            except Exception as e:
                raise Exception(f"Failed to decrypt PDF: {e}")
                
        return reader
        
    except Exception as e:
        raise Exception(f"Error opening PDF file: {e}")


# This function takes a PDF file with password and converts it to a CSV file
def convert_pdf_to_csv(pdf_file, password):
    # Check if the file exists
    if not os.path.exists(pdf_file):
        print("File does not exist")
        return

    # Check if the file is a PDF
    if not pdf_file.endswith(".pdf"):
        print("File is not a PDF")
        return

    # Check if the password is empty
    if password == "":
        print("Password is empty")
        return

    # Open the PDF file
    pdf_reader = open_encrypted_pdf(pdf_file, password)
      
    # Print all text from the PDF
    for page in pdf_reader.pages:
        page.extract_text(visitor_text=visitor_page_start)

    text_body = "".join(parts)

    print(text_body)

# This functions takes a path and looks for all PDF files in it, then calls the convert_pdf_to_csv function
def convert_all_pdfs_to_csv(path, password):
    # Check if the path exists
    if not os.path.exists(path):
        print("Path does not exist")
        return

    # Check if the path is a directory
    if not os.path.isdir(path):
        print("Path is not a directory")
        return

    # Get all files in the directory
    files = os.listdir(path)

    # Loop through all files
    for file in files:
        # Check if the file is a PDF
        if file.endswith(".pdf"):
            # Convert the PDF to CSV
            convert_pdf_to_csv(os.path.join(path, file), password) 

def main():

if __name__ == "__main__":
    main()