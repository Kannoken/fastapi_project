from fastapi import FastAPI, HTTPException
from redis import Redis
from models import TransactionRequest
app = FastAPI()

redis_client = Redis(host='localhost', port=6379, db=0)


@app.post("/wpp")
async def process_transaction(transaction_request_model: TransactionRequest):
    transaction_id = transaction_request_model.transaction.txnReference
    if not redis_client.exists(transaction_id):
        redis_client.rpush("REQUESTS", transaction_request_model.json())
        redis_client.set(transaction_id, 'in-progress')
    else:
        return HTTPException(409, f"txnReference {transaction_id} already exists")
    return {"message": (
        f"Request received and queued, "
        f"transaction number (txnReference) {transaction_id}")}


@app.get("/status/{transaction_id}")
async def process_transaction(transaction_id: str):
    status = redis_client.get(transaction_id)
    if not status:
        return HTTPException(404, f"txnReference {transaction_id} not found")
    return {f"status of txnReference {transaction_id}": redis_client.get(transaction_id)}
