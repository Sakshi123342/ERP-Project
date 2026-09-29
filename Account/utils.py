
from datetime import datetime
from .models import *

def create_bill_no():

    current_year = datetime.now().year % 100      # 26
    next_year = (datetime.now().year + 1) % 100  # 27

    prefix = f"{current_year:02d}{next_year:02d}"   # 2627

    # 00001 → 99999
    for counter in range(1, 100000):

        bill_no = f"{prefix}{counter:05d}"

        # CHECK UNIQUE
        if not BillRegister.objects.filter(no=bill_no).exists():
            return bill_no

    raise ValueError("No bill numbers available")

def create_jobwork_bill_no():
    current_year = datetime.now().year % 100      # 26
    next_year = (datetime.now().year + 1) % 100  # 27

    prefix = f"{current_year:02d}{next_year:02d}"   # 2627

    # 00001 → 99999
    for counter in range(1, 100000):

        bill_no = f"{prefix}{counter:05d}"

        # CHECK UNIQUE
        if not JobworkBillRegister.objects.filter(bill_no=bill_no).exists():
            return bill_no

    raise ValueError("No bill numbers available")
