# Wealth Access API

Python wrapper for the Wealth Access API

## Overview

This package allows data retrieval from Wealth Access API endpoints.  The functions and classes follow the [Data API Examples](https://api.wealthaccess.com/Help) given by Wealth Access.

## Install

```
pip install wealthaccess
```

## Configuration

The following values **MUST** first be provided by Wealth Access to retrieve any data through the endpoints:

1. API Key
2. Secret Key
3. Advisor External User Id

Once you have those items, set up the following environment variables with the values provided from WealthAccess:

- WA_API_KEY
- WA_SECRET_KEY
- WA_USER_GUID

Documentation is also available detailing how authentication is made:  [https://bitbucket.org/wealthaccessintegration/dataapi/wiki/Home](https://bitbucket.org/wealthaccessintegration/dataapi/wiki/Home)

## Usage

You can access the API endpoints in two ways:  function or class

### Functions

The functions will all be available under the wealthaccess namespace

```python
import wealthaccess as wa

data = wa.get_advisor_holdings
```

The functions are more or less broken out by data hierarchy:  Advisor, Investor, and Firm.  Also, they will follow this format:  `<REST_METHOD>_<hierachy>_<data>`.  Here's a list of functions available:

```python
[
    'get_advisor_accounts', 'get_advisor_holdings', 'get_advisor_transactions',
    'get_classifications', 'get_data', 'get_diversifications', 'get_firm_clients',
    'get_investor_account_transactions', 'get_investor_accounts',
    'get_investor_bank_transactions', 'get_investor_brokerage_transactions',
    'get_investor_diversification_holdings', 'get_investor_document_detail',
    'get_investor_documents', 'get_investor_holdings', 'get_investor_profile_adv',
    'get_investor_profile_inv', 'get_investor_transactions', 'get_investors', 'post_investor_documents'
]
```

### Classes

Additionally, there are three classes that group the hierarchical functions together:

- Advisor
- Firm
- Investor

Currently, they all accept no arguments; they're just acting as a convenient interface to package similar functions together

```python
from wealthaccess import Advisor

adv = Advisor()
holdings = adv.get_advisor_holdings()
transactions = adv.get_advisor_transactions()
```
