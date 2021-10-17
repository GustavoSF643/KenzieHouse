from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class FiscalNote:
    shipping_company_name: str
    shipping_company_cnpj: str
    shipping_value: int
    shipping_adress: dict
    total_value: int
    purcharse_date: datetime
    buyer_name: str
    buyer_cpf: str
    buyer_email: str
    products: list = field(default_factory=list)
