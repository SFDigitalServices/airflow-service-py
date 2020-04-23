"""CityTestSF Appointment Report module"""
import os
import datetime
from datetime import date
from modules.acuity import Acuity
from modules.citytest_sf_appointments import CityTestSFAppointments

class CityTestSFAppointmentsReport(CityTestSFAppointments):
    """CityTestSF Report for Appointments """

    @staticmethod
    def get_acuity_appointments(start_date=date.today(), end_date=date.today()):
        """ get_acuity_appointments method """
        acuity = Acuity()
        appointments = []
        default_params = {
            'max': 2000
        }
        types = os.environ['CITYTEST_REPORT_APPT_TYPES'].split(',')
        for appt_type in types:
            params = default_params
            params['appointmentTypeID'] = appt_type.strip()
            days = 1
            for idx in range(0, (end_date-start_date).days+1):
                if idx % days == 0:
                    params['minDate'] = (start_date
                                         + datetime.timedelta(days=idx))
                    params['maxDate'] = (start_date
                                         + datetime.timedelta(days=idx+days-1))
                    print(params)
                    new_appointments = acuity.get_appointments_by_type(
                        appt_type=params['appointmentTypeID'],
                        start_date=params['minDate'],
                        end_date=params['maxDate'],
                        max_records=params['max']
                                        )
                    appointments += new_appointments
        return appointments

    @staticmethod
    def is_test_appt(appt):
        """ Is Test Appointment """
        return appt["firstName"].upper() == "TEST"
