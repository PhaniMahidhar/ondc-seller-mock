from pydantic import BaseModel
from typing import List, Dict

class Address(BaseModel):
    area_code: str
    building: str
    city: str
    country: str
    door: str
    locality: str
    state: str
    street: str
    ward: str

class Location(BaseModel):
    address: Address
    gps: str

class Authorization(BaseModel):
    token: str
    type: str

class Descriptor(BaseModel):
    code: str
    name: str

class Person(BaseModel):
    name: str
    phone: str
    tags: Dict[str, str]

class Customer(BaseModel):
    person: Person

class Agent(BaseModel):
    name: str
    phone: str
    rateable: bool
    rating: str

class FulfillmentStart(BaseModel):
    authorization: Authorization
    location: Location

class FulfillmentEnd(BaseModel):
    location: Location

class FulfillmentState(BaseModel):
    descriptor: Descriptor

class Vehicle(BaseModel):
    category: str
    registration: str

class Fulfillment(BaseModel):
    agent: Agent
    customer: Customer
    end: FulfillmentEnd
    id: str
    start: FulfillmentStart
    state: FulfillmentState
    vehicle: Vehicle

class ItemDescriptor(BaseModel):
    code: str
    name: str

class Item(BaseModel):
    descriptor: ItemDescriptor
    fulfillment_id: str
    id: str
    payment_id: str
    tags: Dict[str, str]

class PaymentParams(BaseModel):
    amount: str
    bank_account: str
    bank_account_name: str
    bank_code: str
    currency: str
    transaction_status: str

class PaymentTime(BaseModel):
    duration: str

class Payment(BaseModel):
    id: str
    params: PaymentParams
    time: PaymentTime
    type: str

class ProviderDescriptor(BaseModel):
    name: str

class Provider(BaseModel):
    descriptor: ProviderDescriptor
    id: str

class QuoteBreakup(BaseModel):
    price: Dict[str, str]
    title: str

class Quote(BaseModel):
    breakup: List[QuoteBreakup]
    currency: str
    value: str

class Order(BaseModel):
    fulfillment: Fulfillment
    id: str
    items: List[Item]
    payment: Payment
    provider: Provider
    quote: Quote

class OnCancelMessage(BaseModel):
    order: Order

class Context(BaseModel):
    action: str
    bap_id: str
    bap_uri: str
    bpp_id: str
    bpp_uri: str
    city: str
    core_version: str
    country: str
    domain: str
    message_id: str
    timestamp: str
    transaction_id: str

class Message(BaseModel):
    order: Order

class JSONData(BaseModel):
    context: Context
    message: Message
