from pydantic import BaseModel
from typing import Union


class BillingAddress(BaseModel):
    firstName: str
    lastName: str
    mobileNo: str
    emailId: str
    addressLine1: str
    city: str
    state: str
    zip: str
    country: str


class Customer(BaseModel):
    billingAddress: BillingAddress


class Merchant(BaseModel):
    merchantID: str
    customerID: str


class PaymentDetail(BaseModel):
    cardNumber: str
    cardType: str
    expYear: str
    expMonth: str
    nameOnCard: str
    saveDetails: str
    cvv: str


class Transaction(BaseModel):
    txnAmount: str
    paymentType: str
    currencyCode: str
    txnReference: str
    seriestype: str
    method: str
    paymentDetail: PaymentDetail


class URL(BaseModel):
    successURL: str
    failURL: str


class TransactionRequest(BaseModel):
    lang: Union[str, None] = None
    merchant: Merchant
    customer: Customer
    transaction: Transaction
    url: Union[URL, None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                  "lang": "en",
                  "merchant": {
                    "merchantID": "MER999900001",
                    "customerID": "C77743201213Bv"
                  },
                  "customer": {
                    "billingAddress": {
                      "firstName": "TestName",
                      "lastName": "TestLastName",
                      "mobileNo": "1234567980",
                      "emailId": "test@test.test",
                      "addressLine1": "abc",
                      "city": "abc",
                      "state": "",
                      "zip": "2345",
                      "country": "CY"
                    }
                  },
                  "transaction": {
                    "txnAmount": "19.01",
                    "paymentType": "sale",
                    "currencyCode": "EUR",
                    "txnReference": "b0f95582-c11b-43b4",
                    "seriestype": "",
                    "method": "",
                    "paymentDetail": {
                      "cardNumber": "4111111111111111",
                      "cardType": "VisaCard",
                      "expYear": "2030",
                      "expMonth": "12",
                      "nameOnCard": "Test Name",
                      "saveDetails": "false",
                      "cvv": "987"
                    }
                  },
                  "url": {
                    "successURL": "https://www.domainname.com/SuccessResponse.html",
                    "failURL": "https://www.domainname.com/FailResponse.html"
                  }
                }
            ]
        }
    }
