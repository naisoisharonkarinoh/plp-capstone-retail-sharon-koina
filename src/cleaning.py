import pandas as pd


def clean_transactions(raw_data):
    """
    Clean supermarket transaction data.

    Returns:
        clean_data: The cleaned DataFrame.
        cleaning_log: A list describing the cleaning actions.
    """

    # Keep the original data unchanged
    clean_data = raw_data.copy()

    cleaning_log = []

    # Record the original number of rows
    original_rows = len(clean_data)

    cleaning_log.append({
        "action": "Initial row count",
        "rows_before": original_rows,
        "rows_after": original_rows,
        "rows_removed": 0
    })

    # 1. Remove duplicate transactions
    before = len(clean_data)

    clean_data = clean_data.drop_duplicates(
        subset=["transaction_id"]
    )

    cleaning_log.append({
        "action": "Remove duplicate transaction IDs",
        "rows_before": before,
        "rows_after": len(clean_data),
        "rows_removed": before - len(clean_data)
    })

    # 2. Convert dates to datetime
    clean_data["date"] = pd.to_datetime(
        clean_data["date"],
        errors="coerce"
    )

    # 3. Remove rows with missing essential fields
    before = len(clean_data)

    essential_columns = [
        "transaction_id",
        "date",
        "customer_id",
        "product_id",
        "branch_id",
        "quantity",
        "unit_price"
    ]

    clean_data = clean_data.dropna(
        subset=essential_columns
    )

    cleaning_log.append({
        "action": "Remove missing essential values",
        "rows_before": before,
        "rows_after": len(clean_data),
        "rows_removed": before - len(clean_data)
    })

    # 4. Remove invalid quantities and prices
    before = len(clean_data)

    clean_data = clean_data[
        (clean_data["quantity"] > 0) &
        (clean_data["unit_price"] > 0)
    ].copy()

    cleaning_log.append({
        "action": "Remove invalid quantities or prices",
        "rows_before": before,
        "rows_after": len(clean_data),
        "rows_removed": before - len(clean_data)
    })

    # 5. Recalculate sales amounts
    clean_data["sales_amount"] = (
        clean_data["quantity"] * clean_data["unit_price"]
    )

    cleaning_log.append({
        "action": "Recalculate sales amount",
        "rows_before": len(clean_data),
        "rows_after": len(clean_data),
        "rows_removed": 0
    })

    # 6. Reset row numbering
    clean_data = clean_data.reset_index(drop=True)

    return clean_data, cleaning_log
