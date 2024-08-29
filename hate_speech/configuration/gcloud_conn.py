import os

class GCloudSync:
    def sync_folder_to_gcloud(self, gcp_bucket_name, filepath, filename):
        command = f"gsutil cp {filepath}/{filename} gs://{gcp_bucket_name}/"
        os.system(command)

    def sync_folder_from_gcloud(self, gcp_bucket_name, filename, destination):
        command = f"gsutil cp gs://{gcp_bucket_name}/{filename} {destination}/{filename}"
        os.system(command)