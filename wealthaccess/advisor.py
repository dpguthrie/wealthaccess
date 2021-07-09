from .private import get_data


def get_advisor_accounts(**kwargs):
    """
    Returns a list of accounts for a given advisor.

    Keyword Arguments
    -----------------
    ignoreOrion: bool, default False, optional
        Allows endpoint to return all accounts except for Orion accounts
    WA_API_KEY: str, default None, optional
        API_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_SECRET_KEY: str, default None, optional
        SECRET_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_USER_GUID: str, default None, optional
        USER_GUID from Wealth Access.  Only necessary when not given as an
        environment variable.
    """
    return get_data('Accounts', 'GET', query_params=kwargs)


def get_advisor_holdings(**kwargs):
    """
    Returns a list of holdings for a given advisor.

    Keyword Arguments
    -----------------
    ignoreOrion: bool, default False, optional
        Allows endpoint to returna ll accounts except for Orion accounts
    """
    return get_data('Holdings', 'GET', query_params=kwargs)


def get_advisor_transactions(**kwargs):
    """
    Returns a list of brokerage transactions for all investors under an
    advisor within the date range or after the transactionId.

    Keyword Arguments
    -----------------
    startDate: date, defaults to lowest possible value, optional
        Set the first date for the date range to filter transactions
    endDate: date, defaults to today, optional
        Set the last date for the date range to filter transactions
    transactionId: int, default None, optional
        Returns all transactions greater than the supplied transactionId
    ignoreOrion: bool, default False, optional
        Allows endpoint to returna ll accounts except for Orion accounts
    WA_API_KEY: str, default None, optional
        API_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_SECRET_KEY: str, default None, optional
        SECRET_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_USER_GUID: str, default None, optional
        USER_GUID from Wealth Access.  Only necessary when not given as an
        environment variable.
    """
    return get_data('Transactions', 'GET', query_params=kwargs)


def get_classifications(**kwargs):
    """
    Returns a list of possible classifications for an advisor

    Keyword Arguments
    -----------------
    WA_API_KEY: str, default None, optional
        API_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_SECRET_KEY: str, default None, optional
        SECRET_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_USER_GUID: str, default None, optional
        USER_GUID from Wealth Access.  Only necessary when not given as an
        environment variable.
    """
    return get_data('Classifications', 'GET')


def get_diversifications(**kwargs):
    """
    Returns a list of possible diversifications for an advisor.

    Keyword Arguments
    -----------------
    WA_API_KEY: str, default None, optional
        API_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_SECRET_KEY: str, default None, optional
        SECRET_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_USER_GUID: str, default None, optional
        USER_GUID from Wealth Access.  Only necessary when not given as an
        environment variable.
    """
    return get_data('Diversifications', 'GET')


def get_investors(**kwargs):
    """
    Returns a list of investors for a given advisor.

    Keyword Arguments
    -----------------
    WA_API_KEY: str, default None, optional
        API_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_SECRET_KEY: str, default None, optional
        SECRET_KEY from Wealth Access.  Only necessary when not given as an
        environment variable.
    WA_USER_GUID: str, default None, optional
        USER_GUID from Wealth Access.  Only necessary when not given as an
        environment variable.
    """
    return get_data('Investors', 'GET')
