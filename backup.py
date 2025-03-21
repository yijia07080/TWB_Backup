import os
import shutil
import zipfile
import subprocess
from datetime import datetime

def zip_folders(base_path, folder_names, save_dir):
    shutil.rmtree(save_dir)
    print(f"Deleted {save_dir}")
    os.makedirs(save_dir)
    print(f"Created {save_dir}")
    with zipfile.ZipFile(f'{save_dir}/backup.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder_name in folder_names:
            folder_path = os.path.join(base_path, folder_name)
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, base_path)
                    zipf.write(file_path, arcname)
            print(f"Added   {folder_path}")

def upload_to_github(zip_filename, repo_path, commit_message):
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
    subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path, check=True)
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_path, check=True)

def split_backup_zip(backup_zip_path, split_size):
    output_path = backup_zip_path.replace("backup.zip", "backup_split.zip")
    subprocess.run(
        ["zip", "-s", split_size, backup_zip_path, "--out", output_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    os.remove(backup_zip_path)

save_dir = "/home/eccdna/backup"
base_path = "/home/eccdna"
folder_names = [
    "bash_tool",
    "eccdna",
    "eccdna_dbtest_data",
    "flow_eccDNA",
    "flow_metadata",
    "public_html"
]

zip_folders(base_path, folder_names, save_dir)
print("Backup complete.")

split_backup_zip(f"{save_dir}/backup.zip", "95m")
print("Backup split complete.")

current_date = datetime.now().strftime("%Y%m%d")
commit_message = f"{current_date}"
upload_to_github(save_dir, base_path, commit_message)
print("Upload complete.")
