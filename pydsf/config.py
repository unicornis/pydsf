# -*- coding: utf-8 -*-
from __future__ import unicode_literals

DISTRIBUTION_CHANNEL = "PTP"
SESSION_HEADER = 'ns0:Brukersesjon'
TRANSACTION_HEADER = 'ns1:Transaksjon'
DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
LOGGER_NAME = 'pydsf'

INPUT_FIELDS = {
    "end_user": "saksref",
    "ssn": "foedselsnr",
    "person_id": "personid",
    "duf_no": "dufnr",
    "date_of_birth": "foedselsdato",
    "last_name": "etternavn",
    "first_name": "fornavn",
    "first_name_no": "fornavnnr",
    "name_before_marriage": "navnUgift",
    "middle_name": "mellomnavn",
    "phonetic_name": "fonetiskNavn",
    "address": "adresse",
    "house_no": "husnr",
    "house_no_from": "husnrFra",
    "house_no_to": "husnrTil",
    "letter": "bokstav",
    "phonetic_address": "fonetiskAdresse",
    "street_no": "gatenr",
    "property_no": "gaardsnr",
    "property_sub_no": "bruksnummer",
    "lease_no": "festenr",
    "county_name": "kommunefylkenavn",
    "county_no": "kommunefylkenr",
    "postal_code": "postnr",
    "birth_municipality_no": "foedekommunenr",
    "birth_municipality_name": "foedekommunenavn",
    "gender": "kjoenn",
    "not_dead": "ikkeDoed",
    "year_of_birth": "foedselsaar",
    "year_of_birth_from": "foedselsaarFra",
    "year_of_birth_to": "foedselsaarTil",
    "age_from": "alderFra",
    "age_to": "alderTil",
    "status": "status",
    "date_of_death_from": "doedsdatoFra",
    "date_of_death_to": "doedsdatoTil"
}

OUTPUT_FIELDS = {
    "FODT": "date_of_birth",
    "PERS": "person_number",
    "INR": "dsf_identity_number",
    "FODTAR": "year_of_birth",
    "STAT-KD": "status_code",
    "STAT": "status",
    "NAVN-S": "last_name",
    "NAVN-F": "first_name",
    "NAVN-M": "middle_name",
    "NAVN": "full_name",
    "NAVN-D": "name_registration_date",
    "ADRR": "address_registration_date",
    "ADRF": "last_moving_date",
    "ADR": "address",
    "POSTN": "zip_code",
    "POSTS": "city",
    "KOMNR": "county_number",
    "KOMNA": "county_name",
    "GARD": "property_number",
    "BRUK": "property_usage_number",
    "ADRTYPE": "address_type",
    "FKOM": "moved_from_county_number",
    "FKOM-N": "moved_from_county_name",
    "FKOM-R": "moved_from_county_registration_date",
    "FKOM-F": "moved_from_county_moving_date",
    "AARSADR": "last_address_change",
    "SPES-KD": "special_reg_code_adress_status",
    "SPES": "special_reg_code_address_status_clear_text",
    "SKKR": "school_area",
    "VAKR": "election_area",
    "MELD": "important_message",
    "KJONN": "gender",
    "AARSNVN": "cause_code_for_name_change"
}
