from datetime import datetime
from .models import onwardchallan


def create_challanNumber():
        current_year = datetime.now().year % 100  # e.g., 25
        next_year = (datetime.now().year + 1) % 100  # e.g., 26
        prefix = f"{current_year:02d}{next_year:02d}"  # '2526'
        
        # Start from 0001 to 9999 (max 4-digit counter)
        for counter in range(1, 10000):
            challan_no = f"{prefix}{counter:05d}"  # '252600001' ... '252609999'
            
            # Ensure uniqueness in DB
            if not onwardchallan.objects.filter(challan_no=challan_no).exists():
                return challan_no

        raise ValueError("No available challan numbers left for the current year range.")

from datetime import datetime
from .models import onwardchallan  

def create_reworknumber():
    prefix = "R/W - "
    
    # Fetch all challan numbers starting with "RW"
    existing_numbers = onwardchallan.objects.filter(challan_no__startswith=prefix).values_list("challan_no", flat=True)
    
    # Extract numeric parts (e.g., RW01 → 1)
    existing_ints = []
    for num in existing_numbers:
        try:
            existing_ints.append(int(num.replace(prefix, "")))
        except ValueError:
            continue
    
    # Generate next available RW number
    for counter in range(1, 1000):  # RW01 to RW999
        rework_no = f"{prefix}{counter:02d}"  # RW01, RW02, RW03...
        if rework_no not in existing_numbers:
            return rework_no
    
    raise ValueError("No available Rework numbers left.")


from .models import Invoice

def create_invoiceno():
    current_year=datetime.now().year % 100
    next_year =(datetime.now().year + 1)% 100
    prefix = f"{ current_year:02d}{next_year:02d}"
    for counter in range(1, 10000):
        invoice_no = f"{prefix}{counter:05d}"
        if not Invoice.objects.filter(invoice_no = invoice_no).exists():
            return invoice_no
    raise ValueError("NO available challan numbers left for the current year range")

from .models import DebitNote
def create_debitNote():
    current_year=datetime.now().year % 100
    next_year=(datetime.now().year +1 )% 100
    prefix =f"{current_year:02d}{next_year:02d}"
    for counter in range(1 , 10000):
        debit_no=f"{prefix}{counter:05d}"
        if not DebitNote.objects.filter(debit_note_no=debit_no).exists():
            return debit_no
    raise ValueError("NO available debit_note_no numbers left for the current year range")


from .models import Newgstsalesreturn
def create_sales_return_no():
    current_year=datetime.now().year % 100
    next_year=(datetime.now().year +1)% 100
    prefix = f'{current_year:02d}{next_year:02d}'
    for counter in range(1, 10000):
        sales_return_no=f"{prefix}{counter:05d}"
        if not Newgstsalesreturn.objects.filter(sales_return_no=sales_return_no).exists():
            return sales_return_no
    raise ValueError("No available sales_return_no number left for the current year range")

from .models import NewSalesOrder
def create_so_no():
    current_year=datetime.now().year % 100
    next_year=(datetime.now().year +1)% 100
    prefix = f'{current_year:02d}{next_year:02d}'
    for counter in range(1, 10000):
        so_no=f"{prefix}{counter:05d}"
        if not NewSalesOrder.objects.filter(so_no=so_no).exists():
            return so_no
    raise ValueError("No available so_no number left for the current year range")


from .models import SalesRateDiff
def create_debit_note_no():
    current_year = datetime.now().year % 100
    next_year =(datetime.now().year+1)% 100
    prefix = f'{current_year:02d}{next_year:02d}'
    for counter in range (1,10000):
        debit_note_no=f"{prefix}{counter:05d}"
        if not SalesRateDiff.objects.filter(debit_note_no = debit_note_no).exists():
            return debit_note_no
    raise ValueError("No available debit_note_no number left for the current year range")



from .models import GSTJobworkInvoice
def create_invoice_no():
    current_year = datetime.now().year % 100
    next_year = (datetime.now().year + 1) % 100

    # Example: 2627
    prefix = f"{current_year:02d}{next_year:02d}"

    for counter in range(1, 10000):
        invoice_no = f"{prefix}{counter:05d}"
        

        if not GSTJobworkInvoice.objects.filter(
            invoice_no=invoice_no
        ).exists():
            return invoice_no

    raise ValueError(
        "No available invoice numbers left for current financial year"
    )

from datetime import datetime
from .models import GSTJobworkRateDiff


def create_debit_note_no_rate_diff():

    current_year = datetime.now().year % 100
    next_year = (datetime.now().year + 1) % 100

    # Example: 2627
    prefix = f"{current_year:02d}{next_year:02d}"

    for counter in range(1, 10000):
        debit_note_no = f"{prefix}{counter:05d}"
       
        if not GSTJobworkRateDiff.objects.filter(
            debit_note_no=debit_note_no
        ).exists():
            return debit_note_no

    raise ValueError(
        "No available debit note numbers left for current financial year"
    )


from datetime import datetime
from .models import CustomerPoAmendment
def create_amd_no():
    current_year = datetime.now().year % 100
    next_year = (datetime.now().year + 1) % 100

    # Example: 2627
    prefix = f"{current_year:02d}{next_year:02d}"

    for counter in range(1, 10000):
        amd_no = f"{prefix}{counter:05d}"

        if not CustomerPoAmendment.objects.filter(amd_no=amd_no).exists():
            return amd_no

    raise ValueError("No available AMD numbers left for current financial year")



from .models import CreditNote
def create_credit_note_no():
    current_year = datetime.now().year % 100
    next_year = (datetime.now().year + 1) % 100

    # Example: 2627
    prefix = f"{current_year:02d}{next_year:02d}"

    for counter in range(1, 10000):
        credit_note_no = f"{prefix}{counter:05d}"

        if not CreditNote.objects.filter(credit_note_no=credit_note_no).exists():
            return credit_note_no

    raise ValueError("No available Credit Note numbers left for current financial year")


from .models import NewProfomaInvoice
def create_invoice_no():
    current_year = datetime.now().year % 100
    next_year = (datetime.now().year + 1) % 100

    # Example: 2627
    prefix = f"{current_year:02d}{next_year:02d}"

    for counter in range(1, 100000):
        invoice_no = f"{prefix}{counter:05d}"

        if not NewProfomaInvoice.objects.filter(invoice_no=invoice_no).exists():
            return invoice_no

    raise ValueError("No available Invoice numbers left for current financial year")