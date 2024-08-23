from typing import List, Union, Dict, Tuple
from datetime import datetime

from pydantic import BaseModel



class Object(BaseModel):
    scraping_date: datetime
    link: str
    name: str
    price: str
    signature: str
    address: str
    list_of_images_of_object: List[str]
    list_of_details_of_object: List
    description: str
    object_overview_data: List
    ad_id: str
    profile: 'Profile'


class Profile(BaseModel):
    name: str
    image: str
    link: str
    installment_loan_payment: Union[str, None]
    advance_payment_of_credit_calculation: Union[str, None]
    list_of_items_included_in_price: Union[List[Tuple], None]
    work_schedule: Union[str, None]


class ListOfObjects(BaseModel):
    objects_from_list: List['ObjectFromList']


class ObjectFromList(BaseModel):
    link: str
    name: str

