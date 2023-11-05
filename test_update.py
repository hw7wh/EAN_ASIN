def get_existing_eans(output_file_path):
    if os.path.exists(output_file_path):
        df = pd.read_excel(output_file_path)
        return set(df['ean'].astype(str).tolist())
    else:
        return set()

def append_to_excel(df, output_file_path):
    # Append to Excel file if it exists, otherwise create a new one
    if os.path.exists(OUTPUT_FILE_PATH):
        with pd.ExcelWriter(OUTPUT_FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False,
                        startrow=writer.sheets['Sheet1'].max_row)
    else:
        with pd.ExcelWriter(OUTPUT_FILE_PATH, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

if __name__ == '__main__':
    try:
        # Load existing EANs from the output file
        existing_eans = get_existing_eans(OUTPUT_FILE_PATH)

        # Read the input file
        df = pd.read_excel(INPUT_FILE_PATH)
        chunksize = max(1, df.shape[0] // CHUNK_SIZE)
        for i, chunk in enumerate(np.array_split(df, chunksize)):
            print(f'Processing chunk {i}...')
            print(chunk.head())
            impersonate = random.choice(USER_AGENT_LIST)
            chunk_data = process_chunk(chunk, impersonate)

            # Filter out products that are already in the Excel file
            new_chunk_data = [product for product in chunk_data if product['id'] not in existing_eans]
            # Transform data for Excel
            new_excel_data = []
            for product in new_chunk_data:
                # Consolidate stores data into a JSON string
                # stores_data = json.dumps(product.get('stores', []), ensure_ascii=False)
                stores_data = stores_to_string(product.get('stores', []))
                # Create a single row for each product
                product_data = {
                    'ean': product['id'],
                    'name': product.get('name', ''),
                    'asin': product.get('asin', ''),
                    'stores': stores_data  # Store the JSON string in the 'stores' column
                }
                new_excel_data.append(product_data)
            
            # Convert to DataFrame
            new_chunk_df = pd.DataFrame(new_excel_data)
            
            
            # Append new data to Excel file
            if not new_chunk_df.empty:
                append_to_excel(new_chunk_df, OUTPUT_FILE_PATH)
            
            # Update the in-memory set of EANs
            existing_eans.update(product['id'] for product in new_chunk_data)

        excell_formating()
    except Exception as e:
        print("Error:", e)
