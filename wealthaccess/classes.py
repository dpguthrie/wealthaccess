import base64
import hashlib
import hmac
import os
from datetime import datetime

import requests

from pytz import timezone


class _WealthAccessBase:

    BASE_URL = "https://api.wealthaccess.com"
    USER_GUID = os.getenv("WA_USER_GUID", "10fdc84d-1da4-435f-9a6b-323156beedbd")
    API_KEY = os.getenv("WA_API_KEY", "5e43bccb-c019-4a4d-ac65-7c4eaf4337ef")
    SECRET_KEY = os.getenv("WA_SECRET_KEY", "CGoAQFT3RF1=")

    _CONFIG = {
        "ADVISOR": {
            "Investors": {"uri": "/api/v2/advisor/investors", "params": []},
            "Transactions": {
                "uri": "/api/v2/advisor/transactions",
                "params": ["startDate", "endDate", "transactionId", "ignoreOrion"],
            },
            "Diversifications": {
                "uri": "/api/v2/Advisor/Diversifications",
                "params": [],
            },
            "AdvisorInvestorProfile": {
                "uri": "/api/v2/advisor/investors/{investor_id}/profile",
                "params": [],
            },
            "AdvisorInvestorDocumentsList": {
                "uri": "/api/v2/advisor/investors/{investor_id}/documents",
                "params": ["parentId", "searchTerm"],
            },
            "AdvisorInvestorDocumentsDetail": {
                "uri": "/api/v2/advisor/investors/{investor_id}/documents/{vault_file_id}",
                "params": ["IsPreview", "AdvisorId", "vaultFileId"],
            },
            "AdvisorInvestorDocumentPost": {
                "uri": "/api/v2/advisor/investors/{investor_id}/documents",
                "params": ["request", "investorId"],
            },
            "AdvisorInvestorTransactions": {
                "uri": "/api/v2/advisor/investors/{investor_id}/transactions",
                "params": ["startDate", "endDate", "ignoreOrion"],
            },
            "AdvisorInvestorBankTransactions": {
                "uri": "/api/v2/advisor/investors/{investor_id}/banktransactions",
                "params": ["hideTransfers", "startDate", "endDate", "ignoreOrion"],
            },
            "AdvisorInvestorBrokerageTransactions": {
                "uri": "/api/v2/advisor/investors/{investor_id}/brokeragetransactions",
                "params": ["hideTransfers", "startDate", "endDate", "ignoreOrion"],
            },
            "AdvisorInvestorHoldings": {
                "uri": "/api/v2/advisor/investors/{investor_id}/holdings",
                "params": ["ignoreOrion"],
            },
            "AdvisorInvestorDiversificationHoldings": {
                "uri": "/api/v2/advisor/investors/{investor_id}/diversificationholdings",
                "params": ["diversificationId", "categoryId", "ignoreOrion"],
            },
            "Classifications": {"uri": "/api/v2/Advisor/Classifications", "params": []},
            "Accounts": {"uri": "/api/v2/advisor/accounts", "params": ["ignoreOrion"]},
            "Holdings": {"uri": "/api/v2/advisor/holdings", "params": ["ignoreOrion"]},
        },
        "INVESTOR": {
            "InvestorAccountTransactions": {
                "uri": "/api/v2/investor/accounts/transactions",
                "params": ["clientIdentifier", "accountNumber", "startDate", "endDate"],
            },
            "InvestorAccounts": {
                "uri": "/api/v2/investor/accounts",
                "params": ["clientIdentifier"],
            },
            "InvestorProfile": {
                "uri": "/api/v2/investor/profile",
                "params": ["clientIdentifier"],
            },
        },
        "FIRM": {
            "FirmInvestors": {"uri": "/api/v2/firm/investors", "params": ["firm"]}
        },
    }

    def __init__(self, **kwargs):
        pass

    @property
    def MAIN_KEY(self):
        raise NotImplementedError()

    def _get_data(self, key, method, uri_params={}, query_params={}):
        config = self._CONFIG[self.MAIN_KEY][key]
        requested_uri = self._construct_uri(config["uri"], uri_params)
        query_params = self._construct_query_params(config, query_params)
        print("params: ", query_params)
        sorted_params = self._construct_sorted_parameters(query_params)
        print("sorted params: ", sorted_params)
        headers = self._create_headers(requested_uri, sorted_params, method)
        print("headers: ", headers)
        response = self._make_request(requested_uri, headers, query_params, method)
        return response

    def _construct_uri(self, uri, uri_params):
        if uri_params:
            return uri.format(**uri_params)
        return uri

    def _construct_query_params(self, config, query_params):
        if "params" in config and query_params:
            params = {k: query_params[k] for k in config["params"]}
            return {
                k: str(v).lower() if v is True or v is False else v
                for k, v in params.items()
            }
        return query_params

    def _construct_sorted_parameters(self, query_parameters):
        if query_parameters:
            query_parameter_strings = []
            for k, v in sorted(query_parameters.items()):
                query_parameter_strings.append(f"{k}={v}")
            return "&".join(query_parameter_strings)
        return query_parameters

    def _create_headers(self, requested_uri, sorted_parameters, method):
        gmt_time = datetime.now(timezone("GMT")).strftime("%a, %d %b %Y %H:%M:%S %Z")
        signature = self._signature(gmt_time, requested_uri, sorted_parameters, method)
        return {
            "Authorization": f"WAS {self.USER_GUID}:{signature}",
            "x-WAApiKey": self.API_KEY,
            "x-WATimestamp": gmt_time,
        }

    def _signature(self, gmt_time, requested_uri, sorted_parameters, method):
        string = f"{self.API_KEY}\n{method}\n{gmt_time}\n{requested_uri}\n"
        if sorted_parameters:
            string += f"{sorted_parameters}"
        message = bytes(string, "utf-8")
        print("message is", message)
        secret = bytes(self.SECRET_KEY, "utf-8")
        signature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha256).digest()
        )
        return signature.decode("utf-8")

    def _make_request(self, requested_uri, headers, query_params, method):
        return requests.request(
            method=method,
            url=f"{self.BASE_URL}{requested_uri}",
            params=query_params,
            headers=headers,
        )

    def _validate_request(self):
        pass


class Advisor(_WealthAccessBase):

    MAIN_KEY = "ADVISOR"

    def __init__(self):
        pass

    # INVESTORS
    def get_investor_bank_transactions(self, investor_id, **kwargs):
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
        return self._get_data(
            key="AdvisorInvestorBankTransactions",
            method="GET",
            uri_params={"investor_id": investor_id},
            query_params=kwargs,
        )

    def get_investor_brokerage_transactions(self, investor_id, **kwargs):
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
        return self._get_data(
            key="AdvisorInvestorBrokerageTransactions",
            method="GET",
            uri_params={"investor_id": investor_id},
            query_params=kwargs,
        )

    def get_investor_diversification_holdings(self, investor_id, **kwargs):
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
        return self._get_data(
            key="AdvisorInvestorDiversificationHoldings",
            method="GET",
            uri_params={"investor_id": investor_id},
            query_params=kwargs,
        )

    def get_investor_document_detail(self, investor_id, vault_file_id, **kwargs):
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
        return self._get_data(
            key="AdvisorInvestorDocumentsList",
            method="GET",
            uri_params={"investor_id": investor_id, "vault_file_id": vault_file_id},
            query_params=kwargs,
        )

    def get_investor_documents(self, investor_id, **kwargs):
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
        return self._get_data(
            key="AdvisorInvestorDocumentsList",
            method="GET",
            uri_params={"investor_id": investor_id},
            query_params=kwargs,
        )

    def get_investor_holdings(self, investor_id, **kwargs):
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
        return self._get_data(
            key="AdvisorInvestorHoldings",
            method="GET",
            uri_params={"investor_id": investor_id},
            query_params=kwargs,
        )

    def get_investor_profile(self, investor_id):
        """
        Returns a list of brokerage transactions for a given investor.

        Arguments
        ---------
        investor_id: int
            Investor specified by the investorId returned from the investors
            endpoint.
        """
        return self._get_data(
            "AdvisorInvestorProfile", "GET", uri_params={"investor_id": investor_id}
        )

    def get_investor_transactions(self, investor_id, **kwargs):
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
        return self._get_data(
            key="AdvisorInvestorTransactions",
            method="GET",
            uri_params={"investor_id": investor_id},
            query_params=kwargs,
        )

    def post_investor_document(self, investor_id, **kwargs):
        return self._get_data(
            key="AdvisorInvestorDocumentPost",
            method="POST",
            uri_params={"investor_id": investor_id},
            query_params=dict(kwargs, investorId=investor_id),
        )

    # ADVISOR
    def get_accounts(self, **kwargs):
        """
        Returns a list of accounts for a given advisor.

        Keyword Arguments
        -----------------
        ignoreOrion: bool, default False, optional
            Allows endpoint to return all accounts except for Orion accounts
        """
        return self._get_data("Accounts", "GET", query_params=kwargs)

    def get_advisor_holdings(self, **kwargs):
        """
        Returns a list of holdings for a given advisor.

        Keyword Arguments
        -----------------
        ignoreOrion: bool, default False, optional
            Allows endpoint to returna ll accounts except for Orion accounts
        """
        return self._get_data("Holdings", "GET", query_params=kwargs)

    def get_advisor_transactions(self, **kwargs):
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
        """
        return self._get_data("Transactions", "GET", query_params=kwargs)

    def get_classifications(self):
        """
        Returns a list of possible classifications for an advisor
        """
        return self._get_data("Classifications", "GET")

    def get_diversifications(self):
        """
        Returns a list of possible diversifications for an advisor.
        """
        return self._get_data("Diversifications", "GET")

    def get_investors(self):
        """
        Returns a list of investors for a given advisor.
        """
        return self._get_data("Investors", "GET")


class Investor(_WealthAccessBase):

    MAIN_KEY = "INVESTOR"

    def __init__(self):
        pass

    def get_account_transactions(self, client_identifier, account_number, **kwargs):
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
        return self._get_data(
            "InvestorAccountTransactions",
            "GET",
            query_params=dict(
                kwargs, clientIdentifier=client_identifier, accountNumber=account_number
            ),
        )

    def get_accounts(self, client_identifier):
        """
        Returns a list of accounts for a given user.

        Arguments
        ---------
        client_identifier: str, required
            Source system client identifier for end-user
        """
        return self._get_data(
            "InvestorAccounts",
            "GET",
            query_params={"clientIdentifier": client_identifier},
        )

    def get_profile(self, client_identifier):
        """
        Returns the user profile for a given user.

        Arguments
        ---------
        client_identifier: str, required
            Source system client identifier for end-user
        """
        return self._get_data(
            "InvestorProfile",
            "GET",
            query_params={"clientIdentifier": client_identifier},
        )


class Firm(_WealthAccessBase):

    MAIN_KEY = "FIRM"

    def __init__(self):
        pass

    def get_clients(self, firm):
        """
        Returns a list of all clients under a firm.

        Arguments
        ---------
        firm: str, required
            Guid that uniquely identifies a firm
        """
        return self._get_data("FirmInvestors", "GET", query_params={"firm": firm})
