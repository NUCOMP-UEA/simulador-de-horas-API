import io
from abc import ABC, abstractmethod


class ISubmitRepository(ABC):
    @classmethod
    @abstractmethod
    async def submit_email(
        cls, student_name: str, student_enrollment: str,
        table_xlsx_file: io.BytesIO, certificates_pdf: io.BytesIO
    ):
        raise NotImplementedError()
