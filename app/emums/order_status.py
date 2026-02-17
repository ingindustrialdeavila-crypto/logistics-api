from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    assigned = "assigned"
    in_progress = "in_progress"
    delivered = "delivered"
    cancelled = "cancelled"