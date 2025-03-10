FROM python:3.9.13-slim

WORKDIR /app

# ติดตั้ง dependencies ที่จำเป็น
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# เปิด port 5000 สำหรับ API
EXPOSE 5000

# รัน application
CMD ["python", "src/app.py"]