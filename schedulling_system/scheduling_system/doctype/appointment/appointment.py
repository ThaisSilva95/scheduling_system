# Copyright (c) 2025, Thais Silva and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime
from datetime import timedelta, datetime
from frappe import _

class Appointment(Document):
    def validate(self):
        if self.start_date and self.duration:
            try:
                start_dt = get_datetime(self.start_date)
                duration_time = datetime.strptime(self.duration, "%H:%M:%S").time()
                duration_delta = timedelta(
                    hours=duration_time.hour,
                    minutes=duration_time.minute,
                    seconds=duration_time.second
                )
                self.end_date = start_dt + duration_delta

            except Exception as e:
                frappe.throw(f"Ocorreu um erro ao calcular o end_date: {e}")

        # Verificar conflitos com compromissos existentes
        if self.seller and self.start_date and self.end_date:
            conflicting_appointments = frappe.db.sql("""
                SELECT name FROM `tabAppointment`
                WHERE
                    seller = %s
                    AND name != %s
                    AND (
                        (start_date <= %s AND end_date > %s) OR
                        (start_date < %s AND end_date >= %s) OR
                        (start_date >= %s AND end_date <= %s)
                    )
                    AND docstatus < 2
            """, (
                self.seller,
                self.name,
                self.start_date, self.start_date,
                self.end_date, self.end_date,
                self.start_date, self.end_date
            ))

            if conflicting_appointments:
                frappe.throw(_(f"O vendedor {self.seller} já tem um compromisso nesse horário."))
