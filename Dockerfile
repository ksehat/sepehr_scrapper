# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR C:\Users\Administrator\Desktop\Projects\sepehr_fids_scrapper\sepehr_scrapper

# Copy the current directory contents into the container at /app
COPY . /fids_scraper

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Set environment variables
ENV NAME fids_scraper

# Run fids_scraper.py when the container launches
CMD ["python", "fids_scraper.py"]
