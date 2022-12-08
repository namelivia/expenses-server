from app.reports.report import generate_expenses_report_en, generate_expenses_report_es
from sqlalchemy.orm import Session
from app.notifications.notifications import Notifications
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger(__name__)


class Tasks:
    @staticmethod
    def send_report(db: Session):
        logger.info("Generating expenses report")
        report_es = generate_expenses_report_es(db)
        report_en = generate_expenses_report_en(db)
        logger.info("Sending expenses report")
        try:
            Notifications.send("en", report_en.content)
            Notifications.send("es", report_es.content)
        except Exception as err:
            logger.error(f"Expenses report could not be sent: {str(err)}")
        except Exception as err:
            logger.error(f"Expenses report could not be sent: {str(err)}")
        return report_en
