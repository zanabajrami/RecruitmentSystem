import uuid
import os

def generate_unique_filename(filename: str) -> str:
    """
    Securely generates a completely unique filename using UUID4 
    to prevent file naming conflicts and overwrites in production storage.
    """
    # Split the filename into a tuple containing the base name and the extension (e.g., '.pdf')
    _, extension = os.path.splitext(filename)
    
    # Fallback to a default '.pdf' extension if no extension was provided in the original file
    if not extension:
        extension = ".pdf"
        
    # Generate a randomly unique 36-character string (UUIDv4) and append the secure extension
    return f"{uuid.uuid4()}{extension}"