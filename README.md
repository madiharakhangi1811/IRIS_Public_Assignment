# FastAPI Excel Processor Assignment

n task is to develop a FastAPI application with the following functionalities:

### 1. Excel Sheet Processing
The application must be able to read a provided Excel sheet and parse its contents (`/Data/capbudg.xls`).

### 2. API Endpoints
You need to implement the following FastAPI endpoints. Please use `http://localhost:9090` as the base URL for your endpoints.

#### a. `GET /list_tables`
   - **Functionality:** This endpoint should list all the table names present in the uploaded/specified Excel sheet.
   - **Response Example:**
     ```json
     {
       "tables": ["Initial Investment", "Revenue Projections", "Operating Expenses"]
     }
     ```

#### b. `GET /get_table_details`
   - **Parameters:**
     - `table_name: str` (Query parameter specifying the name of the table)
   - **Functionality:** This endpoint should return the names of the rows for the selected table. These row names are typically the values found in the first column of that table.
   - **Example:** If the user selects the "Initial Investment" table, the API should list the first column values like so:
     ```json
     {
       "table_name": "Initial Investment",
       "row_names": [
         "Initial Investment=",
         "Opportunity cost (if any)=",
         "Lifetime of the investment",
         "Salvage Value at end of project=",
         "Deprec. method(1:St.line;2:DDB)=",
         "Tax Credit (if any )=",
         "Other invest.(non-depreciable)="
       ]
     }
     ```

#### c. `GET /row_sum`
   - **Parameters:**
     - `table_name: str` (Query parameter specifying the name of the table)
     - `row_name: str` (Query parameter specifying the name of the row, which must be one of the names returned by `/get_table_details`)
   - **Functionality:** This endpoint should calculate and return the sum of all numerical data points in the specified row of the specified table.
   - **Example:** If the `row_name` is `"Tax Credit (if any )="` for a table where this row contains the value `10` (or `10%`), the output should be:
     ```json
     {
       "table_name": "Initial Investment",
       "row_name": "Tax Credit (if any )=",
       "sum": 10 
     }
     ```
     *(Note: You can decide whether to include units like '%' in the response or just return the numerical sum. Please clarify your approach in your documentation.)*


## Testing

To help us quickly test your application, please provide a Postman collection JSON.

*   **Base URL:** `http://localhost:9090` and the given endpoint names.
*   **Postman Collection:** 

## Potential Improvements

1.Allow file uploads through the API (/upload-excel) to make it dynamic.

## Missed Edge Cases

1. Sheets with no recognizable tables will be silently ignored.
2. Rows with mixed text and numbers may partially fail to sum correctly.
3. Table headers that do not meet the "uppercase with spaces" rule will be skipped.
4. File not found or malformed Excel file errors are caught but not deeply diagnosed.
5. Row names must match exactly — no fuzzy matching or suggestions are implemented.