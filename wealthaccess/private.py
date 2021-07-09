import base64
import hashlib
import hmac
import os
from datetime import datetime

import requests

from pytz import timezone


BASE_URL = "https://api.wealthaccess.com"

_CONFIG = {
    "Investors": {"uri": "/api/v2/advisor/investors", "params": []},
    "Transactions": {
        "uri": "/api/v2/advisor/transactions",
        "params": ["startDate", "endDate", "transactionId", "ignoreOrion"],
    },
    "Diversifications": {"uri": "/api/v2/Advisor/Diversifications", "params": []},
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
    "FirmInvestors": {"uri": "/api/v2/firm/investors", "params": ["firm"]},
}


def get_data(key, method, uri_params={}, query_params={}):
    config = _CONFIG[key]
    requested_uri = _construct_uri(config["uri"], uri_params)
    keys, query_params = _get_keys(query_params)
    query_params = _construct_query_params(config, query_params)
    sorted_params = _construct_sorted_params(query_params)
    headers = _create_headers(requested_uri, sorted_params, method, keys)
    response = _make_request(requested_uri, headers, query_params, method)
    return response


def _construct_uri(uri, uri_params):
    if uri_params:
        return uri.format(**uri_params)
    return uri


def _get_keys(query_params):
    keys = {
        "API_KEY": query_params.pop("WA_API_KEY", os.getenv("WA_API_KEY")),
        "SECRET_KEY": query_params.pop("WA_SECRET_KEY", os.getenv("WA_SECRET_KEY")),
        "USER_GUID": query_params.pop("WA_USER_GUID", os.getenv("WA_USER_GUID")),
    }
    print(keys)
    if any(v is None for k, v in keys.items()):
        raise TypeError(
            "You're missing a key required by Wealth Access to make requests"
        )
    return keys, query_params


def _construct_query_params(config, query_params):
    if "params" in config and query_params:
        query_params = {
            k: query_params[k] for k in query_params if k in config["params"]
        }
    return query_params


def _construct_sorted_params(query_parameters):
    if query_parameters:
        query_parameter_strings = []
        for k, v in sorted(query_parameters.items()):
            query_parameter_strings.append(f"{k}={v}")
        return "&".join(query_parameter_strings)
    return query_parameters


def _create_headers(requested_uri, sorted_parameters, method, keys):
    gmt_time = datetime.now(timezone("GMT")).strftime("%a, %d %b %Y %H:%M:%S %Z")
    signature = _signature(gmt_time, requested_uri, sorted_parameters, method, keys)
    return {
        "Authorization": f'WAS {keys["USER_GUID"]}:{signature}',
        "x-WAApiKey": keys["API_KEY"],
        "x-WATimestamp": gmt_time,
    }


def _signature(gmt_time, requested_uri, sorted_parameters, method, keys):
    string = f"{keys['API_KEY']}\n{method}\n{gmt_time}\n{requested_uri}\n"
    if sorted_parameters:
        string += f"{sorted_parameters}"
    message = bytes(string, "utf-8")
    secret = bytes(keys["SECRET_KEY"], "utf-8")
    signature = base64.b64encode(
        hmac.new(secret, message, digestmod=hashlib.sha256).digest()
    )
    return signature.decode("utf-8")


def _make_request(requested_uri, headers, query_params, method):
    return requests.request(
        method=method,
        url=f"{BASE_URL}{requested_uri}",
        params=query_params,
        headers=headers,
    )
