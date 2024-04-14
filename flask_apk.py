from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to create a database and table if they don't exist
def create_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        company_name TEXT,
                        branch TEXT)''')
    conn.commit()
    conn.close()

create_table()

# Insert API endpoint to insert single or multiple entries
@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.json
    if isinstance(data, list):
        for entry in data:
            insert_entry(entry)
    else:
        insert_entry(data)
    return jsonify({"message": "Data inserted successfully"})

# Function to insert a single entry into the database
def insert_entry(entry):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (first_name, last_name, company_name, branch) 
                      VALUES (?, ?, ?, ?)''', (entry['first_name'], entry['last_name'], entry['company_name'], entry['branch']))
    conn.commit()
    conn.close()


# Delete API endpoint to delete a record with given ID
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_data(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM users WHERE id = ?''', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Record with ID {id} deleted successfully"})


@app.route('/update/<int:id>', methods=['PUT'])
def update_data(id):
    data = request.json

    # Validate that required field ("first_name") is present
    if 'first_name' not in data:
        return jsonify({"message": "Missing required field: first_name"}), 400  # Bad request

    # Connect to the database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Update the specific record using the provided ID
    cursor.execute('''UPDATE users SET first_name = ?, last_name = ?, company_name = ?, branch = ? WHERE id = ?''', (data['first_name'], data['last_name'], data['company_name'], data['branch'], id))
    conn.commit()
    conn.close()

    # Check if any rows were affected (updated)
    if cursor.rowcount == 0:
        return jsonify({"message": "Record not found or not updated"}), 404  # Not found

    return jsonify({"message": f"Record with ID {id} updated successfully"})



# Get a specific record by ID API endpoint
@app.route('/get/<int:id>', methods=['GET'])
def get_record_by_id(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE id = ?''', (id,))
    record = cursor.fetchone()
    conn.close()

    if record:
        data = {
            'id': record[0],
            'first_name': record[1],
            'last_name': record[2],
            'company_name': record[3],
            'branch': record[4]
        }
        return jsonify({"data": data})
    else:
        return jsonify({"error": f"Record with ID {id} not found."}), 404




# Get all records API endpoint
@app.route('/get-all', methods=['GET'])
def get_all_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users''')
    records = cursor.fetchall()
    conn.close()

    data = []
    for record in records:
        data.append({
            'id': record[0],
            'first_name': record[1],
            'last_name': record[2],
            'company_name': record[3],
            'branch': record[4]
        })

    return jsonify({"data": data})


if __name__ == '__main__':
    app.run(debug=True)






























# Delete API endpoint to delete a record with ID 3
# @app.route('/delete', methods=['DELETE'])
# def delete_data():
#     conn = sqlite3.connect('data.db')
#     cursor = conn.cursor()
#     cursor.execute('''DELETE FROM users WHERE id = ?''', (2,))
#     conn.commit()
#     conn.close()
#     return jsonify({"message": "Record with ID 3 deleted successfully"})

# Update API endpoint to update a column of the record with ID 1
# @app.route('/update', methods=['PUT'])
# def update_data():
#     data = request.json
#     conn = sqlite3.connect('data.db')
#     cursor = conn.cursor()
#     cursor.execute('''UPDATE users SET first_name = ? WHERE id = ?''', (data['first_name'], 1))
#     conn.commit()
#     conn.close()
#     return jsonify({"message": "Record with ID 1 updated successfully"})