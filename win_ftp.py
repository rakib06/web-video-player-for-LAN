import http.server
import os
from urllib.parse import unquote

# Set the path to your Downloads folder
downloads_folder = r"C:\Users\rakibul\Nobody"
os.chdir(downloads_folder)  # Change the working directory to Downloads

# Supported video file extensions
video_extensions = ('.mp4', '.mkv', '.webm', '.avi', '.mov')

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the list of video files with thumbnails
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Create an HTML response with embedded video thumbnails
            self.wfile.write(b"<html><head><title>Video Files</title></head>")
            self.wfile.write(b"<body><h1>Video Files</h1><ul>")

            # List video files in the Downloads folder
            for file in os.listdir():
                if file.endswith(video_extensions):
                    # Embed the video as a small thumbnail and make it clickable for full view
                    video_tag = f'''
                    <li>
                        <video width="200" controls="controls" preload="metadata">
                            <source src="/{file}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        <p>{file}</p>
                    </li>
                    '''
                    self.wfile.write(video_tag.encode())

            self.wfile.write(b"</ul></body></html>")
        else:
            # For any other path, serve the file as usual (like a video file)
            self.path = unquote(self.path)  # Decode URL-encoded characters
            return super().do_GET()

# Set up the server
httpd = http.server.HTTPServer(('127.0.0.1', 4443), CustomHTTPRequestHandler)

print("Serving HTTP on http://127.0.0.1:4443")
httpd.serve_forever()