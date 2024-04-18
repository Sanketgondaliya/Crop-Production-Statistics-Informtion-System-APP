def fetch_data(query):
    # Database credentials
    host = 'localhost'
    port = '5432'
    database = 'crop_data'
    user = 'postgres'
    password = 's@nket2002'

    # Establish a connection
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )    
    with conn.cursor() as cursor:
        cursor.execute(query)
        col_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
    return pd.DataFrame(data, columns=col_names)