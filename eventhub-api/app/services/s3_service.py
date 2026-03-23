"""
S3 service — optional banner image upload.
Falls back gracefully if AWS credentials are not configured.
"""
import logging
import uuid
from typing import Optional

logger = logging.getLogger(__name__)


class S3Service:
    def __init__(self):
        from app.config import get_settings
        self.settings = get_settings()

    async def upload_banner(self, file_data: bytes, content_type: str) -> Optional[str]:
        """Upload a banner image to S3 and return the public URL."""
        if not self.settings.AWS_ACCESS_KEY_ID:
            logger.warning("S3 not configured — skipping upload")
            return None
        try:
            import boto3
            s3 = boto3.client(
                "s3",
                aws_access_key_id=self.settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.settings.AWS_SECRET_ACCESS_KEY,
                region_name=self.settings.AWS_REGION,
            )
            key = f"banners/{uuid.uuid4()}.jpg"
            s3.put_object(
                Bucket=self.settings.S3_BUCKET,
                Key=key,
                Body=file_data,
                ContentType=content_type,
                ACL="public-read",
            )
            return f"https://{self.settings.S3_BUCKET}.s3.{self.settings.AWS_REGION}.amazonaws.com/{key}"
        except Exception as exc:
            logger.error("S3 upload failed: %s", exc)
            return None


s3_service = S3Service()