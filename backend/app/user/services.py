from fastapi import UploadFile
from pusher.pusher import os
from sqlalchemy.orm import Session

from app.models import Users


DEFAULT_CHUNK_SIZE = 1024 * 1024 * 1  # 1 megabyte


class ImageSaver:
    def __init__(self, db: Session, *, user: Users):
        self.db: Session = db
        self.user: Users = user

    async def save_user_image(
        self, user: Users, uploaded_image: UploadFile
    ) -> str | None:
        file_extension: str = uploaded_image.filename.split(".")[-1].lower()
        filename: str = f"{user.username}.{file_extension}"

        # match settings.ENVIRONMENT:
        #     case "development":
        return await self._save_image_to_static(user, uploaded_image, filename)
        # case "production":
        #     return await self._save_image_to_aws_bucket(
        #         user, uploaded_image, filename
        #     )
        # case _:
        #     logger.error(f"Unsupported environment: {settings.ENVIRONMENT}")
        #     return None

    async def _save_image_to_static(
        self, user: Users, uploaded_image: UploadFile, filename: str
    ) -> str:
        """
        Handles the logic for saving user images to a static folder in a development environment.
        Saves user image to the static folder 'static/images/profile'.
        Returns the URL address where the image is saved.

        Parameters:
            - user (User): User object associated with the image.
            - uploaded_image (UploadFile): The image file uploaded.
            - filename (str): The desired filename for the saved image.

        Returns:
            - str: URL address where the image is saved.
        """
        # Ensure that the directory exists
        folder_path = "src/static/images/profile"
        os.makedirs(folder_path, exist_ok=True)

        # Create a temporary file path for saving the uploaded image
        file_path = f"{folder_path}/{filename}_temporary"

        # Load the image in chunks and save it to disk
        with open(file_path, "wb") as f:
            while chunk := await uploaded_image.read(DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

        # Resize the saved image to 600x600
        resized_image: Image = self._resize_image(file_path)

        # Save the resized image with a modified file path
        resized_image_file_path = file_path.replace("_temporary", "")
        resized_image.save(resized_image_file_path, resized_image.format)

        # Remove the original uploaded image
        os.remove(file_path)

        # Form the URL address for the saved image
        image_url = resized_image_file_path.replace("src/", "/")

        # Update user information with the image URL and commit to the database
        user.user_image = image_url
        self.db.commit()

        return image_url
