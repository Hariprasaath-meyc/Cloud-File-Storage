


from app.modules.files.s3_service import S3Service


def main():
    result = S3Service.generate_upload_url(
        user_id="test-user-001",
        filename="sample.pdf",
        content_type="application/pdf",
    )

    print("Object key:", result["object_key"])
    print("Upload URL:", result["upload_url"])
    print("Expires in:", result["expires_in"], "seconds")


if __name__ == "__main__":
    main()