
if __name__ == "__main__":
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    print("Accessing Storage Vault: ancient\\_fragment.txt\n"
          "Connection established...\n")
    try:
        f = open("ancient_fragment.txt", "rt")
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")
    else:
        print(f.read(), '\n')
        f.close()
        print("Data recovery complete. Storage unit disconnected.")
