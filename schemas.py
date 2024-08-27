from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class BillingAddress(Base):
    __tablename__ = "billing_addresses"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey('customers.id'), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    mobile_no = Column(String, nullable=False)
    email_id = Column(String, nullable=False)
    address_line1 = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=True)
    zip = Column(String, nullable=False)
    country = Column(String, nullable=False)

    def __repr__(self):
        return (f"<BillingAddress(id={self.id}, first_name='{self.first_name}', "
                f"last_name='{self.last_name}', mobile_no='{self.mobile_no}', "
                f"email_id='{self.email_id}', address_line1='{self.address_line1}', "
                f"city='{self.city}', state='{self.state}', zip='{self.zip}', "
                f"country='{self.country}')>")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customerID = Column(String, nullable=False)

    def __repr__(self):
        return f"<Customer(id={self.id}, customerID='{self.customerID}')>"


class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    merchantID = Column(String, nullable=False)
    customerID = Column(String, ForeignKey('customers.id'), nullable=False)

    def __repr__(self):
        return (f"<Merchant(id={self.id}, merchant_id='{self.merchantID}', "
                f"customer_id={self.customerID})>")


class PaymentDetail(Base):
    __tablename__ = "payment_details"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    card_type = Column(String, nullable=False)
    exp_year = Column(String, nullable=False)
    exp_month = Column(String, nullable=False)
    name_on_card = Column(String, nullable=False)
    save_details = Column(String, nullable=False)
    cvv = Column(String, nullable=False)

    transactions = relationship("Transaction", back_populates="payment_detail")

    def __repr__(self):
        return (f"<PaymentDetail(id={self.id}, card_number='{self.card_number}', "
                f"card_type='{self.card_type}', exp_year='{self.exp_year}', "
                f"exp_month='{self.exp_month}', name_on_card='{self.name_on_card}', "
                f"save_details='{self.save_details}', cvv='{self.cvv}')>")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    txn_amount = Column(Float, nullable=False)
    payment_type = Column(String, nullable=False)
    currency_code = Column(String, nullable=False)
    txn_reference = Column(String, nullable=False)
    seriestype = Column(String, nullable=True)
    method = Column(String, nullable=True)
    payment_detail_id = Column(Integer, ForeignKey('payment_details.id'), nullable=False)
    merchant_id = Column(Integer, ForeignKey('merchants.id'), nullable=False)

    payment_detail = relationship("PaymentDetail", back_populates="transactions")
    url = relationship("URL", back_populates="transaction", uselist=False)

    def __repr__(self):
        return (f"<Transaction(id={self.id}, txn_amount={self.txn_amount}, "
                f"payment_type='{self.payment_type}', currency_code='{self.currency_code}', "
                f"txn_reference='{self.txn_reference}', seriestype='{self.seriestype}', "
                f"method='{self.method}', payment_detail_id={self.payment_detail_id}, ")


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    success_url = Column(String, nullable=False)
    fail_url = Column(String, nullable=False)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    transaction = relationship("Transaction", back_populates="url")

    def __repr__(self):
        return (f"<URL(id={self.id}, success_url='{self.success_url}', "
                f"fail_url='{self.fail_url}', transaction_id={self.transaction_id})>")


class POSTRequest(Base):
    __tablename__ = "post_requests"

    id = Column(Integer, primary_key=True, index=True)
    lang = Column(String, nullable=False)
    merchant_id = Column(Integer, ForeignKey('merchants.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))

    def __repr__(self):
        return (f"<URL(id={self.id}, success_url='{self.success_url}', "
                f"fail_url='{self.fail_url}', transaction_id={self.transaction_id})>")
