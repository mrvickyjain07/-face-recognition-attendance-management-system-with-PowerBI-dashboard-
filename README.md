# Face Recognition Attendance Management System

This is a Flask-based face recognition attendance management system with a PowerBI dashboard. The application uses OpenCV, dlib, and face_recognition libraries to detect and recognize faces, and stores attendance data in a database.

## Features

- Face recognition-based attendance tracking
- Dashboard with attendance statistics
- Student registration through webcam
- Daily and historical attendance reports

## Deployment Guide for Render.com (Free Tier)

This guide will help you deploy the application on Render.com's free tier.

### Prerequisites

1. A [Render.com](https://render.com) account
2. Your project code in a Git repository (GitHub, GitLab, etc.)

### Step 1: Prepare Your Repository

Make sure your repository includes all the necessary files:
- app.py
- database.py
- requirements.txt
- Procfile
- render.yaml
- Training images folder with sample images

### Step 2: Create a New Web Service on Render

1. Log in to your Render.com account
2. Click on "New +" and select "Blueprint"
3. Connect your Git repository
4. Render will automatically detect the render.yaml file and configure your services

### Step 3: Configure Environment Variables

The render.yaml file already includes the necessary environment variables, but you can add more if needed:

- `FLASK_ENV`: Set to "production" for production deployment
- `DATABASE_URL`: This will be automatically set by Render based on your database configuration

### Step 4: Deploy Your Application

1. Click "Apply" to create the services defined in your render.yaml file
2. Render will automatically build and deploy your application
3. Once deployment is complete, you can access your application at the provided URL

### Important Considerations for Free Tier

1. **Service Spin-down**: Render's free tier web services spin down after 15 minutes of inactivity. The first request after inactivity will take some time to respond while the service spins up.

2. **Database Expiration**: Free PostgreSQL databases on Render expire after 90 days. Make sure to back up your data before this period ends.

3. **Usage Limits**: Free tier includes 750 hours of service per month. If you exceed this limit, your service will be suspended until the next month.

4. **Service-Initiated Traffic**: Render may suspend services that initiate an uncommonly high volume of traffic. To avoid this:
   - Minimize external API calls
   - Avoid continuous background processes
   - Implement proper caching strategies

5. **Memory Optimization**: Face recognition can be memory-intensive. The application has been optimized for lower memory usage by:
   - Using the HOG model instead of CNN
   - Reducing image resolution during processing
   - Implementing caching for face encodings

### Keeping Your Service Active

The application includes a built-in keep-alive mechanism to prevent your service from spinning down due to inactivity. This works by having the application ping itself at regular intervals.

To enable this feature:

1. After deployment, go to your service's environment variables in the Render dashboard
2. Set `ENABLE_KEEP_ALIVE` to `true`
3. Set `APP_URL` to your application's URL (e.g., `https://your-app-name.onrender.com`)
4. Set `PING_INTERVAL` to `840` (14 minutes in seconds, just under Render's 15-minute inactivity threshold)

Alternatively, you can use external services like [UptimeRobot](https://uptimerobot.com/) to ping your application regularly.

### Memory Optimization for Face Recognition

Face recognition can be memory-intensive. The application has been optimized for lower memory usage by:

- Using the HOG model instead of CNN for face detection
- Reducing image resolution during processing
- Implementing caching for face encodings
- Processing fewer frames during recognition

## Local Development

### Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`

### Usage

1. Access the application at `http://localhost:5000`
2. Register students using the registration form
3. Use the recognition feature to mark attendance
4. View attendance reports and dashboard

## License

This project is licensed under the MIT License - see the LICENSE file for details.