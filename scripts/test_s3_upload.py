import requests

from app.modules.files.s3_service import S3Service


def main():
    service = S3Service()

    result = service.generate_upload_url(
        user_id="test-user-001",
        content_type="text/plain",
    )

    upload_url = result["upload_url"]

    response = requests.put(
        upload_url,
        data=b"Hello from FastAPI Cloud Storage!",
        headers={"Content-Type": "text/plain"},
    )

    print("Status:", response.status_code)
    print("Object key:", result["object_key"])

    if response.status_code == 200:
        print("File uploaded successfully!")
    else:
        print("Upload failed:", response.text)


if __name__ == "__main__":
    main()