import subprocess

def rotate_logs():
    """call the logger.sh rotate_logs function"""
    subprocess.call(['bash', 'utils/logger.sh', 'rotate_logs'])

def encrypt_log(log_file, key):
    """call the logger.sh encrypt_log function"""
    subprocess.call(['bash', 'utils/logger.sh', 'encrypt_log', log_file, key])