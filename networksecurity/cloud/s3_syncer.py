import os

class S3Sync:
    def sync_folder_to_s3(self,folder,aws_bucker_url):
        """To upload data from local to aws s3 bucket"""
        command = f"aws s3 sync {folder} {aws_bucker_url}"
        os.system(command)
        
    def sync_folder_from_s3(self,folder,aws_bucket_url):
        """To sync data from aws s3 bucket to local"""
        command = f"aws s3 sync {aws_bucket_url} {folder}"
        os.system(command)