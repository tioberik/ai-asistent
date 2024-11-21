# Korak 1: Koristite Python kao osnovnu sliku za izgradnju
FROM python:3.9-slim

# Postavite radni direktorij
WORKDIR /app

# Kopirajte datoteke aplikacije u radni direktorij
COPY . .

# Instalirajte potrebne Python pakete
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (Flask default)
EXPOSE 5000

# Pokrenite Flask aplikaciju
#CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["python", "app.py"]
