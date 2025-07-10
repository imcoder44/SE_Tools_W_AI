#!/bin/bash
# Advanced Log Management Utilities

LOG_DIR="logs"
CURRENT_LOG="$LOG_DIR/events.log"
ARCHIVE_DIR="$LOG_DIR/archive"
RETENTION_DAYS=$(grep 'retention_days' config/settings.yaml | awk '{print $2}')

# Rotate logs based on size and age
# rotate_logs() {
#     if [ -f "$CURRENT_LOG" ]; then
#         # Create archive directory if needed
#         if [ ! -d "$ARCHIVE_DIR" ]; then
#             mkdir -p "$ARCHIVE_DIR"
#         fi
        
#         # Rotate if older than 1 day or larger than 10MB
#         if [ $(find "$CURRENT_LOG" -mtime +0 -o -size +10M | wc -l) -eq 1 ]; then
#             TIMESTAMP=$(date +%Y%m%d_%H%M%S)
#             mv "$CURRENT_LOG" "$ARCHIVE_DIR/events_$TIMESTAMP.log"
#             touch "$CURRENT_LOG"
            
#             # Apply retention policy
#             find "$ARCHIVE_DIR" -name "*.log" -mtime +$RETENTION_DAYS -exec rm {} \;
#         fi
#     fi
# }
if [ "$1" == "rotate_logs" ]; then
     if [ -f "$CURRENT_LOG" ]; then
        # Create archive directory if needed
        if [ ! -d "$ARCHIVE_DIR" ]; then
            mkdir -p "$ARCHIVE_DIR"
        fi
        
        # Rotate if older than 1 day or larger than 10MB
        if [ $(find "$CURRENT_LOG" -mtime +0 -o -size +10M | wc -l) -eq 1 ]; then
            TIMESTAMP=$(date +%Y%m%d_%H%M%S)
            mv "$CURRENT_LOG" "$ARCHIVE_DIR/events_$TIMESTAMP.log"
            touch "$CURRENT_LOG"
            
            # Apply retention policy
            find "$ARCHIVE_DIR" -name "*.log" -mtime +$RETENTION_DAYS -exec rm {} \;
        fi
    fi
fi

# Encrypt logs using AES-256
# encrypt_log() {
#     LOG_FILE=$1
#     KEY=$2
    
#     if [ -f "$LOG_FILE" ]; then
#         openssl enc -aes-256-cbc -salt -in "$LOG_FILE" -out "${LOG_FILE}.enc" -pass pass:"$KEY" 2>/dev/null
#         if [ $? -eq 0 ]; then
#             rm -f "$LOG_FILE"
#         fi
#     fi
# }

if [ "$1" == "encrypt_log" ]; then
    LOG_FILE=$2
    KEY=$3
    
    if [ -f "$LOG_FILE" ]; then
        openssl enc -aes-256-cbc -salt -in "$LOG_FILE" -out "${LOG_FILE}.enc" -pass pass:"$KEY" 2>/dev/null
        if [ $? -eq 0 ]; then
            rm -f "$LOG_FILE"
        fi
    fi
fi

# Decrypt logs (for authorized access only)
decrypt_log() {
    ENC_FILE=$1
    KEY=$2
    
    if [ -f "${ENC_FILE}" ]; then
        openssl enc -d -aes-256-cbc -in "${ENC_FILE}" -out "${ENC_FILE%.enc}" -pass pass:"$KEY" 2>/dev/null
    fi
}