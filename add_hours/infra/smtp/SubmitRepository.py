import io
import mimetypes
import os
import smtplib
import ssl
from email.message import EmailMessage

from add_hours.domain.repository.submit_repository_interface import \
    ISubmitRepository


class SubmitRepository(ISubmitRepository):
    @classmethod
    async def submit_email(
        cls, student_name: str, student_enrollment: str,
        table_xlsx_file: io.BytesIO, certificates_pdf: io.BytesIO
    ):
        email_message = EmailMessage()
        email_message["Subject"] = (
            f"Horas complementares de {student_name} ({student_enrollment})"
        )
        email_message["From"] = os.getenv("EMAIL_SENDER")
        email_message["To"] = os.getenv("EMAIL_TARGET")

        email_message.set_content(
            "Tabela de horas complementares e certificados em anexo"
        )

        maintype, _, subtype = mimetypes.guess_type(
            "tabela_horas_complementares.xlsx"
        )[0].partition("/")
        email_message.add_attachment(
            table_xlsx_file.getvalue(), maintype=maintype, subtype=subtype,
            filename="tabela_horas_complementares.xlsx"
        )

        maintype, _, subtype = mimetypes.guess_type(
            "certificados_pdf.xlsx"
        )[0].partition("/")
        email_message.add_attachment(
            certificates_pdf.getvalue(), maintype=maintype, subtype=subtype,
            filename="certificados_pdf.pdf"
        )

        with smtplib.SMTP(os.getenv("EMAIL_HOST"), 587) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASS"))
            smtp.send_message(email_message)
            smtp.quit()
