from .private import get_data


def get_firm_clients(firm):
    """
    Returns a list of all clients under a firm.

    Arguments
    ---------
    firm: str, required
        Guid that uniquely identifies a firm
    """
    return get_data(
        'FirmInvestors',
        'GET',
        query_params={'firm': firm}
    )
