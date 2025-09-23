#!/usr/bin/env python3
"""
Simple Python web server for deployment testing
"""
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Django Doctor Appointment System - Deployed!</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { 
                        font-family: Arial, sans-serif; 
                        margin: 0; 
                        padding: 40px; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    .container { 
                        background: white; 
                        padding: 40px; 
                        border-radius: 10px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 600px;
                    }
                    h1 { 
                        color: #333; 
                        margin-bottom: 20px;
                        font-size: 2.5em;
                    }
                    .success { 
                        color: #28a745; 
                        font-size: 1.2em;
                        margin: 20px 0;
                    }
                    .info { 
                        background: #f8f9fa; 
                        padding: 20px; 
                        border-radius: 5px;
                        margin: 20px 0;
                        text-align: left;
                    }
                    .btn {
                        display: inline-block;
                        padding: 12px 24px;
                        margin: 10px;
                        background: #007bff;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        transition: background 0.3s;
                    }
                    .btn:hover {
                        background: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🏥 Django Doctor Appointment System</h1>
                    <div class="success">✅ Successfully Deployed to Azure!</div>
                    <div class="info">
                        <p><strong>🎉 Congratulations!</strong></p>
                        <p>Your Django Doctor Appointment System is now running live on Azure Web App.</p>
                        <br>
                        <p><strong>📊 Deployment Details:</strong></p>
                        <ul>
                            <li><strong>Platform:</strong> Microsoft Azure Web App</li>
                            <li><strong>Container:</strong> Docker with Python 3.11</li>
                            <li><strong>CI/CD:</strong> GitHub Actions</li>
                            <li><strong>Status:</strong> Online and Accessible</li>
                            <li><strong>URL:</strong> https://django-doctor-appointment.azurewebsites.net</li>
                        </ul>
                        <br>
                        <p><strong>🚀 Next Steps:</strong></p>
                        <ul>
                            <li>Set up PostgreSQL database connection</li>
                            <li>Configure Django models and migrations</li>
                            <li>Add authentication and user management</li>
                            <li>Implement appointment booking features</li>
                        </ul>
                    </div>
                    <div>
                        <a href="https://github.com/joiceantony27/django-doctor-appointment" class="btn">View on GitHub</a>
                        <a href="/health" class="btn">Health Check</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f'Server running on port {port}')
    server.serve_forever()
