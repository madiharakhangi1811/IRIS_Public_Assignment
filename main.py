from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

# ---------- Excel Parser Functions ----------

def read_excel_tables(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")

    df = pd.read_excel(file_path, None)  # Read all sheets
    tables = {}

    for sheet_name, sheet in df.items():
        rows, cols = sheet.shape
        table_name = None
        current_table = {}

        for i in range(rows):
            row = sheet.iloc[i].fillna("").astype(str)
            for j in range(cols):
                cell = row.iloc[j].strip()
                if cell.isupper() and len(cell) > 2 and " " in cell:
                    if table_name and current_table:
                        tables[table_name] = current_table
                        current_table = {}
                    table_name = cell
                elif table_name and row.iloc[0]:
                    key = row.iloc[0].strip()
                    values = pd.to_numeric(row.iloc[1:], errors="coerce").dropna().tolist()
                    current_table[key] = values

        if table_name and current_table:
            tables[table_name] = current_table
    return tables

def list_all_tables(parsed_data: dict) -> list:
    return list(parsed_data.keys())

def get_row_names(parsed_data: dict, table_name: str) -> list:
    table = parsed_data.get(table_name)
    if not table:
        raise ValueError(f"Table '{table_name}' not found.")
    return list(table.keys())

def get_row_sum(parsed_data: dict, table_name: str, row_name: str) -> float:
    table = parsed_data.get(table_name)
    if not table:
        raise ValueError(f"Table '{table_name}' not found.")
    row = table.get(row_name)
    if row is None:
        raise ValueError(f"Row '{row_name}' not found in table '{table_name}'.")
    return sum(row)

# ---------- File Path and Data Parsing ----------

FILE_PATH = "Data/capbudg.xls"
parsed_data = read_excel_tables(FILE_PATH)

# ---------- API Setup ----------

app = FastAPI(
    title="Excel Sheet Processor",
    description="API to parse Excel tables and calculate row sums.",
    version="1.0"
)

# Enable CORS if testing from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.get("/list_tables")
def list_tables():
    try:
        tables = list_all_tables(parsed_data)
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_table_details")
def get_table_details(table_name: str = Query(...)):
    try:
        rows = get_row_names(parsed_data, table_name)
        return {"table_name": table_name, "row_names": rows}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/row_sum")
def row_sum(table_name: str = Query(...), row_name: str = Query(...)):
    try:
        total = get_row_sum(parsed_data, table_name, row_name)
        return {"table": table_name, "row": row_name, "sum": total}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router)
