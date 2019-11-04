# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..exceptions import DSFInputError
from ..exceptions import DSFServiceError
from .response import parse_response
from .translations import translate_input_fields, translate_output_fields


def find_person(client, **input_fields):
    """
    Request details on a given person.

    This function sends a single request for data from DSF, with a given input.

    The following keyword arguments are valid as input:
    - end_user
    - ssn
    - person_id
    - duf_no
    - date_of_birth
    - last_name
    - first_name
    - first_name_no
    - name_before_marriage
    - middle_name
    - phonetic_name
    - address
    - house_no
    - house_no_from
    - house_no_to
    - letter
    - phonetic_address
    - street_no
    - property_no
    - property_sub_no
    - lease_no
    - county_name
    - county_no
    - postal_code
    - birth_municipality_no
    - birth_municipality_name
    - gender
    - not_dead
    - year_of_birth
    - year_of_birth_from
    - year_of_birth_to
    - age_from
    - age_to
    - status
    - date_of_death_from
    - date_of_death_to

    Args:
        client (DSFClient): Client to run the request with
        **input_fields: Keyword argument list containing the fields to be filled out in the
            request

    Returns:
        result: If a result is returned from DSF, it is parsed and returned.
        None: If no person could be found in the registry.

    Raises:
        DSFClientError: If the is an issue with the input (e.g. unrecognised field name) or
            there is an issue with the client/configuration.
        WebServiceError: If there was an error returned from DSF.
    """
    log = client.get_logger()
    log.info("Preparing to request DSF:hentDetaljer.")
    log.debug("Translating input fields.")
    try:
        search_fields = translate_input_fields(**input_fields)
    except ValueError as error:
        err_msg = "Error in input data: {}".format(error.message)
        log.error(err_msg)
        raise DSFInputError(err_msg)

    log.info("Search parameters: {}".format(search_fields))
    log.debug("Running query.")
    dsf_response = client.get_details(**search_fields)

    try:
        parsed_response = parse_response(dsf_response)
    except DSFServiceError as error:
        err_msg = "An error occured while performing this request: {}".format(error.message)
        log.error(err_msg)
        import traceback
        log.error(traceback.format_exc())
        raise DSFServiceError(err_msg)

    if not parsed_response:
        log.info("No person found, returning None.")
        return None

    log.info("Found match in DSF. Creating response.")  # make objects out of this?
    result = translate_output_fields(parsed_response)
    log.info("Result: {}".format(result))
    return result
