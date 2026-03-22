FROM python:3.11-slim

WORKDIR /app

# copy everything
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose port
EXPOSE 8000

# run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]