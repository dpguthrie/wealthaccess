from .private import get_data


def get_investor_account_transactions(
        client_identifier, account_number, **kwargs):
    """
    Returns a list of transactions for a given account and user.

    Arguments
    ---------
    client_identifier: str, required
        Source system client identifier for end-user
    account_number: str, required
        Unique identifier for account

    Keyword Arguments
    -----------------
    startDate: date, defaults to lowest possible value, optional
        Transaction date has to be greater than or equal to this date
    endDate: date, defaults to today, optional
        Transaction date has to be less than or equal to this date
    """
    return get_data(
        'InvestorAccountTransactions',
        'GET',
        query_params=dict(
            kwargs,
            clientIdentifier=client_identifier,
            accountNumber=account_number
        )
    )


def get_investor_accounts(client_identifier):
    """
    Returns a list of accounts for a given user.

    Arguments
    ---------
    client_identifier: str, required
        Source system client identifier for end-user
    """
    return get_data(
        'InvestorAccounts',
        'GET',
        query_params={'clientIdentifier': client_identifier}
    )


def get_investor_bank_transactions(investor_id, **kwargs):
    """
    Returns a list of transactions for a given investor.

    Arguments
    ---------
    investor_id: int
        Investor specified by the investorId returned from the investors
        endpoint.

    Keyword Arguments
    -----------------
    hideTransfers: bool, default True, optional
        Filter out transfers
    startDate: date, defaults to lowest possible value, optional
        Set the first date for the date range to filter transactions
    endDate: date, defaults to today, optional
        Set the last date for the date range to filter transactions
    ignoreOrion: bool, default False, optional
        Allows endpoint to returna ll accounts except for Orion accounts
    """
    return get_data(
        key='AdvisorInvestorBankTransactions',
        method='GET',
        uri_params={'investor_id': investor_id},
        query_params=kwargs
    )


def get_investor_brokerage_transactions(investor_id, **kwargs):
    """
    Returns a list of brokerage transactions for a given investor.

    Arguments
    ---------
    investor_id: int
        Investor specified by the investorId returned from the investors
        endpoint.

    Keyword Arguments
    -----------------
    startDate: date, defaults to lowest possible value, optional
        Set the first date for the date range to filter transactions
    endDate: date, defaults to today, optional
        Set the last date for the date range to filter transactions
    ignoreOrion: bool, default False, optional
        Allows endpoint to returna ll accounts except for Orion accounts
    """
    return get_data(
        key='AdvisorInvestorBrokerageTransactions',
        method='GET',
        uri_params={'investor_id': investor_id},
        query_params=kwargs
    )


def get_investor_diversification_holdings(investor_id, **kwargs):
    """
    Returns a list of holdings for a given investor. Investor is specified
    by the investorId returned from the investors endpoint.

    Arguments
    ---------
    investor_id: int
        Investor specified by the investorId returned from the investors
        endpoint.

    Keyword Arguments
    -----------------
    diversificationId: int, default 1, optional
        Drill down into a diversification subtype
    categoryId: int, default 0, optional
        Used when a diversification subtype has category
    ignoreOrion: bool, default False, optional
        Allows endpoint to returna ll accounts except for Orion accounts
    """
    return get_data(
        key='AdvisorInvestorDiversificationHoldings',
        method='GET',
        uri_params={'investor_id': investor_id},
        query_params=kwargs
    )


def get_investor_document_detail(
        investor_id, vault_file_id, **kwargs):
    """
    Download specific file or folder. Investor is specified by the
    investorId returned from the investors endpoint.

    Arguments
    ---------
    investor_id: int, required
        Investor specified by the investorId returned from the investors
        endpoint.
    vault_file_id: int, required
        Folder ID

    Keyword Arguments
    -----------------
    IsPreview: bool, default None, optional
    AdvisorId: int, default None, optional
    investorId: int, required
        Investor is specified by the investorId returned from the investors
        endpoint
    vaultFileId: str, default None, optional
    """
    return get_data(
        key='AdvisorInvestorDocumentsList',
        method='GET',
        uri_params={
            'investor_id': investor_id,
            'vault_file_id': vault_file_id
        },
        query_params=kwargs
    )


def get_investor_documents(investor_id, **kwargs):
    """
    Returns a list of documents for a given investor. Investor is specified
    by the investorId returned from the investors endpoint.

    Arguments
    ---------
    investor_id: int
        Investor specified by the investorId returned from the investors
        endpoint.

    Keyword Arguments
    -----------------
    parentId: int, default None, optional
        Drilldown into a folder by folder's VaultFileId
    searchTerm: str, default None, optional
        Search for a file
    """
    return get_data(
        key='AdvisorInvestorDocumentsList',
        method='GET',
        uri_params={'investor_id': investor_id},
        query_params=kwargs
    )


def get_investor_holdings(investor_id, **kwargs):
    """
    Returns a list of holdings for a given investor. Investor is specified
    by the investorId returned from the investors endpoint.

    Arguments
    ---------
    investor_id: int
        Investor specified by the investorId returned from the investors
        endpoint.

    Keyword Arguments
    -----------------
    ignoreOrion: bool, default False, optional
        Allows endpoint to returna ll accounts except for Orion accounts
    """
    return get_data(
        key='AdvisorInvestorHoldings',
        method='GET',
        uri_params={'investor_id': investor_id},
        query_params=kwargs
    )


def get_investor_profile_inv(client_identifier):
    """
    Returns the user profile for a given user.

    Arguments
    ---------
    client_identifier: str, required
        Source system client identifier for end-user
    """
    return get_data(
        'InvestorProfile',
        'GET',
        query_params={'clientIdentifier': client_identifier}
    )


def get_investor_profile_adv(investor_id):
    """
    Returns the user profile for a given user.

    Arguments
    ---------
    investor_id: int
        Investor specified by the investorId returned from the investors
        endpoint.
    """
    return get_data(
        'AdvisorInvestorProfile',
        'GET',
        uri_params={'investor_id': investor_id}
    )


def get_investor_transactions(investor_id, **kwargs):
    """
    Returns a list of brokerage transactions for a given investor.
    Investor is specified by the investorId returned from the investors
    endpoint.

    Arguments
    ---------
    investor_id: int
        Investor specified by the investorId returned from the investors
        endpoint.

    Keyword Arguments
    -----------------
    startDate: date, defaults to lowest possible value, optional
        Set the first date for the date range to filter transactions
    endDate: date, defaults to today, optional
        Set the last date for the date range to filter transactions
    ignoreOrion: bool, default False, optional
        Allows endpoint to returna ll accounts except for Orion accounts
    """
    return get_data(
        key='AdvisorInvestorTransactions',
        method='GET',
        uri_params={'investor_id': investor_id},
        query_params=kwargs
    )


def post_investor_document(investor_id, **kwargs):
    return get_data(
        key='AdvisorInvestorDocumentPost',
        method='POST',
        uri_params={'investor_id': investor_id},
        query_params=dict(kwargs, investorId=investor_id)
    )
