from app.expenses import crud
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
        report = crud.generate_report(db)
        logger.info("Sending expenses report")
        try:
            Notifications.send(report.content)
        except Exception as err:
            logger.error(f"Expenses report could not be sent: {str(err)}")
        except Exception as err:
            logger.error(f"Expenses report could not be sent: {str(err)}")
        return report
