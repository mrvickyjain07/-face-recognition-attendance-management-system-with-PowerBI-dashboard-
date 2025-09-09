import time
import threading
import requests
import os

def keep_alive():
    """Function to ping the application URL at regular intervals to prevent spin-down"""
    app_url = os.environ.get('APP_URL')
    
    if not app_url:
        print("Warning: APP_URL environment variable not set. Keep-alive functionality disabled.")
        return
    
    interval = int(os.environ.get('PING_INTERVAL', 840))  # Default to 14 minutes (840 seconds)
    
    def ping_app():
        while True:
            try:
                response = requests.get(app_url)
                print(f"Ping sent to {app_url}, status: {response.status_code}")
            except Exception as e:
                print(f"Error pinging {app_url}: {str(e)}")
            
            # Sleep for the specified interval
            time.sleep(interval)
    
    # Start the ping thread
    ping_thread = threading.Thread(target=ping_app, daemon=True)
    ping_thread.start()
    print(f"Keep-alive service started, pinging {app_url} every {interval} seconds")

# This can be imported and called from app.py
# Example usage in app.py:
# if os.environ.get('ENABLE_KEEP_ALIVE') == 'true':
#     from keep_alive import keep_alive
#     keep_alive()