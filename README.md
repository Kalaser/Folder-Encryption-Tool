# which provides a GUI for encrypting and decrypting files in a folder
# Folder Encryption Tool

This Python application provides a user-friendly graphical interface for encrypting and decrypting all files within a selected folder using the **Fernet symmetric encryption** method. It allows users to:

- **Generate a Key**: Create a secure encryption key and save it for later use.
- **Encrypt Files**: Encrypt all files in a chosen folder using the generated key.
- **Decrypt Files**: Decrypt all encrypted files in a folder using the key.

The tool supports progress tracking for long operations, and users can cancel the task at any time.

## Features:
1. **Key Generation**: Create a unique encryption key using `Fernet` encryption. The key is saved to a file (`key.key`) and can be reused for subsequent encryption and decryption tasks.
2. **Folder Processing**: Select a folder, and the tool will automatically encrypt or decrypt all files in that folder, including files within subdirectories.
3. **Progress Tracking**: A progress bar tracks the encryption/decryption process, with the ability to cancel the operation at any point.
4. **Multithreading**: The app runs the encryption or decryption task in a separate thread to keep the UI responsive.

## How to Use:
1. Click **"Generate Key"** to create and save a new encryption key.
2. Select **"Encrypt Folder"** to encrypt the files in a folder.
3. Select **"Decrypt Folder"** to decrypt the previously encrypted files in a folder.
4. Use the **"Cancel"** button to stop the process during encryption or decryption.

## Technical Details:
- **Library Used**: `cryptography.fernet` for symmetric encryption.
- **UI Framework**: `tkinter` for the graphical user interface.
- **Multithreading**: Using Python's `threading` module to ensure the UI remains responsive during long-running encryption/decryption tasks.

---

This tool is suitable for users who need to secure their files quickly and easily without manually handling encryption algorithms.
