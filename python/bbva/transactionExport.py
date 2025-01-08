import os
import argparse
from pypdf import PdfReader
import re
import csv

# Write transactions to a CSV file
def write_transactions_to_csv(transactions, output_file):
    csv_headers = ["oper","liq","description","cargos","abonos", "saldo", "filename"]

    file_exists = os.path.isfile(output_file)
    with open(output_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        if not file_exists:
            writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)
    
    print(f"Transactions written to {output_file}")

# Function that looks at the text in the text_array and starts extracting the transaction details to a CSV file
def parse_text_to_array(text, pdf_file):
    # Identify the transactions section
    transactions_start = re.search(r"Detalle de Movimientos Realizados", text)
    transactions_end = re.search(r"Total de Movimientos", text)
    
    if transactions_start and transactions_end:
        transactions_text = text[transactions_start.end():transactions_end.start()]
    else:
        print("Transactions section not found")
        transactions_text = ""
    
    # Parse individual transactions
    transactions = []
    count = 0
    for line in transactions_text.split('\n'):
        match = re.search(r"(\d{2}\/\w{3})(\s*\d{2}\/\w{3})(\s*[^\d]*)(\s*[\d.,]+)(\s*[\d.,]*)(\s*[\d.,]*)", line)
        if match:
            if count < 10:
                print(match.groups())
                count+=1
            oper, liq, description, cargos, abonos, saldo = match.groups()
            transactions.append({
                'oper': oper,
                'liq': liq,
                'description': description,
                'cargos': convert_to_float_or_empty(cargos),
                'abonos': convert_to_float_or_empty(abonos),
                'saldo': convert_to_float_or_empty(saldo),
                'filename': os.path.basename(pdf_file)
            })
    
    return transactions

def convert_to_float_or_empty(value):
    value = value.replace(",", "")
    try:
        return float(value)
    except ValueError:
        return ""


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


# This function takes a PDF file with password and returs a text 
def convert_pdf_to_text(pdf_file, password, output_file):
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
    
    text_body = ""
    # Print all text from the PDF
    for page in pdf_reader.pages:
        text_body+=page.extract_text()

    transactions = parse_text_to_array(text_body, pdf_file)
    write_transactions_to_csv(transactions, output_file)
    

# This functions takes a path and looks for all PDF files in it, then calls the convert_pdf_to_csv function
def convert_all_pdfs_to_text(path, password, output_file):
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
            convert_pdf_to_text(os.path.join(path, file), password, output_file) 

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to CSV")
    parser.add_argument("pdf_folder", type=str, help="Path to the PDF files")
    parser.add_argument("password", type=str, help="Password to decrypt the PDF")
    parser.add_argument("output_file", type=str, help="Password to decrypt the PDF")
    
    args = parser.parse_args()
    
    convert_all_pdfs_to_text(args.pdf_folder, args.password, args.output_file)

if __name__ == "__main__":
    main()