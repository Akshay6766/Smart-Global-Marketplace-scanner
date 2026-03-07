"""
Backup .kiro folder to AWS S3 - AUTOMATIC UPLOAD
Creates a zip archive and uploads to S3 automatically
"""

import os
import zipfile
import datetime
from pathlib import Path
import sys

# ============================================================================
# AWS CONFIGURATION - EDIT THESE VALUES
# ============================================================================
AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 'smart-product-finder-backup'  # Your EB bucket

# Optional: AWS credentials (leave empty to use AWS CLI configured credentials)
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

# ============================================================================

try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    print("Warning: boto3 not installed. Install with: pip install boto3")

def create_backup():
    source_dir = Path(r"C:\Users\Arora\.kiro")
    backup_dir = Path(r"C:\Users\Arora\kiro-backups")
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"kiro-backup-{timestamp}.zip"
    backup_path = backup_dir / backup_filename
    
    print("="*80)
    print("CREATING BACKUP OF .KIRO FOLDER")
    print("="*80)
    print(f"\nSource: {source_dir}")
    print(f"Destination: {backup_path}")
    print("\nCompressing files...")
    
    file_count = 0
    total_size = 0
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(source_dir.parent)
                try:
                    zipf.write(file_path, arcname)
                    file_count += 1
                    total_size += file_path.stat().st_size
                    if file_count % 100 == 0:
                        print(f"  Compressed {file_count} files...")
                except Exception as e:
                    print(f"  Warning: Could not add {file_path}: {e}")
    
    backup_size_mb = backup_path.stat().st_size / (1024 * 1024)
    
    print(f"\n Backup created successfully!")
    print(f"  Files: {file_count}")
    print(f"  Original size: {total_size / (1024 * 1024):.2f} MB")
    print(f"  Compressed size: {backup_size_mb:.2f} MB")
    print(f"  Location: {backup_path}")
    
    return backup_path, backup_size_mb, backup_filename

def upload_to_s3(backup_path, backup_filename):
    if not BOTO3_AVAILABLE:
        print("\n boto3 not installed. Cannot upload to S3.")
        print("Install with: pip install boto3")
        return False
    
    if S3_BUCKET_NAME == 'your-bucket-name':
        print("\n S3 bucket name not configured!")
        print("Edit the script and set S3_BUCKET_NAME")
        return False
    
    print("\n" + "="*80)
    print("UPLOADING TO AWS S3")
    print("="*80)
    
    try:
        # Create S3 client
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            s3 = boto3.client('s3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
            print("Using provided AWS credentials")
        else:
            s3 = boto3.client('s3', region_name=AWS_REGION)
            print("Using AWS CLI configured credentials")
        
        # Upload file
        s3_key = f'kiro-backups/{backup_filename}'
        print(f"\nUploading to: s3://{S3_BUCKET_NAME}/{s3_key}")
        print("Please wait...")
        
        s3.upload_file(
            str(backup_path),
            S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={'StorageClass': 'STANDARD_IA'}
        )
        
        print(f"\n Upload successful!")
        print(f"  S3 Location: s3://{S3_BUCKET_NAME}/{s3_key}")
        print(f"  Storage Class: STANDARD_IA (cost-optimized)")
        
        return True
        
    except Exception as e:
        print(f"\n Upload failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check AWS credentials are configured")
        print("2. Verify S3 bucket exists and you have write permissions")
        print("3. Check your internet connection")
        return False

if __name__ == "__main__":
    try:
        # Create backup
        backup_path, size_mb, backup_filename = create_backup()
        
        # Upload to S3
        if BOTO3_AVAILABLE:
            success = upload_to_s3(backup_path, backup_filename)
            if success:
                print("\n" + "="*80)
                print("BACKUP COMPLETE - LOCAL + S3")
                print("="*80)
            else:
                print("\n" + "="*80)
                print("BACKUP COMPLETE - LOCAL ONLY")
                print("="*80)
                print("S3 upload failed. Backup saved locally.")
        else:
            print("\n" + "="*80)
            print("BACKUP COMPLETE - LOCAL ONLY")
            print("="*80)
            print("Install boto3 for automatic S3 upload: pip install boto3")
        
    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback
        traceback.print_exc()
