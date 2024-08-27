import json
import time
from sqlalchemy.exc import SQLAlchemyError
from schemas import Transaction, Merchant, BillingAddress, Customer, PaymentDetail, URL, POSTRequest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import redis_client

# SQLite database URL
DATABASE_URL = "sqlite:///./transactions.session"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Session = sessionmaker(bind=engine)


def process_transaction(data: dict):
    txn_reference = data["transaction"]["txnReference"]
    with Session() as session:
        try:
            with session.begin_nested():
                try:
                    lang = data.get("lang", "")
                    merchant_info = data["merchant"]
                    billing_address_info = data["customer"]["billingAddress"]
                    transaction_info = data["transaction"]
                    payment_detail_info = transaction_info["paymentDetail"]
                    url_info = data.get("url", {})

                    # Create Customer record
                    customer = Customer(
                        customerID=merchant_info.get("customerID"),
                    )
                    session.add(customer)
                    session.flush()

                    billing_address = BillingAddress(
                        customer_id=customer.id,
                        first_name=billing_address_info.get("firstName"),
                        last_name=billing_address_info.get("lastName"),
                        mobile_no=billing_address_info.get("mobileNo"),
                        email_id=billing_address_info.get("emailId"),
                        address_line1=billing_address_info.get("addressLine1"),
                        city=billing_address_info.get("city"),
                        state=billing_address_info.get("state", ""),
                        zip=billing_address_info.get("zip"),
                        country=billing_address_info.get("country")
                    )
                    session.add(billing_address)
                    session.flush()

                    merchant = Merchant(
                        customerID=customer.customerID,
                        merchantID=merchant_info.get("merchantID"),
                    )
                    session.add(merchant)
                    session.flush()

                    # Create PaymentDetail record
                    payment_detail = PaymentDetail(
                        card_number=payment_detail_info.get("cardNumber"),
                        card_type=payment_detail_info.get("cardType"),
                        exp_year=payment_detail_info.get("expYear"),
                        exp_month=payment_detail_info.get("expMonth"),
                        name_on_card=payment_detail_info.get("nameOnCard"),
                        save_details=payment_detail_info.get("saveDetails"),
                        cvv=payment_detail_info.get("cvv")
                    )
                    session.add(payment_detail)
                    session.flush()

                    # Create Transaction record
                    transaction = Transaction(
                        txn_amount=float(transaction_info.get("txnAmount")),
                        payment_type=transaction_info.get("paymentType"),
                        currency_code=transaction_info.get("currencyCode"),
                        txn_reference=txn_reference,
                        seriestype=transaction_info.get("seriestype", ""),
                        method=transaction_info.get("method", ""),
                        payment_detail_id=payment_detail.id,
                        merchant_id=merchant.id
                    )
                    session.add(transaction)
                    session.flush()

                    # Create URL record if URLs are provided
                    if url_info:
                        url = URL(
                            success_url=url_info.get("successURL"),
                            fail_url=url_info.get("failURL"),
                            transaction_id=transaction.id  # Link to the Transaction record
                        )
                        session.add(url)

                    # Create POSTRequest record
                    post_requests = POSTRequest(
                        lang=lang,
                        merchant_id=merchant.id,
                        customer_id=customer.id,
                        transaction_id=transaction.id
                    )
                    session.add(post_requests)
                    session.flush()

                except SQLAlchemyError as exc:
                    print(f"An error occurred inside the nested transaction: {str(exc)}")
                    raise

            # If no exception occurs, commit the whole transaction
            session.commit()

        except SQLAlchemyError as exc:
            print(f"An error occurred, rolling back the entire transaction: {str(exc)}")
            session.rollback()
            redis_client.delete(txn_reference)

        else:
            redis_client.set(txn_reference, "done")

        finally:
            print(f"Processed transaction: {txn_reference}")


def worker():
    while True:
        try:
            # Blocking pop from Redis queue
            _, message = redis_client.blpop("REQUESTS")

            data = json.loads(message)
            process_transaction(data)
        except Exception as e:
            raise Exception(f"processing transaction: {e}")

        time.sleep(1)


if __name__ == "__main__":
    worker()
