# Plagium Website

This repository contains the website for the plagiarism detection project. It allows to interact with the main core of the project using a web interface, with a hand made library to use python3 default libraries to generate the website.

## Usage

To use the website you need to open the [index.html](./index.html) file in your browser, then you can add as many files as you want to process and then click the process button to receive the results.

## Deployment

You can deploy the website using a docker container, for that purpose you can use the [Dockerfile](./Dockerfile) file to build the image and then run it with the following commands:

```bash
docker build -t plagium_web .
docker run -d -p 80:80 plagium_web
```