from typing import List
from uuid import UUID
from app.models.retailer_model import User
from app.models.customer_model import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate

class CustomerService:
    @staticmethod
    async def list_customers(user:User)->List[Customer]:
        customers = await Customer.find(Customer.owner.id == user.id).to_list()
        return customers
    
    @staticmethod
    async def create_customer(user: User, data: CustomerCreate) -> Customer:
        customer = Customer(**data.dict(), owner=user)
        return await customer.insert()
    
    @staticmethod
    async def retrieve_customer(current_user:User, customer_id:UUID):
        customer = await Customer.find_one(Customer.customer_id == customer_id, Customer.owner.id == current_user.id)
        return customer
    
    @staticmethod
    async def update_customer(current_user: User, customer_id:UUID, data: CustomerUpdate):
        customer = await CustomerService.retrieve_customer(current_user, customer_id)
        await customer.update({"$set": data.dict(exclude_unset=True)})
        await customer.save()
        return customer
    
    @staticmethod
    async def delete_customer(current_user: User, customer_id:UUID):
        customer = await CustomerService.retrieve_customer(current_user, customer_id)
        if customer:
            await customer.delete()

        return None
