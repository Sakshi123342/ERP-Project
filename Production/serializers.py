
from rest_framework import serializers
from .models import ScrapRejection


class ScrapRejectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapRejection
        fields = '__all__'  # This will include all fields of the ScrapRejection model



# Production Entry
from rest_framework import serializers
from .models import ProductionEntry, MachineIdleTime

class MachineIdleTime_Detail_EnterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineIdleTime
        fields = '__all__'

# class ProductionEntrySerializer(serializers.ModelSerializer):
#     MachineIdleTime_Detail_Enter = MachineIdleTime_Detail_EnterSerializer(many=True, read_only=True)

#     class Meta:
#         model = ProductionEntry
#         fields = '__all__'



from rest_framework import serializers
from decimal import Decimal
import re
from .models import ProductionEntry, MachineIdleTime
from .serializers import MachineIdleTime_Detail_EnterSerializer  # if in same app, import directly
from Store.models import MaterialChallan, MaterialChallanTable


from rest_framework import serializers
from decimal import Decimal
from Store.models import MaterialChallanTable
from .models import ProductionEntry


# class ProductionEntrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductionEntry
#         fields = "__all__"

#     def create(self, validated_data):
#         """
#         Production entry create karte time: prod_qty subtract karo MaterialChallanTable.Qty se
#         """
#         production = ProductionEntry.objects.create(**validated_data)

#         # Extract HeatNo from lot_no
#         lot_no_value = (production.lot_no or "").strip()
#         heat_no = lot_no_value.split("|")[0].strip() if "|" in lot_no_value else lot_no_value

#         qty_to_subtract = Decimal(production.prod_qty or 0)

#         # Subtract cumulatively across matching rows (FIFO)
#         remaining = Decimal(qty_to_subtract)
#         for item in MaterialChallanTable.objects.filter(HeatNo__iexact=heat_no).order_by('id'):
#             if remaining <= 0:
#                 break
#             current_qty = Decimal(item.Qty or 0)
#             if current_qty <= 0:
#                 continue
#             to_subtract = min(current_qty, remaining)
#             item.Qty = str(current_qty - to_subtract)
#             item.save(update_fields=["Qty"])
#             print(f"✓ ChallanTable {item.id} FIFO subtract: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={heat_no})")
#             remaining -= to_subtract

#         return production

#     def update(self, instance, validated_data):
#         """
#         Update ke waqt: pehle purani qty restore karo, phir nayi qty subtract karo.
#         """
#         # Capture old values before mutation
#         old_lot_no_value = (instance.lot_no or "").strip()
#         old_heat_no = old_lot_no_value.split("|")[0].strip() if "|" in old_lot_no_value else old_lot_no_value
#         old_qty = Decimal(instance.prod_qty or 0)

#         # Apply incoming changes
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         # Restore previous quantity to the first matching row for old HeatNo
#         old_item = MaterialChallanTable.objects.filter(HeatNo__iexact=old_heat_no).order_by('id').first()
#         if old_item and old_qty > 0:
#             restored_val = Decimal(old_item.Qty or 0) + old_qty
#             old_item.Qty = str(restored_val)
#             old_item.save(update_fields=["Qty"])
#             print(f"♻ Restored ChallanTable {old_item.id}: +{old_qty} (HeatNo={old_heat_no})")

#         # Subtract new quantity from new heat records
#         new_lot_no_value = (instance.lot_no or "").strip()
#         new_heat_no = new_lot_no_value.split("|")[0].strip() if "|" in new_lot_no_value else new_lot_no_value
#         new_qty = Decimal(instance.prod_qty or 0)

#         # Subtract cumulatively across matching rows for new HeatNo
#         remaining_new = Decimal(new_qty)
#         for item in MaterialChallanTable.objects.filter(HeatNo__iexact=new_heat_no).order_by('id'):
#             if remaining_new <= 0:
#                 break
#             current_qty = Decimal(item.Qty or 0)
#             if current_qty <= 0:
#                 continue
#             to_subtract = min(current_qty, remaining_new)
#             item.Qty = str(current_qty - to_subtract)
#             item.save(update_fields=["Qty"])
#             print(f"✓ Updated ChallanTable {item.id} FIFO: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={new_heat_no})")
#             remaining_new -= to_subtract

#         return instance











class ProductionEntrySerializer(serializers.ModelSerializer):
    MachineIdleTime_Detail_Enter = MachineIdleTime_Detail_EnterSerializer(many=True, read_only=True)

    class Meta:
        model = ProductionEntry
        fields = "__all__"

    def extract_bom_qty(self, parent_operation):
        """Extract BOMQty numeric value from string like: 'ScracpQty: N/A | BOMQty: 0.987'"""
        text = parent_operation or ""
        # Case-insensitive search for BOMQty
        match = re.search(r"BOMQty:\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
        if not match:
            print(f"⚠️ Could not extract BOMQty from: '{text}', using default 1")
            return Decimal("1")
        try:
            bom_qty = Decimal(match.group(1))
            print(f"✅ Extracted BOMQty: {bom_qty} from: '{text}'")
            return bom_qty
        except Exception as e:
            print(f"⚠️ Error extracting BOMQty from '{text}': {e}, using default 1")
            return Decimal("1")

    def compute_effective_qty(self, production, original_parent_operation=None):
        """
        Return effective qty:
        - If operation starts with '10': prod_qty * BOMQty (truncated to 2 decimals)
        - Otherwise: prod_qty
        """
        prod_qty = Decimal(production.prod_qty or 0)
        operation = (production.operation or "").strip()
        
        if operation.startswith("10"):
            # Use original_parent_operation if provided, otherwise use current ParentOperation
            parent_op_source = original_parent_operation if original_parent_operation is not None else production.ParentOperation
            bom_qty = self.extract_bom_qty(parent_op_source)
            # Truncate (ROUND_DOWN) to 2 decimals after multiplication
            return (prod_qty * bom_qty).quantize(Decimal("0.01"), rounding=Decimal.ROUND_DOWN)
        
        return prod_qty

    def update_parent_operation_for_operation_10(self, production, original_parent_operation=None):
        """Update ParentOperation when operation starts with '10': BOMQty = (BOMQty * prod_qty) - prod_qty"""
        operation = (production.operation or "").strip()
        if not operation.startswith("10"):
            return
        
        prod_qty = Decimal(production.prod_qty or 0)
        # Use original_parent_operation if provided, otherwise use current ParentOperation
        parent_op_source = original_parent_operation if original_parent_operation is not None else production.ParentOperation
        original_bom_qty = self.extract_bom_qty(parent_op_source)
        
        # Calculate new BOMQty: (BOMQty * prod_qty) - prod_qty
        new_bom_qty = (original_bom_qty * prod_qty) - prod_qty
        
        # Ensure non-negative
        if new_bom_qty < 0:
            new_bom_qty = Decimal("0")
        
        # Format with 3 decimal places
        new_bom_qty_str = str(new_bom_qty.quantize(Decimal("0.001")))
        
        # Update ParentOperation: "ScracpQty: N/A | BOMQty: <calculated_value>"
        production.ParentOperation = f"ScracpQty: N/A | BOMQty: {new_bom_qty_str}"
        production.save(update_fields=["ParentOperation"])
        print(f"📝 Updated ParentOperation for operation 10: BOMQty {original_bom_qty} → {new_bom_qty_str}")

    def create(self, validated_data):
        production = ProductionEntry.objects.create(**validated_data)

        # Store original ParentOperation before any updates
        original_parent_operation = validated_data.get('ParentOperation', production.ParentOperation)

        # Update ParentOperation if operation starts with '10'
        self.update_parent_operation_for_operation_10(production, original_parent_operation=original_parent_operation)

        # Extract HeatNo from lot_no
        lot_no_value = (production.lot_no or "").strip()
        heat_no = lot_no_value.split("|")[0].strip() if "|" in lot_no_value else lot_no_value

        # Compute quantity to subtract based on operation type
        operation = (production.operation or "").strip()
        prod_qty = Decimal(production.prod_qty or 0)
        
        if operation.startswith("10"):
            # ✅ For operation starting with "10": multiply prod_qty * BOMQty
            bom_qty = self.extract_bom_qty(original_parent_operation)
            qty_to_subtract = (prod_qty * bom_qty).quantize(Decimal("0.01"), rounding=Decimal.ROUND_DOWN)
            print(f"🔢 Operation 10 - prod_qty: {prod_qty}, BOMQty: {bom_qty}, qty_to_subtract: {qty_to_subtract}")
        else:
            # ✅ For other operations: just use prod_qty
            qty_to_subtract = prod_qty
            print(f"🔢 Other Operation - qty_to_subtract: {qty_to_subtract}")
        
        if qty_to_subtract <= 0:
            return production

        # FIFO subtraction from MaterialChallanTable
        remaining = Decimal(qty_to_subtract)
        for item in MaterialChallanTable.objects.filter(HeatNo__iexact=heat_no).order_by('id'):
            if remaining <= 0:
                break
            current_qty = Decimal(item.Qty or 0)
            if current_qty <= 0:
                continue
            to_subtract = min(current_qty, remaining)
            item.Qty = str(current_qty - to_subtract)
            item.save(update_fields=["Qty"])
            print(f"✓ ChallanTable {item.id} FIFO subtract: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={heat_no})")
            remaining -= to_subtract

        return production

    def update(self, instance, validated_data):
        # Store old values for restoration
        old_lot_no_value = (instance.lot_no or "").strip()
        old_heat_no = old_lot_no_value.split("|")[0].strip() if "|" in old_lot_no_value else old_lot_no_value
        
        # Compute old effective quantity using original ParentOperation
        old_qty_effective = self.compute_effective_qty(instance)

        # Capture original ParentOperation before updates
        original_parent_operation = validated_data.get('ParentOperation', instance.ParentOperation)

        # Apply updates to instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update ParentOperation if operation starts with '10'
        self.update_parent_operation_for_operation_10(instance, original_parent_operation=original_parent_operation)

        # ♻️ Restore old quantity first (add back to MaterialChallanTable)
        if old_qty_effective > 0:
            old_item = MaterialChallanTable.objects.filter(HeatNo__iexact=old_heat_no).order_by('id').first()
            if old_item:
                restored_val = Decimal(old_item.Qty or 0) + old_qty_effective
                old_item.Qty = str(restored_val)
                old_item.save(update_fields=["Qty"])
                print(f"♻️ Restored ChallanTable {old_item.id}: +{old_qty_effective} (HeatNo={old_heat_no})")

        # 🔻 Subtract new quantity
        new_lot_no_value = (instance.lot_no or "").strip()
        new_heat_no = new_lot_no_value.split("|")[0].strip() if "|" in new_lot_no_value else new_lot_no_value
        
        # Get new operation and prod_qty from validated_data or instance
        new_operation = validated_data.get('operation', instance.operation) or ""
        new_operation = new_operation.strip() if isinstance(new_operation, str) else str(new_operation).strip()
        new_prod_qty = Decimal(validated_data.get('prod_qty', instance.prod_qty) or 0)
        
        if new_operation.startswith("10"):
            # ✅ For operation starting with "10": multiply prod_qty * BOMQty
            bom_qty = self.extract_bom_qty(original_parent_operation)
            new_qty_effective = (new_prod_qty * bom_qty).quantize(Decimal("0.01"), rounding=Decimal.ROUND_DOWN)
            print(f"🔢 Updated Operation 10 - prod_qty: {new_prod_qty}, BOMQty: {bom_qty}, qty_to_subtract: {new_qty_effective}")
        else:
            # ✅ For other operations: just use prod_qty
            new_qty_effective = new_prod_qty
            print(f"🔢 Updated Other Operation - qty_to_subtract: {new_qty_effective}")
        
        if new_qty_effective <= 0:
            return instance

        # FIFO subtraction from MaterialChallanTable
        remaining_new = Decimal(new_qty_effective)
        for item in MaterialChallanTable.objects.filter(HeatNo__iexact=new_heat_no).order_by('id'):
            if remaining_new <= 0:
                break
            current_qty = Decimal(item.Qty or 0)
            if current_qty <= 0:
                continue
            to_subtract = min(current_qty, remaining_new)
            item.Qty = str(current_qty - to_subtract)
            item.save(update_fields=["Qty"])
            print(f"✓ Updated ChallanTable {item.id} FIFO: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={new_heat_no})")
            remaining_new -= to_subtract

        return instance





"""



import re
from decimal import Decimal, ROUND_DOWN
from rest_framework import serializers
class OOPurchaseSerializer(serializers.ModelSerializer):
    MachineIdleTime_Detail_Enter = MachineIdleTime_Detail_EnterSerializer(many=True)

    class Meta:
        model = ProductionEntry
        fields = '__all__'

    def get_parent_op_number(self, parent_operation):
            
        text = str(parent_operation or "")
        match = re.search(r"OP\s*:\s*(\d+)", text)
        return match.group(1) if match else None

    
    def subtract_from_parent_operation(self, production_entry):
        parent_op_no = self.get_parent_op_number(production_entry.ParentOperation)
        if not parent_op_no:
            print(" No parent OP found, skipping subtraction.")
            return

        current_op_no = str(production_entry.operation).split("|")[0].strip()

    # Prevent subtracting if current = parent (safety)
        if current_op_no == parent_op_no:
            return

        item = production_entry.item
        lot_no_first = str(production_entry.lot_no).split("|")[0].strip()
        
        prod_qty = Decimal(production_entry.prod_qty or 0)

    # Fetch latest parent entry
        parent_entry = ProductionEntry.objects.filter(
          item=item,
           lot_no__startswith=lot_no_first,
           operation__startswith=parent_op_no
           ).order_by("-id").first()

        if not parent_entry:
            print(" No parent operation entry found.")
            return

        parent_old_qty = Decimal(parent_entry.prod_qty or 0)
        parent_new_qty = parent_old_qty - prod_qty
        if parent_new_qty < 0:
            parent_new_qty = Decimal("0")

        parent_entry.prod_qty = str(parent_new_qty)
        parent_entry.save(update_fields=["prod_qty"])

        print(f"🔄 Updated Parent OP {parent_op_no}: {parent_old_qty} → {parent_new_qty}")




    # -------------------------------------------------------------
    # Helper: Extract BOMQty numeric value from ParentOperation string
    # -------------------------------------------------------------
    def extract_bom_qty(self, parent_operation):
        text = str(parent_operation or "")
        print(f"[EXTRACT_BOM] Input text: '{text}'", flush=True)
        match = re.search(r"BOMQty:\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
        if not match:
            print(f"⚠️ Could not extract BOMQty from: '{text}', defaulting to 1", flush=True)
            return Decimal("1")
        try:
            bom_qty = Decimal(match.group(1))
            print(f"✅ Extracted BOMQty: {bom_qty}", flush=True)
            return bom_qty
        except Exception as e:
            print(f"⚠️ Error extracting BOMQty: {e}, using default 1", flush=True)
            return Decimal("1")

    # -------------------------------------------------------------
    # Compute effective qty (depends on operation type)
    # -------------------------------------------------------------
    def compute_effective_qty(self, operation, prod_qty, parent_operation):
        print(f"[COMPUTE_QTY] START - operation={operation}, prod_qty={prod_qty}", flush=True)
        
        prod_qty = Decimal(str(prod_qty or 0))
        operation_str = str(operation or "").strip().replace(" ", "").replace("|", "")
        bom_qty = self.extract_bom_qty(parent_operation)

        print(f"DEBUG: operation_str={operation_str}, bom_qty={bom_qty}, prod_qty={prod_qty}", flush=True)

        # ✅ If operation starts with '10' → multiply prod_qty * BOMQty
        if operation_str.startswith("10"):
            effective = (prod_qty * bom_qty).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            print(f"✅ Operation starts with 10 → {prod_qty} × {bom_qty} = {effective}", flush=True)
            return effective

        # Otherwise → just prod_qty
        print(f"⚪ Operation not starting with 10 → Use prod_qty only = {prod_qty}", flush=True)
        return prod_qty

    # -------------------------------------------------------------
    # Update ParentOperation when operation starts with "10"
    # -------------------------------------------------------------
    def update_parent_operation_for_operation_10(self, production, original_parent_operation=None):
        print(f"[UPDATE_PARENT_OP] START - operation={production.operation}", flush=True)
        operation = str(production.operation or "").strip().replace(" ", "").replace("|", "")
        if not operation.startswith("10"):
            print(f"[UPDATE_PARENT_OP] Operation doesn't start with 10, skipping", flush=True)
            return

        prod_qty = Decimal(production.prod_qty or 0)
        parent_op_source = original_parent_operation if original_parent_operation is not None else production.ParentOperation
        original_bom_qty = self.extract_bom_qty(parent_op_source)

        new_bom_qty = (original_bom_qty * prod_qty) - prod_qty
        if new_bom_qty < 0:
            new_bom_qty = Decimal("0")

        new_bom_qty_str = str(new_bom_qty.quantize(Decimal("0.001")))
        production.ParentOperation = f"ScracpQty: N/A | BOMQty: {new_bom_qty_str}"
        production.save(update_fields=["ParentOperation"])

        print(f"📝 Updated ParentOperation for operation 10: BOMQty {original_bom_qty} → {new_bom_qty_str}", flush=True)

    # -------------------------------------------------------------
    # CREATE
    # -------------------------------------------------------------
    def create(self, validated_data):
        print("\n" + "="*80, flush=True)
        print("🚀 OOPurchaseSerializer.create() CALLED", flush=True)
        print("="*80 + "\n", flush=True)
        
        # Extract nested data
        MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
        
        # Store original ParentOperation before creating the object
        original_parent_operation = validated_data.get('ParentOperation', None)
        
        # Create production entry
        production_entry = ProductionEntry.objects.create(**validated_data)
       
        self.subtract_from_parent_operation(production_entry)

        print(f"✅ Created ProductionEntry: ID={production_entry.id}", flush=True)
        
        # Create related MachineIdleTime entries
        for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
            MachineIdleTime_Detail = MachineIdleTime.objects.create(**MachineIdleTime_data)
            production_entry.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)
        
        # Update ParentOperation if operation starts with "10"
        self.update_parent_operation_for_operation_10(production_entry, original_parent_operation=original_parent_operation)

        # Extract heat number
        lot_no_value = (production_entry.lot_no or "").strip()
        heat_no = lot_no_value.split("|")[0].strip() if "|" in lot_no_value else lot_no_value
        print(f"🔍 Extracted HeatNo: {heat_no}", flush=True)

        # Compute effective quantity based on operation type
        operation = (production_entry.operation or "").strip()
        prod_qty = Decimal(production_entry.prod_qty or 0)

        qty_to_subtract = self.compute_effective_qty(operation, prod_qty, original_parent_operation)
        
        # print(f"📊 Quantity to subtract: {qty_to_subtract}", flush=True)

        # if qty_to_subtract <= 0:
        #     print(f"⚠️ qty_to_subtract <= 0, skipping FIFO subtraction", flush=True)
        #     return production_entry
        
        # Subtract only when operation starts with 10
        operation_clean = str(operation).replace(" ", "").split("|")[0]

        if not operation_clean.startswith("10"):
            print("⏭️ Skipping FIFO subtraction — operation is not starting with 10", flush=True)
            return production_entry

        if qty_to_subtract <= 0:
            print(f"⚠️ qty_to_subtract <= 0, skipping FIFO subtraction", flush=True)
            return production_entry

# FIFO subtraction logic continues...

        

         



        # FIFO subtraction from MaterialChallanTable
        print(f"🔄 Starting FIFO subtraction for HeatNo: {heat_no}", flush=True)
        remaining = Decimal(qty_to_subtract)
        for item in MaterialChallanTable.objects.filter(HeatNo__iexact=heat_no).order_by('id'):
            if remaining <= 0:
                break
            current_qty = Decimal(item.Qty or 0)
            if current_qty <= 0:
                continue
            to_subtract = min(current_qty, remaining)
            item.Qty = str(current_qty - to_subtract)
            item.save(update_fields=["Qty"])
            print(f"✓ ChallanTable {item.id} FIFO subtract: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={heat_no})", flush=True)
            remaining -= to_subtract

        print(f"✅ OOPurchaseSerializer.create() COMPLETED\n", flush=True)
        


        return production_entry

    # -------------------------------------------------------------
    # UPDATE
    # -------------------------------------------------------------
    def update(self, instance, validated_data):
        print("\n" + "="*80, flush=True)
        print("🔄 OOPurchaseSerializer.update() CALLED", flush=True)
        print("="*80 + "\n", flush=True)
        
        # Extract nested data
        MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
        
        # Store old values for restoration
        old_lot_no_value = (instance.lot_no or "").strip()
        old_heat_no = old_lot_no_value.split("|")[0].strip() if "|" in old_lot_no_value else old_lot_no_value
        old_qty_effective = self.compute_effective_qty(instance.operation, instance.prod_qty, instance.ParentOperation)
        
        # Store original ParentOperation
        original_parent_operation = validated_data.get('ParentOperation', instance.ParentOperation)

        # Apply updates
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        print(f"✅ Updated ProductionEntry: ID={instance.id}", flush=True)

        # Update nested MachineIdleTime entries
        instance.MachineIdleTime_Detail_Enter.clear()
        for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
            MachineIdleTime_Detail = MachineIdleTime.objects.create(**MachineIdleTime_data)
            instance.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)

        # Update ParentOperation if operation starts with "10"
        self.update_parent_operation_for_operation_10(instance, original_parent_operation=original_parent_operation)

        # ♻️ Restore old quantity to MaterialChallanTable
        if old_qty_effective > 0:
            old_item = MaterialChallanTable.objects.filter(HeatNo__iexact=old_heat_no).order_by('id').first()
            if old_item:
                restored_val = Decimal(old_item.Qty or 0) + old_qty_effective
                old_item.Qty = str(restored_val)
                old_item.save(update_fields=["Qty"])
                print(f"♻️ Restored ChallanTable {old_item.id}: +{old_qty_effective} (HeatNo={old_heat_no})", flush=True)

        # Subtract new quantity
        new_lot_no_value = (instance.lot_no or "").strip()
        new_heat_no = new_lot_no_value.split("|")[0].strip() if "|" in new_lot_no_value else new_lot_no_value
        new_operation = validated_data.get('operation', instance.operation)
        new_prod_qty = Decimal(validated_data.get('prod_qty', instance.prod_qty) or 0)

        new_qty_effective = self.compute_effective_qty(new_operation, new_prod_qty, original_parent_operation)
        print(f"📊 New quantity to subtract: {new_qty_effective}", flush=True)

        # if new_qty_effective <= 0:
        #     print(f"⚠️ new_qty_effective <= 0, skipping FIFO subtraction", flush=True)
        #     return instance
        

        operation_clean = str(new_operation).replace(" ", "").split("|")[0]

        if not operation_clean.startswith("10"):
            print("⏭️ Skipping FIFO subtraction — operation is not starting with 10", flush=True)
            return instance

        if new_qty_effective <= 0:
            print(f"⚠️ new_qty_effective <= 0, skipping FIFO subtraction", flush=True)
            return instance

# FIFO subtraction continues...

        




        # FIFO subtraction
        print(f"🔄 Starting FIFO subtraction for HeatNo: {new_heat_no}", flush=True)
        remaining_new = Decimal(new_qty_effective)
        for item in MaterialChallanTable.objects.filter(HeatNo__iexact=new_heat_no).order_by('id'):
            if remaining_new <= 0:
                break
            current_qty = Decimal(item.Qty or 0)
            if current_qty <= 0:
                continue
            to_subtract = min(current_qty, remaining_new)
            item.Qty = str(current_qty - to_subtract)
            item.save(update_fields=["Qty"])
            print(f"✓ Updated ChallanTable {item.id} FIFO: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={new_heat_no})", flush=True)
            remaining_new -= to_subtract

        print(f"✅ OOPurchaseSerializer.update() COMPLETED\n", flush=True)
        return instance

    

"""










"""
import re
from decimal import Decimal, ROUND_DOWN
from rest_framework import serializers
class OOPurchaseSerializer(serializers.ModelSerializer):
    MachineIdleTime_Detail_Enter = MachineIdleTime_Detail_EnterSerializer(many=True)

    class Meta:
        model = ProductionEntry
        fields = '__all__'

    # -------------------------------------------------------------
    # Helper: Extract BOMQty numeric value from ParentOperation string
    # -------------------------------------------------------------
    def extract_bom_qty(self, parent_operation):
        text = str(parent_operation or "")
        print(f"[EXTRACT_BOM] Input text: '{text}'", flush=True)
        match = re.search(r"BOMQty:\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
        if not match:
            print(f"⚠️ Could not extract BOMQty from: '{text}', defaulting to 1", flush=True)
            return Decimal("1")
        try:
            bom_qty = Decimal(match.group(1))
            print(f"✅ Extracted BOMQty: {bom_qty}", flush=True)
            return bom_qty
        except Exception as e:
            print(f"⚠️ Error extracting BOMQty: {e}, using default 1", flush=True)
            return Decimal("1")

    # -------------------------------------------------------------
    # Compute effective qty (depends on operation type)
    # -------------------------------------------------------------
    def compute_effective_qty(self, operation, prod_qty, parent_operation):
        print(f"[COMPUTE_QTY] START - operation={operation}, prod_qty={prod_qty}", flush=True)
        
        prod_qty = Decimal(str(prod_qty or 0))
        operation_str = str(operation or "").strip().replace(" ", "").replace("|", "")
        bom_qty = self.extract_bom_qty(parent_operation)

        print(f"DEBUG: operation_str={operation_str}, bom_qty={bom_qty}, prod_qty={prod_qty}", flush=True)

        # ✅ If operation starts with '10' → multiply prod_qty * BOMQty
        if operation_str.startswith("10"):
            effective = (prod_qty * bom_qty).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            print(f"✅ Operation starts with 10 → {prod_qty} × {bom_qty} = {effective}", flush=True)
            return effective

        # Otherwise → just prod_qty
        print(f"⚪ Operation not starting with 10 → Use prod_qty only = {prod_qty}", flush=True)
        return prod_qty

    # -------------------------------------------------------------
    # Update ParentOperation when operation starts with "10"
    # -------------------------------------------------------------
    def update_parent_operation_for_operation_10(self, production, original_parent_operation=None):
        print(f"[UPDATE_PARENT_OP] START - operation={production.operation}", flush=True)
        operation = str(production.operation or "").strip().replace(" ", "").replace("|", "")
        if not operation.startswith("10"):
            print(f"[UPDATE_PARENT_OP] Operation doesn't start with 10, skipping", flush=True)
            return

        prod_qty = Decimal(production.prod_qty or 0)
        parent_op_source = original_parent_operation if original_parent_operation is not None else production.ParentOperation
        original_bom_qty = self.extract_bom_qty(parent_op_source)

        new_bom_qty = (original_bom_qty * prod_qty) - prod_qty
        if new_bom_qty < 0:
            new_bom_qty = Decimal("0")

        new_bom_qty_str = str(new_bom_qty.quantize(Decimal("0.001")))
        production.ParentOperation = f"ScracpQty: N/A | BOMQty: {new_bom_qty_str}"
        production.save(update_fields=["ParentOperation"])

        print(f"📝 Updated ParentOperation for operation 10: BOMQty {original_bom_qty} → {new_bom_qty_str}", flush=True)

    # -------------------------------------------------------------
    # CREATE
    # -------------------------------------------------------------
    def create(self, validated_data):
        print("\n" + "="*80, flush=True)
        print("🚀 OOPurchaseSerializer.create() CALLED", flush=True)
        print("="*80 + "\n", flush=True)
        
        # Extract nested data
        MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
        
        # Store original ParentOperation before creating the object
        original_parent_operation = validated_data.get('ParentOperation', None)
        
        # Create production entry
        production_entry = ProductionEntry.objects.create(**validated_data)
        print(f"✅ Created ProductionEntry: ID={production_entry.id}", flush=True)
        
        # Create related MachineIdleTime entries
        for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
            MachineIdleTime_Detail = MachineIdleTime.objects.create(**MachineIdleTime_data)
            production_entry.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)
        
        # Update ParentOperation if operation starts with "10"
        self.update_parent_operation_for_operation_10(production_entry, original_parent_operation=original_parent_operation)

        # Extract heat number
        lot_no_value = (production_entry.lot_no or "").strip()
        heat_no = lot_no_value.split("|")[0].strip() if "|" in lot_no_value else lot_no_value
        print(f"🔍 Extracted HeatNo: {heat_no}", flush=True)

        # Compute effective quantity based on operation type
        operation = (production_entry.operation or "").strip()
        prod_qty = Decimal(production_entry.prod_qty or 0)
        qty_to_subtract = self.compute_effective_qty(operation, prod_qty, original_parent_operation)
        
        print(f"📊 Quantity to subtract: {qty_to_subtract}", flush=True)

        if qty_to_subtract <= 0:
            print(f"⚠️ qty_to_subtract <= 0, skipping FIFO subtraction", flush=True)
            return production_entry

        # FIFO subtraction from MaterialChallanTable
        print(f"🔄 Starting FIFO subtraction for HeatNo: {heat_no}", flush=True)
        remaining = Decimal(qty_to_subtract)
        for item in MaterialChallanTable.objects.filter(HeatNo__iexact=heat_no).order_by('id'):
            if remaining <= 0:
                break
            current_qty = Decimal(item.Qty or 0)
            if current_qty <= 0:
                continue
            to_subtract = min(current_qty, remaining)
            item.Qty = str(current_qty - to_subtract)
            item.save(update_fields=["Qty"])
            print(f"✓ ChallanTable {item.id} FIFO subtract: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={heat_no})", flush=True)
            remaining -= to_subtract

        print(f"✅ OOPurchaseSerializer.create() COMPLETED\n", flush=True)
        


        return production_entry

    # -------------------------------------------------------------
    # UPDATE
    # -------------------------------------------------------------
    def update(self, instance, validated_data):
        print("\n" + "="*80, flush=True)
        print("🔄 OOPurchaseSerializer.update() CALLED", flush=True)
        print("="*80 + "\n", flush=True)
        
        # Extract nested data
        MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
        
        # Store old values for restoration
        old_lot_no_value = (instance.lot_no or "").strip()
        old_heat_no = old_lot_no_value.split("|")[0].strip() if "|" in old_lot_no_value else old_lot_no_value
        old_qty_effective = self.compute_effective_qty(instance.operation, instance.prod_qty, instance.ParentOperation)
        
        # Store original ParentOperation
        original_parent_operation = validated_data.get('ParentOperation', instance.ParentOperation)

        # Apply updates
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        print(f"✅ Updated ProductionEntry: ID={instance.id}", flush=True)

        # Update nested MachineIdleTime entries
        instance.MachineIdleTime_Detail_Enter.clear()
        for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
            MachineIdleTime_Detail = MachineIdleTime.objects.create(**MachineIdleTime_data)
            instance.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)

        # Update ParentOperation if operation starts with "10"
        self.update_parent_operation_for_operation_10(instance, original_parent_operation=original_parent_operation)

        # ♻️ Restore old quantity to MaterialChallanTable
        if old_qty_effective > 0:
            old_item = MaterialChallanTable.objects.filter(HeatNo__iexact=old_heat_no).order_by('id').first()
            if old_item:
                restored_val = Decimal(old_item.Qty or 0) + old_qty_effective
                old_item.Qty = str(restored_val)
                old_item.save(update_fields=["Qty"])
                print(f"♻️ Restored ChallanTable {old_item.id}: +{old_qty_effective} (HeatNo={old_heat_no})", flush=True)

        # Subtract new quantity
        new_lot_no_value = (instance.lot_no or "").strip()
        new_heat_no = new_lot_no_value.split("|")[0].strip() if "|" in new_lot_no_value else new_lot_no_value
        new_operation = validated_data.get('operation', instance.operation)
        new_prod_qty = Decimal(validated_data.get('prod_qty', instance.prod_qty) or 0)

        new_qty_effective = self.compute_effective_qty(new_operation, new_prod_qty, original_parent_operation)
        print(f"📊 New quantity to subtract: {new_qty_effective}", flush=True)

        if new_qty_effective <= 0:
            print(f"⚠️ new_qty_effective <= 0, skipping FIFO subtraction", flush=True)
            return instance

        # FIFO subtraction
        print(f"🔄 Starting FIFO subtraction for HeatNo: {new_heat_no}", flush=True)
        remaining_new = Decimal(new_qty_effective)
        for item in MaterialChallanTable.objects.filter(HeatNo__iexact=new_heat_no).order_by('id'):
            if remaining_new <= 0:
                break
            current_qty = Decimal(item.Qty or 0)
            if current_qty <= 0:
                continue
            to_subtract = min(current_qty, remaining_new)
            item.Qty = str(current_qty - to_subtract)
            item.save(update_fields=["Qty"])
            print(f"✓ Updated ChallanTable {item.id} FIFO: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={new_heat_no})", flush=True)
            remaining_new -= to_subtract

        print(f"✅ OOPurchaseSerializer.update() COMPLETED\n", flush=True)
        return instance
"""
    




# class OOPurchaseSerializer(serializers.ModelSerializer):
#     MachineIdleTime_Detail_Enter = MachineIdleTime_Detail_EnterSerializer(many=True)

#     class Meta:
#         model = ProductionEntry
#         fields = '__all__'

#     def create(self, validated_data):
#         MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
#         production_entry = ProductionEntry.objects.create(**validated_data)
        
#         for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
#             MachineIdleTime_Detail = MachineIdleTime.objects.create(**MachineIdleTime_data)
#             production_entry.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)

#         # After creating, subtract cumulatively for matching HeatNo
#         lot_no_value = (production_entry.lot_no or "").strip()
#         heat_no = lot_no_value.split("|")[0].strip() if "|" in lot_no_value else lot_no_value
#         qty_to_subtract = Decimal(production_entry.prod_qty or 0)

#         remaining = Decimal(qty_to_subtract)
#         for item in MaterialChallanTable.objects.filter(HeatNo__iexact=heat_no).order_by('id'):
#             if remaining <= 0:
#                 break
#             current_qty = Decimal(item.Qty or 0)
#             if current_qty <= 0:
#                 continue
#             to_subtract = min(current_qty, remaining)
#             item.Qty = str(current_qty - to_subtract)
#             item.save(update_fields=["Qty"])
#             print(f"✓ ChallanTable {item.id} FIFO subtract: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={heat_no})")
#             remaining -= to_subtract

#         return production_entry
    

# Production Entry Shift Time Serailizer :-Fetch
from All_Masters.models import Shift_Master_Model
class ProductionEntryShift(serializers.ModelSerializer):
    class Meta:
        model = Shift_Master_Model
        fields = '__all__'

# Production Entry Contractor:- Fetch
from All_Masters.models import Contractor_Master_Model
class ProductionEntryContractor(serializers.ModelSerializer):
    class Meta:
        model = Contractor_Master_Model
        fields = ['ContractorName']


# Production Entry Operator:- Fetch
from All_Masters.models import Add_New_Operator_Model
class ProductionOperatorSupervisor(serializers.ModelSerializer):
    class Meta:
        model = Add_New_Operator_Model
        fields = ['Name', 'Code', 'Type'] 


# Production Entry Fetch Unit Machine from Work Center Master
from All_Masters.models import Work_Center_Model
class ProductionEntryUnitMachine(serializers.ModelSerializer):
    class Meta: 
        model = Work_Center_Model
        fields = ['WorkCenterCode', 'WorkCenterName']




# Rework Production Entry 2
from rest_framework import serializers
from .models import ProductionEntry2, MachineIdleTime2

class MachineIdleTime_Detail_EnterSerializer2(serializers.ModelSerializer):
    class Meta:
        model = MachineIdleTime2
        fields = '__all__'

class ProductionEntrySerializer2(serializers.ModelSerializer):
    MachineIdleTime_Detail_Enter = MachineIdleTime_Detail_EnterSerializer2(many=True, read_only=True)

    class Meta:
        model = ProductionEntry2
        fields = '__all__'

class OOPurchaseSerializer2(serializers.ModelSerializer):
    MachineIdleTime_Detail_Enter = MachineIdleTime_Detail_EnterSerializer2(many=True)

    class Meta:
        model = ProductionEntry2
        fields = '__all__'

    def create(self, validated_data):
        MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
        production_entry = ProductionEntry2.objects.create(**validated_data)
        
        for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
            MachineIdleTime_Detail = MachineIdleTime2.objects.create(**MachineIdleTime_data)
            production_entry.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)

        return production_entry
    


# Rework Production: Rework production Entry

from rest_framework import serializers
from .models import ProductDetail2, Item2, ConsumptionDetails

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item2
        fields = ['id', 'item_desc', 'heat_code', 'rework_to_ok_qty', 'reject_to_ok_qty', 'rework_to_reject_qty']

class ConsumptionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumptionDetails
        fields = ['id', 'item_desc', 'heat_code', 'qty']

class ProductDetailSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    consumption_details = ConsumptionDetailsSerializer(many=True)
    user = serializers.StringRelatedField(read_only=True)  # Show the username in response

    class Meta:
        model = ProductDetail2
        fields = ['id', 'series', 'rework_no', 'rework_date', 'rework_time', 'machine', 'work_order', 'item_code',
                  'part_code', 'heat_code', 'rework_to_ok_qty', 'reject_to_ok_qty', 'change_fg', 'part_code2',
                  'heat_code2', 'reason_for_rework', 'quality_remark', 'operator', 'items', 'consumption_details', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        # Bulk create support
        if isinstance(validated_data, list):
            instances = []
            for entry in validated_data:
                items_data = entry.pop('items')
                consumption_data = entry.pop('consumption_details')
                product_detail = ProductDetail2.objects.create(user=user, **entry)

                for item in items_data:
                    Item2.objects.create(product_detail=product_detail, **item)
                for cons in consumption_data:
                    ConsumptionDetails.objects.create(product_detail=product_detail, **cons)

                instances.append(product_detail)
            return instances

        # Single create
        items_data = validated_data.pop('items')
        consumption_data = validated_data.pop('consumption_details')
        product_detail = ProductDetail2.objects.create(user=user, **validated_data)

        for item in items_data:
            Item2.objects.create(product_detail=product_detail, **item)
        for cons in consumption_data:
            ConsumptionDetails.objects.create(product_detail=product_detail, **cons)

        return product_detail

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        consumption_details_data = validated_data.pop('consumption_details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                Item2.objects.create(product_detail=instance, **item_data)

        if consumption_details_data is not None:
            instance.consumption_details.all().delete()
            for cons_data in consumption_details_data:
                ConsumptionDetails.objects.create(product_detail=instance, **cons_data)

        return instance

    


# Production Entry Assembly:-

from rest_framework import serializers
from .models import AssemblyProductionDetails, MachineIdleTimeAss, ItemStockDetails

class MachineIdleTimeAssSerializer(serializers.ModelSerializer):  # Renamed ItemSerializer
    class Meta:
        model = MachineIdleTimeAss
        fields = ["idle_reason", "from_time", "to_time", "total_time", "supervisor_operator", "setting_part", "remark"]
        

class ItemStockDetailsSerializer(serializers.ModelSerializer):  # Renamed ConsumptionDetailsSerializer
    class Meta:
        model = ItemStockDetails
        fields = ["Item_Group", "Alt_Item", "Item_No", "Item_Code", "Desc", "Bom_Qty", "Reg_Qty", "Stock"]

from .models import ReworkReason,RejectReason

class ReworkReasonSerializer(serializers.ModelSerializer):  # Renamed ConsumptionDetailsSerializer
    class Meta:
        model = ReworkReason
        fields = ["Description", "Qty"]
    

class RejectReasonSerializer(serializers.ModelSerializer):  # Renamed ConsumptionDetailsSerializer
    class Meta:
        model = RejectReason
        fields = ["Description", "Qty"]

class AssemblyProductionDetailsSerializer(serializers.ModelSerializer):
    MachineIdleTimeAss = MachineIdleTimeAssSerializer(many=True)  # Renamed items to MachineIdleTimeAss
    ItemStockDetails = ItemStockDetailsSerializer(many=True)  # Renamed consumption_details to ItemStockDetails
    ReworkReason = ReworkReasonSerializer(many=True) 
    RejectReason = RejectReasonSerializer(many=True) 

    class Meta:
        model = AssemblyProductionDetails
        fields = '__all__'

    def create(self, validated_data):
        machine_idle_time_ass_data = validated_data.pop('MachineIdleTimeAss')
        item_stock_details_data = validated_data.pop('ItemStockDetails')
        ReworkReason_details_data = validated_data.pop('ReworkReason')
        RejectReason_details_data = validated_data.pop('RejectReason')
        assembly_production_details = AssemblyProductionDetails.objects.create(**validated_data)

        for item_data in machine_idle_time_ass_data:
            MachineIdleTimeAss.objects.create(product_detail=assembly_production_details, **item_data)

        for consumption_data in item_stock_details_data:
            ItemStockDetails.objects.create(product_detail=assembly_production_details, **consumption_data)

        for  ReworkReason_data in ReworkReason_details_data:
            ReworkReason.objects.create(product_detail=assembly_production_details, ** ReworkReason_data)
        
        for RejectReason_data in RejectReason_details_data:
            RejectReason.objects.create(product_detail=assembly_production_details, **RejectReason_data)

        return assembly_production_details

    def update(self, instance, validated_data):
        machine_idle_time_ass_data = validated_data.pop('MachineIdleTimeAss', None)
        item_stock_details_data = validated_data.pop('ItemStockDetails', None)
        ReworkReason_details_data = validated_data.pop('ReworkReason', None)
        RejectReason_details_data = validated_data.pop('RejectReason', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if machine_idle_time_ass_data:
            instance.MachineIdleTimeAss.all().delete()
            for item_data in machine_idle_time_ass_data:
                MachineIdleTimeAss.objects.create(product_detail=instance, **item_data)

        if item_stock_details_data:
            instance.ItemStockDetails.all().delete()
            for consumption_data in item_stock_details_data:
                ItemStockDetails.objects.create(product_detail=instance, **consumption_data)
        
        if ReworkReason_details_data:
            instance.ReworkReason.all().delete()
            for ReworkReason_data in ReworkReason_details_data:
                ReworkReason.objects.create(product_detail=instance, **ReworkReason_data)

        if RejectReason_details_data:
            instance.RejectReason.all().delete()
            for RejectReason_data in RejectReason_details_data:
                RejectReason.objects.create(product_detail=instance, **RejectReason_data)

        return instance

from .models import ReworkReason2,RejectReason2

class ReworkReason2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ReworkReason2
        fields = '__all__'

class RejectReason2Serializer(serializers.ModelSerializer):
    class Meta:
        model = RejectReason2
        fields = '__all__'
    

# Contractor Production Entry

from rest_framework import serializers
from .models import ProductionRecord

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRecord
        fields = "__all__"



# FG Scrap Rejection Note
from rest_framework import serializers
from .models import FGScrapDetails, FGScrapItem

class FGScrapItemSerializer(serializers.ModelSerializer):  
    class Meta:
        model = FGScrapItem
        fields = ["ItemDescription", "HeatCode", "ReworkQty", "Reason", "RejectQty", "Reason2", "ScrapWt"]

class FGScrapDetailsSerializer(serializers.ModelSerializer):
    scrap_items = FGScrapItemSerializer(many=True)  # Matches related_name in the model
    
    class Meta:
        model = FGScrapDetails
        fields = '__all__'

    def create(self, validated_data):
        scrap_items_data = validated_data.pop('scrap_items')
        scrap_detail = FGScrapDetails.objects.create(**validated_data)

        for item_data in scrap_items_data:
            FGScrapItem.objects.create(ItemDesc=scrap_detail, **item_data)

        return scrap_detail

    def update(self, instance, validated_data):
        scrap_items_data = validated_data.pop('scrap_items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if scrap_items_data:
            instance.scrap_items.all().delete()
            for item_data in scrap_items_data:
                FGScrapItem.objects.create(ItemDesc=instance, **item_data)

        return instance


# Scrap Line Rejection Note
from rest_framework import serializers
from .models import ScrapLineRejectionNote, ScrapLineRejectionNoteDetails

class ScrapRejectSerializer(serializers.ModelSerializer):  
    class Meta:
        model = ScrapLineRejectionNoteDetails
        fields = ["ItemNo", "ScrapRejectionQty", "ReasonNote", "RejectReason", "ScrapRejectionItem","ScrapQty"]

class ScrapRejectDetailsSerializer(serializers.ModelSerializer):
    scrap_items = ScrapRejectSerializer(many=True)  # Matches related_name in the model
    
    class Meta:
        model = ScrapLineRejectionNote
        fields = '__all__'

    def create(self, validated_data):
        scrap_items_data = validated_data.pop('scrap_items')
        scrap_detail = ScrapLineRejectionNote.objects.create(**validated_data)

        for item_data in scrap_items_data:
            ScrapLineRejectionNoteDetails.objects.create(ItemDesc=scrap_detail, **item_data)

        return scrap_detail

    def update(self, instance, validated_data):
        scrap_items_data = validated_data.pop('scrap_items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if scrap_items_data:
            instance.scrap_items.all().delete()
            for item_data in scrap_items_data:
                ScrapLineRejectionNoteDetails.objects.create(ItemDesc=instance, **item_data)

        return instance
    
# New Work Order 
from rest_framework import serializers
from .models import WorkOrderEntry

# Work Order Customer_supplier Search
from All_Masters.models import Item
class WO_Customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'Name', 'number']

# New Work Order 
from .models import NewWorkOrderItem
class New_Work_Oder_Item_Serializer(serializers.ModelSerializer):   # Renamed items to MachineIdleTimeAss
    class Meta:
        model = NewWorkOrderItem
        fields = ["Purchase_order_detail", "item", "Description", "SO_Sch_Qty", "Bal_Qty", "Work_Order_Qty", "Remark", "Machine", "Shift", "Process", "Raw_Material"]


class WorkOrderSerializer(serializers.ModelSerializer):
    NewWorkOrderItem = New_Work_Oder_Item_Serializer(many=True)

    class Meta:
        model = WorkOrderEntry
        fields = '__all__'

    def create(self, validated_data):
        Work_Order_detail_data = validated_data.pop('NewWorkOrderItem')
        Work_Order_entry_details = WorkOrderEntry.objects.create(**validated_data)

        for item_data in Work_Order_detail_data:
            NewWorkOrderItem.objects.create(Work_Order_detail=Work_Order_entry_details, **item_data)

        return Work_Order_entry_details

    def update(self, instance, validated_data):
        Work_Order_detail_data = validated_data.pop('NewWorkOrderItem', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if Work_Order_detail_data:
            instance.NewWorkOrderItem.all().delete()
            for item_data in Work_Order_detail_data:
                NewWorkOrderItem.objects.create(Work_Order_detail=instance, **item_data)

        return instance
    

##
from rest_framework import serializers
from .models import ProductDetail2, Item2, ConsumptionDetails

class ProductDetailGetSerializer(serializers.ModelSerializer):
    part_no = serializers.SerializerMethodField()
    Part_Code = serializers.SerializerMethodField()
    Name_Description = serializers.SerializerMethodField()

    OPNo = serializers.SerializerMethodField()
    PartCode = serializers.SerializerMethodField()

    change_fg_part_no = serializers.SerializerMethodField()
    change_fg_Part_Code = serializers.SerializerMethodField()
    change_fg_Name_Description = serializers.SerializerMethodField()

    OPNo2 = serializers.SerializerMethodField()
    PartCode2 = serializers.SerializerMethodField()

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductDetail2
        fields = [
            'Plant', 'rework_no', 'rework_date',
            'part_no', 'Part_Code', 'Name_Description',
            'OPNo', 'PartCode',
            'change_fg_part_no', 'change_fg_Part_Code', 'change_fg_Name_Description',
            'OPNo2', 'PartCode2',
            'rework_to_ok_qty', 'reject_to_ok_qty',
            'reason_for_rework', 'quality_remark', 'user'
        ]

    # Helpers
    def split_item_code(self, value, expected_parts=3):
        if value:
            parts = [x.strip() for x in value.split('|')]
            while len(parts) < expected_parts:
                parts.append("")
            return parts
        return [""] * expected_parts

    def split_part_code(self, value, expected_parts=2):
        if value:
            parts = [x.strip() for x in value.split('|')]
            while len(parts) < expected_parts:
                parts.append("")
            return parts
        return [""] * expected_parts

    # item_code
    def get_part_no(self, obj):
        return self.split_item_code(obj.item_code)[0]

    def get_Part_Code(self, obj):
        return self.split_item_code(obj.item_code)[1]

    def get_Name_Description(self, obj):
        return self.split_item_code(obj.item_code)[2]

    # part_code
    def get_OPNo(self, obj):
        return self.split_part_code(obj.part_code)[0]

    def get_PartCode(self, obj):
        return self.split_part_code(obj.part_code)[1]

    # change_fg
    def get_change_fg_part_no(self, obj):
        return self.split_item_code(obj.change_fg)[0]

    def get_change_fg_Part_Code(self, obj):
        return self.split_item_code(obj.change_fg)[1]

    def get_change_fg_Name_Description(self, obj):
        return self.split_item_code(obj.change_fg)[2]

    # part_code2
    def get_OPNo2(self, obj):
        return self.split_part_code(obj.part_code2)[0]

    def get_PartCode2(self, obj):
        return self.split_part_code(obj.part_code2)[1]


from All_Masters.models import *
from All_Masters.models import ItemTable
class ItemdropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTable
        fields= ['Part_Code','part_no' , 'Name_Description']

class BOMItemdropSerializer(serializers.ModelSerializer):
    item_part_code = serializers.CharField(source='item.Part_Code', read_only=True)
    class Meta:
        model = BOMItem
        fields = ['item_part_code','OPNo', 'PartCode','ScracpQty','WipWt','WipRate','QtyKg']









# import re
# from decimal import Decimal, ROUND_DOWN
# from rest_framework import serializers
# from Store.models import InwardChallanTable
# from django.db.models import Q
# from All_Masters.models import ItemTable,BOMItem
# class OOPurchaseSerializer(serializers.ModelSerializer):
#     MachineIdleTime_Detail_Enter = MachineIdleTime_Detail_EnterSerializer(many=True)

#     class Meta:
#         model = ProductionEntry
#         fields = '__all__'

#     def get_parent_op_number(self, parent_operation):
            
#         text = str(parent_operation or "")
#         match = re.search(r"OP\s*:\s*(\d+)", text)
#         return match.group(1) if match else None


    

#     def get_parent_inward_queryset(self, production_entry, parent_op_no):
#         """
#         Returns FIFO queryset of matching InwardChallanTable records
#         using the same RM / FG logic as HeatSummaryAPIView.
#         """

#         part_no = (
#              production_entry.ItemCode
#              or production_entry.item
#              or ""
#            ).strip()

#         # If item contains "FGFG1001 - CAP OIL LOCK"
#         # take only the part number.
#         if " - " in part_no:
#             part_no = part_no.split(" - ")[0].strip()

#         try:
#             fg_item = ItemTable.objects.prefetch_related("bom_items").get(
#                 Q(part_no__iexact=part_no)
#                 | Q(Part_Code__iexact=part_no)
#                 | Q(Name_Description__iexact=part_no)
#             )
#         except ItemTable.DoesNotExist:
#             return InwardChallanTable.objects.none()

#         rm_part = None

#         bom_items = BOMItem.objects.filter(item=fg_item).order_by("OPNo")

#         for bom in bom_items:
#             if str(bom.OPNo) == "10":
#                 rm_part = bom.BomPartCode
#                 break

#         heat = str(production_entry.lot_no or "").split("|")[0].strip()

#         inward_qs = InwardChallanTable.objects.filter(
#             heat_no__iexact=heat
#         ).order_by("id")

#         matched_ids = []

#         for inward in inward_qs:

#             item_desc = (inward.ItemDescription or "").strip()

#             operation = None

#             if rm_part and item_desc.startswith(rm_part):

#                 op = (inward.opno or "").upper().replace(" ", "")

#                 m = re.search(r"OP:?(\d+)", op)

#                 if m:
#                     operation = m.group(1)
#                 else:
#                     operation = op.replace("OP", "").replace(":", "")

#             elif f"Part: {part_no}" in item_desc:

#                 m = re.search(r"Op:\s*OP:(\d+)", item_desc)

#                 if m:
#                     operation = m.group(1)

#             if operation == str(parent_op_no):
#                 matched_ids.append(inward.id)

#         return InwardChallanTable.objects.filter(
#             id__in=matched_ids
#         ).order_by("id")


#     def subtract_from_inward(self, production_entry, parent_op_no, qty):

#         remaining = Decimal(qty)

#         inward_rows = self.get_parent_inward_queryset(
#             production_entry,
#             parent_op_no
#         )

#         if not inward_rows.exists():
#             print("❌ No matching inward stock found.")
#             return

#         print(f"📦 Remaining to consume from Inward = {remaining}")

#         for inward in inward_rows:

#             if remaining <= 0:
#                 break

#             current_qty = Decimal(inward.ChallanQty or 0)

#             if current_qty <= 0:
#                 continue

#             consume = min(current_qty, remaining)

#             inward.ChallanQty = str(current_qty - consume)

#             inward.save(update_fields=["ChallanQty"])

#             print(
#                 f"✓ Inward {inward.id}: "
#                 f"{current_qty} -> {inward.ChallanQty}"
#             )

#             remaining -= consume

#         if remaining > 0:
#             print(
#                 f"⚠ Still Remaining after inward consumption = {remaining}"
#             )


    


    
        
#     def subtract_from_parent_operation(self, production_entry):

#         parent_op_no = self.get_parent_op_number(
#             production_entry.ParentOperation
#         )

#         if not parent_op_no:
#             print("❌ No parent operation found.")
#             return

#         current_op_no = str(
#             production_entry.operation or ""
#         ).split("|")[0].strip()

#         # Safety
#         if current_op_no == parent_op_no:
#             return

#         item = production_entry.item

#         heat_no = str(
#             production_entry.lot_no or ""
#         ).split("|")[0].strip()

#         required_qty = Decimal(
#             production_entry.prod_qty or 0
#         )

#         print(
#             f"\n🔄 Need Parent Stock = {required_qty}"
#             f"\nParent OP = {parent_op_no}"
#             f"\nHeat = {heat_no}"
#         )

#         parent_entries = ProductionEntry.objects.filter(
#             item=item,
#             lot_no__startswith=heat_no,
#             operation__startswith=parent_op_no
#         ).order_by("-id")

#         remaining = Decimal(required_qty)

#         # ---------------------------------------------------------
#         # STEP-1
#         # Consume Parent Production first
#         # ---------------------------------------------------------

#         for parent in parent_entries:

#             if remaining <= 0:
#                 break

#             current_qty = Decimal(parent.prod_qty or 0)

#             if current_qty <= 0:
#                 continue

#             consume = min(current_qty, remaining)

#             parent.prod_qty = str(current_qty - consume)

#             parent.save(update_fields=["prod_qty"])

#             print(
#                 f"✅ Parent Production {parent.id}"
#                 f" : {current_qty} -> {parent.prod_qty}"
#             )

#             remaining -= consume

#         # ---------------------------------------------------------
#         # STEP-2
#         # Remaining -> Inward FIFO
#         # ---------------------------------------------------------

#         if remaining > 0:

#             print(
#                 f"📦 Production insufficient."
#                 f"\nRemaining={remaining}"
#                 f"\nTrying Inward..."
#             )

#             self.subtract_from_inward(
#                 production_entry,
#                 parent_op_no,
#                 remaining
#             )

#         else:

#             print("✅ Fully consumed from Production.")


#     # -------------------------------------------------------------
#     # Helper: Extract BOMQty numeric value from ParentOperation string
#     # -------------------------------------------------------------
#     def extract_bom_qty(self, parent_operation):
#         text = str(parent_operation or "")
#         print(f"[EXTRACT_BOM] Input text: '{text}'", flush=True)
#         match = re.search(r"BOMQty:\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
#         if not match:
#             print(f"⚠️ Could not extract BOMQty from: '{text}', defaulting to 1", flush=True)
#             return Decimal("1")
#         try:
#             bom_qty = Decimal(match.group(1))
#             print(f"✅ Extracted BOMQty: {bom_qty}", flush=True)
#             return bom_qty
#         except Exception as e:
#             print(f"⚠️ Error extracting BOMQty: {e}, using default 1", flush=True)
#             return Decimal("1")

#     # -------------------------------------------------------------
#     # Compute effective qty (depends on operation type)
#     # -------------------------------------------------------------
#     def compute_effective_qty(self, operation, prod_qty, parent_operation):
#         print(f"[COMPUTE_QTY] START - operation={operation}, prod_qty={prod_qty}", flush=True)
        
#         prod_qty = Decimal(str(prod_qty or 0))
#         operation_str = str(operation or "").strip().replace(" ", "").replace("|", "")
#         bom_qty = self.extract_bom_qty(parent_operation)

#         print(f"DEBUG: operation_str={operation_str}, bom_qty={bom_qty}, prod_qty={prod_qty}", flush=True)

#         # ✅ If operation starts with '10' → multiply prod_qty * BOMQty
#         if operation_str.startswith("10"):
#             effective = (prod_qty * bom_qty).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
#             print(f"✅ Operation starts with 10 → {prod_qty} × {bom_qty} = {effective}", flush=True)
#             return effective

#         # Otherwise → just prod_qty
#         print(f"⚪ Operation not starting with 10 → Use prod_qty only = {prod_qty}", flush=True)
#         return prod_qty

#     # -------------------------------------------------------------
#     # Update ParentOperation when operation starts with "10"
#     # -------------------------------------------------------------
#     def update_parent_operation_for_operation_10(self, production, original_parent_operation=None):
#         print(f"[UPDATE_PARENT_OP] START - operation={production.operation}", flush=True)
#         operation = str(production.operation or "").strip().replace(" ", "").replace("|", "")
#         if not operation.startswith("10"):
#             print(f"[UPDATE_PARENT_OP] Operation doesn't start with 10, skipping", flush=True)
#             return

#         prod_qty = Decimal(production.prod_qty or 0)
#         parent_op_source = original_parent_operation if original_parent_operation is not None else production.ParentOperation
#         original_bom_qty = self.extract_bom_qty(parent_op_source)

#         new_bom_qty = (original_bom_qty * prod_qty) - prod_qty
#         if new_bom_qty < 0:
#             new_bom_qty = Decimal("0")

#         new_bom_qty_str = str(new_bom_qty.quantize(Decimal("0.001")))
#         production.ParentOperation = f"ScracpQty: N/A | BOMQty: {new_bom_qty_str}"
#         production.save(update_fields=["ParentOperation"])

#         print(f"📝 Updated ParentOperation for operation 10: BOMQty {original_bom_qty} → {new_bom_qty_str}", flush=True)

#     # -------------------------------------------------------------
#     # CREATE
#     # -------------------------------------------------------------
#     def create(self, validated_data):
#         print("\n" + "="*80, flush=True)
#         print("🚀 OOPurchaseSerializer.create() CALLED", flush=True)
#         print("="*80 + "\n", flush=True)
        
#         # Extract nested data
#         MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
        
#         # Store original ParentOperation before creating the object
#         original_parent_operation = validated_data.get('ParentOperation', None)
        
#         # Create production entry
#         production_entry = ProductionEntry.objects.create(**validated_data)
       
#         self.subtract_from_parent_operation(production_entry)

#         print(f"✅ Created ProductionEntry: ID={production_entry.id}", flush=True)
        
#         # Create related MachineIdleTime entries
#         for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
#             MachineIdleTime_Detail = MachineIdleTime.objects.create(**MachineIdleTime_data)
#             production_entry.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)
        
#         # Update ParentOperation if operation starts with "10"
#         self.update_parent_operation_for_operation_10(production_entry, original_parent_operation=original_parent_operation)

#         # Extract heat number
#         lot_no_value = (production_entry.lot_no or "").strip()
#         heat_no = lot_no_value.split("|")[0].strip() if "|" in lot_no_value else lot_no_value
#         print(f"🔍 Extracted HeatNo: {heat_no}", flush=True)

#         # Compute effective quantity based on operation type
#         operation = (production_entry.operation or "").strip()
#         prod_qty = Decimal(production_entry.prod_qty or 0)

#         qty_to_subtract = self.compute_effective_qty(operation, prod_qty, original_parent_operation)
        
#         # print(f"📊 Quantity to subtract: {qty_to_subtract}", flush=True)

#         # if qty_to_subtract <= 0:
#         #     print(f"⚠️ qty_to_subtract <= 0, skipping FIFO subtraction", flush=True)
#         #     return production_entry
        
#         # Subtract only when operation starts with 10
#         operation_clean = str(operation).replace(" ", "").split("|")[0]

#         if not operation_clean.startswith("10"):
#             print("⏭️ Skipping FIFO subtraction — operation is not starting with 10", flush=True)
#             return production_entry

#         if qty_to_subtract <= 0:
#             print(f"⚠️ qty_to_subtract <= 0, skipping FIFO subtraction", flush=True)
#             return production_entry

# # FIFO subtraction logic continues...

        

         



#         # FIFO subtraction from MaterialChallanTable
#         print(f"🔄 Starting FIFO subtraction for HeatNo: {heat_no}", flush=True)
#         remaining = Decimal(qty_to_subtract)
#         for item in MaterialChallanTable.objects.filter(HeatNo__iexact=heat_no).order_by('id'):
#             if remaining <= 0:
#                 break
#             current_qty = Decimal(item.Qty or 0)
#             if current_qty <= 0:
#                 continue
#             to_subtract = min(current_qty, remaining)
#             item.Qty = str(current_qty - to_subtract)
#             item.save(update_fields=["Qty"])
#             print(f"✓ ChallanTable {item.id} FIFO subtract: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={heat_no})", flush=True)
#             remaining -= to_subtract

#         print(f"✅ OOPurchaseSerializer.create() COMPLETED\n", flush=True)
        


#         return production_entry

#     # -------------------------------------------------------------
#     # UPDATE
#     # -------------------------------------------------------------
#     def update(self, instance, validated_data):
#         print("\n" + "="*80, flush=True)
#         print("🔄 OOPurchaseSerializer.update() CALLED", flush=True)
#         print("="*80 + "\n", flush=True)
        
#         # Extract nested data
#         MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
        
#         # Store old values for restoration
#         old_lot_no_value = (instance.lot_no or "").strip()
#         old_heat_no = old_lot_no_value.split("|")[0].strip() if "|" in old_lot_no_value else old_lot_no_value
#         old_qty_effective = self.compute_effective_qty(instance.operation, instance.prod_qty, instance.ParentOperation)
        
#         # Store original ParentOperation
#         original_parent_operation = validated_data.get('ParentOperation', instance.ParentOperation)

#         # Apply updates
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         print(f"✅ Updated ProductionEntry: ID={instance.id}", flush=True)

#         # Update nested MachineIdleTime entries
#         instance.MachineIdleTime_Detail_Enter.clear()
#         for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
#             MachineIdleTime_Detail = MachineIdleTime.objects.create(**MachineIdleTime_data)
#             instance.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)

#         # Update ParentOperation if operation starts with "10"
#         self.update_parent_operation_for_operation_10(instance, original_parent_operation=original_parent_operation)

#         # ♻️ Restore old quantity to MaterialChallanTable
#         if old_qty_effective > 0:
#             old_item = MaterialChallanTable.objects.filter(HeatNo__iexact=old_heat_no).order_by('id').first()
#             if old_item:
#                 restored_val = Decimal(old_item.Qty or 0) + old_qty_effective
#                 old_item.Qty = str(restored_val)
#                 old_item.save(update_fields=["Qty"])
#                 print(f"♻️ Restored ChallanTable {old_item.id}: +{old_qty_effective} (HeatNo={old_heat_no})", flush=True)

#         # Subtract new quantity
#         new_lot_no_value = (instance.lot_no or "").strip()
#         new_heat_no = new_lot_no_value.split("|")[0].strip() if "|" in new_lot_no_value else new_lot_no_value
#         new_operation = validated_data.get('operation', instance.operation)
#         new_prod_qty = Decimal(validated_data.get('prod_qty', instance.prod_qty) or 0)

#         new_qty_effective = self.compute_effective_qty(new_operation, new_prod_qty, original_parent_operation)
#         print(f"📊 New quantity to subtract: {new_qty_effective}", flush=True)

#         # if new_qty_effective <= 0:
#         #     print(f"⚠️ new_qty_effective <= 0, skipping FIFO subtraction", flush=True)
#         #     return instance
        

#         operation_clean = str(new_operation).replace(" ", "").split("|")[0]

#         if not operation_clean.startswith("10"):
#             print("⏭️ Skipping FIFO subtraction — operation is not starting with 10", flush=True)
#             return instance

#         if new_qty_effective <= 0:
#             print(f"⚠️ new_qty_effective <= 0, skipping FIFO subtraction", flush=True)
#             return instance

#         # FIFO subtraction continues...

        




#         # FIFO subtraction
#         print(f"🔄 Starting FIFO subtraction for HeatNo: {new_heat_no}", flush=True)
#         remaining_new = Decimal(new_qty_effective)
#         for item in MaterialChallanTable.objects.filter(HeatNo__iexact=new_heat_no).order_by('id'):
#             if remaining_new <= 0:
#                 break
#             current_qty = Decimal(item.Qty or 0)
#             if current_qty <= 0:
#                 continue
#             to_subtract = min(current_qty, remaining_new)
#             item.Qty = str(current_qty - to_subtract)
#             item.save(update_fields=["Qty"])
#             print(f"✓ Updated ChallanTable {item.id} FIFO: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={new_heat_no})", flush=True)
#             remaining_new -= to_subtract

#         print(f"✅ OOPurchaseSerializer.update() COMPLETED\n", flush=True)
#         return instance


"""This is the final working on both side server and local
In this Production and Inwardchallan both side heat no wise stock will subtract"""
import re
from decimal import Decimal, ROUND_DOWN
from rest_framework import serializers
from Store.models import InwardChallanTable
from django.db.models import Q
from All_Masters.models import ItemTable,BOMItem
class OOPurchaseSerializer(serializers.ModelSerializer):
    MachineIdleTime_Detail_Enter = MachineIdleTime_Detail_EnterSerializer(many=True)

    class Meta:
        model = ProductionEntry
        fields = '__all__'

    def get_parent_op_number(self, parent_operation):
            
        text = str(parent_operation or "")
        match = re.search(r"OP\s*:\s*(\d+)", text)
        return match.group(1) if match else None


    

    def get_parent_inward_queryset(self, production_entry, parent_op_no):
        """
        Return FIFO matching InwardChallan rows.

        Matching Rules:
        1. Same Heat No
        2. Same Parent Operation
        3. Match RM / Semi / FG Part from BOM
        """

        # -------------------------------------------------
        # FG Part
        # production_entry.item =
        # "FG1013 | B2AW | BLEEDER-REM"
        # -------------------------------------------------

        item_text = (production_entry.item or "").strip()

        fg_part = item_text.split("|")[0].strip()

        heat_no = (production_entry.lot_no or "").split("|")[0].strip()

        print("=" * 70)
        print("Searching Parent Inward")
        print("FG Part :", fg_part)
        print("Parent OP :", parent_op_no)
        print("Heat :", heat_no)
        print("=" * 70)

        # -------------------------------------------------
        # Parent BOM
        # -------------------------------------------------

        bom = (
            BOMItem.objects
            .filter(
                item__part_no=fg_part,
                OPNo=str(parent_op_no)
            )
            .first()
        )

        if not bom:
            print(
                f"❌ BOM not found "
                f"(FG={fg_part}, OP={parent_op_no})"
            )
            return InwardChallanTable.objects.none()

        search_parts = []

        if bom.BomPartCode:
            search_parts.append(bom.BomPartCode.strip())

        if bom.PartCode:
            search_parts.append(bom.PartCode.strip())

        print("Search Parts :", search_parts)

        # -------------------------------------------------
        # Heat Wise FIFO
        # -------------------------------------------------

        inward_qs = (
            InwardChallanTable.objects
            .filter(
                heat_no__iexact=heat_no
            )
            .order_by("id")
        )

        matched_ids = []

        for inward in inward_qs:

            item_desc = (inward.ItemDescription or "").strip()

            # ---------------------------------------------
            # RM Inward
            # ---------------------------------------------
            if inward.opno:

                op = inward.opno.upper().replace(" ", "")

                m = re.search(r"OP:?(\d+)", op)

                if m:
                    inward_op = m.group(1)
                else:
                    inward_op = op.replace("OP", "").replace(":", "")

                if inward_op != str(parent_op_no):
                    continue

                print(
                    f"✓ RM Inward Matched "
                    f"ID={inward.id} "
                    f"OP={inward.opno}"
                )

                matched_ids.append(inward.id)
                continue

            # ---------------------------------------------
            # FG Inward (Old Logic)
            # ---------------------------------------------

            matched = False

            for part in search_parts:
                if part and part in item_desc:
                    matched = True
                    break

            if not matched:
                if f"Part: {fg_part}" in item_desc:
                    matched = True

            if not matched:
                continue

            # Extract OP from ItemDescription
            m = re.search(r"Op:\s*OP:(\d+)", item_desc)

            if m and m.group(1) != str(parent_op_no):
                continue

            print(
                f"✓ FG Inward Matched "
                f"ID={inward.id}"
            )

            matched_ids.append(inward.id)
        rows = (
            InwardChallanTable.objects
            .filter(id__in=matched_ids)
            .order_by("id")
        )

        print(
            f"Total Matched Rows = {rows.count()}"
        )

        return rows

    def subtract_from_inward(self, production_entry, parent_op_no, qty):

        remaining = Decimal(qty)

        inward_rows = self.get_parent_inward_queryset(
            production_entry,
            parent_op_no
        )

        if not inward_rows.exists():
            print("❌ No matching inward stock found.")
            return

        print(f"📦 Remaining to consume from Inward = {remaining}")

        for inward in inward_rows:

            if remaining <= 0:
                break

            current_qty = Decimal(inward.ChallanQty or 0)

            if current_qty <= 0:
                continue

            consume = min(current_qty, remaining)

            inward.ChallanQty = str(current_qty - consume)

            inward.save(update_fields=["ChallanQty"])

            print(
                f"✓ Inward {inward.id}: "
                f"{current_qty} -> {inward.ChallanQty}"
            )

            remaining -= consume

        if remaining > 0:
            print(
                f"⚠ Still Remaining after inward consumption = {remaining}"
            )


    


    
        
    def subtract_from_parent_operation(self, production_entry):

        parent_op_no = self.get_parent_op_number(
            production_entry.ParentOperation
        )

        if not parent_op_no:
            print("❌ No parent operation found.")
            return

        current_op_no = str(
            production_entry.operation or ""
        ).split("|")[0].strip()

        # Safety
        if current_op_no == parent_op_no:
            return

        item = production_entry.item

        heat_no = str(
            production_entry.lot_no or ""
        ).split("|")[0].strip()

        required_qty = Decimal(
            production_entry.prod_qty or 0
        )

        print(
            f"\n🔄 Need Parent Stock = {required_qty}"
            f"\nParent OP = {parent_op_no}"
            f"\nHeat = {heat_no}"
        )

        parent_entries = ProductionEntry.objects.filter(
            item=item,
            lot_no__startswith=heat_no,
            operation__startswith=parent_op_no
        ).order_by("-id")

        remaining = Decimal(required_qty)

        # ---------------------------------------------------------
        # STEP-1
        # Consume Parent Production first
        # ---------------------------------------------------------

        for parent in parent_entries:

            if remaining <= 0:
                break

            current_qty = Decimal(parent.prod_qty or 0)

            if current_qty <= 0:
                continue

            consume = min(current_qty, remaining)

            parent.prod_qty = str(current_qty - consume)

            parent.save(update_fields=["prod_qty"])

            print(
                f"✅ Parent Production {parent.id}"
                f" : {current_qty} -> {parent.prod_qty}"
            )

            remaining -= consume

        # ---------------------------------------------------------
        # STEP-2
        # Remaining -> Inward FIFO
        # ---------------------------------------------------------

        if remaining > 0:

            print(
                f"📦 Production insufficient."
                f"\nRemaining={remaining}"
                f"\nTrying Inward..."
            )

            self.subtract_from_inward(
                production_entry,
                parent_op_no,
                remaining
            )

        else:

            print("✅ Fully consumed from Production.")


    # -------------------------------------------------------------
    # Helper: Extract BOMQty numeric value from ParentOperation string
    # -------------------------------------------------------------
    def extract_bom_qty(self, parent_operation):
        text = str(parent_operation or "")
        print(f"[EXTRACT_BOM] Input text: '{text}'", flush=True)
        match = re.search(r"BOMQty:\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
        if not match:
            print(f"⚠️ Could not extract BOMQty from: '{text}', defaulting to 1", flush=True)
            return Decimal("1")
        try:
            bom_qty = Decimal(match.group(1))
            print(f"✅ Extracted BOMQty: {bom_qty}", flush=True)
            return bom_qty
        except Exception as e:
            print(f"⚠️ Error extracting BOMQty: {e}, using default 1", flush=True)
            return Decimal("1")

    # -------------------------------------------------------------
    # Compute effective qty (depends on operation type)
    # -------------------------------------------------------------
    def compute_effective_qty(self, operation, prod_qty, parent_operation):
        print(f"[COMPUTE_QTY] START - operation={operation}, prod_qty={prod_qty}", flush=True)
        
        prod_qty = Decimal(str(prod_qty or 0))
        operation_str = str(operation or "").strip().replace(" ", "").replace("|", "")
        bom_qty = self.extract_bom_qty(parent_operation)

        print(f"DEBUG: operation_str={operation_str}, bom_qty={bom_qty}, prod_qty={prod_qty}", flush=True)

        # ✅ If operation starts with '10' → multiply prod_qty * BOMQty
        if operation_str.startswith("10"):
            effective = (prod_qty * bom_qty).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            print(f"✅ Operation starts with 10 → {prod_qty} × {bom_qty} = {effective}", flush=True)
            return effective

        # Otherwise → just prod_qty
        print(f"⚪ Operation not starting with 10 → Use prod_qty only = {prod_qty}", flush=True)
        return prod_qty

    # -------------------------------------------------------------
    # Update ParentOperation when operation starts with "10"
    # -------------------------------------------------------------
    def update_parent_operation_for_operation_10(self, production, original_parent_operation=None):
        print(f"[UPDATE_PARENT_OP] START - operation={production.operation}", flush=True)
        operation = str(production.operation or "").strip().replace(" ", "").replace("|", "")
        if not operation.startswith("10"):
            print(f"[UPDATE_PARENT_OP] Operation doesn't start with 10, skipping", flush=True)
            return

        prod_qty = Decimal(production.prod_qty or 0)
        parent_op_source = original_parent_operation if original_parent_operation is not None else production.ParentOperation
        original_bom_qty = self.extract_bom_qty(parent_op_source)

        new_bom_qty = (original_bom_qty * prod_qty) - prod_qty
        if new_bom_qty < 0:
            new_bom_qty = Decimal("0")

        new_bom_qty_str = str(new_bom_qty.quantize(Decimal("0.001")))
        production.ParentOperation = f"ScracpQty: N/A | BOMQty: {new_bom_qty_str}"
        production.save(update_fields=["ParentOperation"])

        print(f"📝 Updated ParentOperation for operation 10: BOMQty {original_bom_qty} → {new_bom_qty_str}", flush=True)

    # -------------------------------------------------------------
    # CREATE
    # -------------------------------------------------------------
    def create(self, validated_data):
        print("\n" + "="*80, flush=True)
        print("🚀 OOPurchaseSerializer.create() CALLED", flush=True)
        print("="*80 + "\n", flush=True)
        
        # Extract nested data
        MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
        
        # Store original ParentOperation before creating the object
        original_parent_operation = validated_data.get('ParentOperation', None)
        
        # Create production entry
        production_entry = ProductionEntry.objects.create(**validated_data)
       
        self.subtract_from_parent_operation(production_entry)

        print(f"✅ Created ProductionEntry: ID={production_entry.id}", flush=True)
        
        # Create related MachineIdleTime entries
        for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
            MachineIdleTime_Detail = MachineIdleTime.objects.create(**MachineIdleTime_data)
            production_entry.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)
        
        # Update ParentOperation if operation starts with "10"
        self.update_parent_operation_for_operation_10(production_entry, original_parent_operation=original_parent_operation)

        # Extract heat number
        lot_no_value = (production_entry.lot_no or "").strip()
        heat_no = lot_no_value.split("|")[0].strip() if "|" in lot_no_value else lot_no_value
        print(f"🔍 Extracted HeatNo: {heat_no}", flush=True)

        # Compute effective quantity based on operation type
        operation = (production_entry.operation or "").strip()
        prod_qty = Decimal(production_entry.prod_qty or 0)

        qty_to_subtract = self.compute_effective_qty(operation, prod_qty, original_parent_operation)
        
        # print(f"📊 Quantity to subtract: {qty_to_subtract}", flush=True)

        # if qty_to_subtract <= 0:
        #     print(f"⚠️ qty_to_subtract <= 0, skipping FIFO subtraction", flush=True)
        #     return production_entry
        
        # Subtract only when operation starts with 10
        operation_clean = str(operation).replace(" ", "").split("|")[0]

        if not operation_clean.startswith("10"):
            print("⏭️ Skipping FIFO subtraction — operation is not starting with 10", flush=True)
            return production_entry

        if qty_to_subtract <= 0:
            print(f"⚠️ qty_to_subtract <= 0, skipping FIFO subtraction", flush=True)
            return production_entry

# FIFO subtraction logic continues...

        

         



        # FIFO subtraction from MaterialChallanTable
        print(f"🔄 Starting FIFO subtraction for HeatNo: {heat_no}", flush=True)
        remaining = Decimal(qty_to_subtract)
        for item in MaterialChallanTable.objects.filter(HeatNo__iexact=heat_no).order_by('id'):
            if remaining <= 0:
                break
            current_qty = Decimal(item.Qty or 0)
            if current_qty <= 0:
                continue
            to_subtract = min(current_qty, remaining)
            item.Qty = str(current_qty - to_subtract)
            item.save(update_fields=["Qty"])
            print(f"✓ ChallanTable {item.id} FIFO subtract: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={heat_no})", flush=True)
            remaining -= to_subtract

        print(f"✅ OOPurchaseSerializer.create() COMPLETED\n", flush=True)
        


        return production_entry

    # -------------------------------------------------------------
    # UPDATE
    # -------------------------------------------------------------
    def update(self, instance, validated_data):
        print("\n" + "="*80, flush=True)
        print("🔄 OOPurchaseSerializer.update() CALLED", flush=True)
        print("="*80 + "\n", flush=True)
        
        # Extract nested data
        MachineIdleTime_Detail_Enter_data = validated_data.pop('MachineIdleTime_Detail_Enter', [])
        
        # Store old values for restoration
        old_lot_no_value = (instance.lot_no or "").strip()
        old_heat_no = old_lot_no_value.split("|")[0].strip() if "|" in old_lot_no_value else old_lot_no_value
        old_qty_effective = self.compute_effective_qty(instance.operation, instance.prod_qty, instance.ParentOperation)
        
        # Store original ParentOperation
        original_parent_operation = validated_data.get('ParentOperation', instance.ParentOperation)

        # Apply updates
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        print(f"✅ Updated ProductionEntry: ID={instance.id}", flush=True)

        # Update nested MachineIdleTime entries
        instance.MachineIdleTime_Detail_Enter.clear()
        for MachineIdleTime_data in MachineIdleTime_Detail_Enter_data:
            MachineIdleTime_Detail = MachineIdleTime.objects.create(**MachineIdleTime_data)
            instance.MachineIdleTime_Detail_Enter.add(MachineIdleTime_Detail)

        # Update ParentOperation if operation starts with "10"
        self.update_parent_operation_for_operation_10(instance, original_parent_operation=original_parent_operation)

        # ♻️ Restore old quantity to MaterialChallanTable
        if old_qty_effective > 0:
            old_item = MaterialChallanTable.objects.filter(HeatNo__iexact=old_heat_no).order_by('id').first()
            if old_item:
                restored_val = Decimal(old_item.Qty or 0) + old_qty_effective
                old_item.Qty = str(restored_val)
                old_item.save(update_fields=["Qty"])
                print(f"♻️ Restored ChallanTable {old_item.id}: +{old_qty_effective} (HeatNo={old_heat_no})", flush=True)

        # Subtract new quantity
        new_lot_no_value = (instance.lot_no or "").strip()
        new_heat_no = new_lot_no_value.split("|")[0].strip() if "|" in new_lot_no_value else new_lot_no_value
        new_operation = validated_data.get('operation', instance.operation)
        new_prod_qty = Decimal(validated_data.get('prod_qty', instance.prod_qty) or 0)

        new_qty_effective = self.compute_effective_qty(new_operation, new_prod_qty, original_parent_operation)
        print(f"📊 New quantity to subtract: {new_qty_effective}", flush=True)

        # if new_qty_effective <= 0:
        #     print(f"⚠️ new_qty_effective <= 0, skipping FIFO subtraction", flush=True)
        #     return instance
        

        operation_clean = str(new_operation).replace(" ", "").split("|")[0]

        if not operation_clean.startswith("10"):
            print("⏭️ Skipping FIFO subtraction — operation is not starting with 10", flush=True)
            return instance

        if new_qty_effective <= 0:
            print(f"⚠️ new_qty_effective <= 0, skipping FIFO subtraction", flush=True)
            return instance

        # FIFO subtraction continues...

        




        # FIFO subtraction
        print(f"🔄 Starting FIFO subtraction for HeatNo: {new_heat_no}", flush=True)
        remaining_new = Decimal(new_qty_effective)
        for item in MaterialChallanTable.objects.filter(HeatNo__iexact=new_heat_no).order_by('id'):
            if remaining_new <= 0:
                break
            current_qty = Decimal(item.Qty or 0)
            if current_qty <= 0:
                continue
            to_subtract = min(current_qty, remaining_new)
            item.Qty = str(current_qty - to_subtract)
            item.save(update_fields=["Qty"])
            print(f"✓ Updated ChallanTable {item.id} FIFO: {current_qty} → {item.Qty} (−{to_subtract}, HeatNo={new_heat_no})", flush=True)
            remaining_new -= to_subtract

        print(f"✅ OOPurchaseSerializer.update() COMPLETED\n", flush=True)
        return instance

