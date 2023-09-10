import datetime
import io
import os

from PyPDF2 import PdfMerger
from minio import Minio

from add_hours.domain.repository.storage_repository_interface import \
    IStorageRepository


class StorageRepositoryMinio(IStorageRepository):
    @classmethod
    async def save_certificate(
        cls, certificate_name: str, student_id: str,
        certificate_bytes: io.BytesIO
    ):
        client = await cls._get_client()

        client.put_object(
            os.getenv("MINIO_BUCKET_NAME", "certificates"),
            f"{student_id}|"
            f"{datetime.datetime.utcnow().isoformat()}",
            certificate_bytes,
            certificate_bytes.getbuffer().nbytes,
            content_type=os.getenv(
                "MINIO_SUPPORTED_MIME_TYPE", "application/pdf"
            )
        )

    @classmethod
    async def get_all_certificates(cls, student_id: str) -> io.BytesIO:
        client = await cls._get_client()

        certificates = []

        certificates_objects = client.list_objects(
            bucket_name=os.getenv("MINIO_BUCKET_NAME", "certificates"),
            prefix=f"{student_id}"
        )

        merger = PdfMerger()
        response = None
        for certificate in certificates_objects:
            try:
                response = client.get_object(
                    bucket_name=os.getenv("MINIO_BUCKET_NAME", "certificates"),
                    object_name=certificate.object_name,
                )
                merger.append(io.BytesIO(response.data))
            finally:
                response.close()
                response.release_conn()

        merged_pdfs = io.BytesIO()

        merger.write(merged_pdfs)
        merger.close()

        return merged_pdfs

    @classmethod
    async def _get_client(cls) -> Minio:
        client = Minio(
            os.getenv("MINIO_HOST", "localhost:9000"),
            access_key=os.getenv("MINIO_USER", "minio-add-hours"),
            secret_key=os.getenv("MINIO_PASS", "minio-add-hours"),
            secure=False,
        )

        exists = client.bucket_exists("certificates")

        if not exists:
            client.make_bucket("certificates")

        return client
