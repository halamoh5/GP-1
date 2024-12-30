# import sqlite3
# import os
# from PIL import Image
# import imagehash

# # Constants
# list_of_interest = ['+19193912507', '0791425285', '07996949610', '9198887386', 'hala mohammad']
# wifi_of_interest = ["CcookiesDcastleR5 Guest", "MyHomeNetwork", "OfficeWifi"]

# # Helper Functions
# import sqlite3

# def read_database(db_path, query):
#     # Ensure that db_path is a single string (not a list)
#     if isinstance(db_path, list):
#         db_path = db_path[0]
    
#     if not isinstance(db_path, str):
#         raise ValueError(f"Expected string for db_path, but got {type(db_path)}")
    
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     connection.close()
    
#     return rows

# def compare_contacts(db1, db2):
#     query = "SELECT * FROM phone_lookup;"
#     users_1 = read_database(db1, query)
#     users_2 = read_database(db2, query)

#     if users_1 and users_2:
#         phone_numbers_1 = {user[2] for user in users_1}
#         phone_numbers_2 = {user[2] for user in users_2}
#         common_numbers = list(phone_numbers_1.intersection(phone_numbers_2))
#         interest_matches = list(phone_numbers_1.intersection(list_of_interest))
#         return {"common_numbers": common_numbers, "interest_matches": interest_matches}
#     return {"error": "No data found in one or both databases."}

# def compare_call_logs(db1, db2):
#     query = "SELECT * FROM calls;"
#     logs_1 = read_database(db1, query)
#     logs_2 = read_database(db2, query)

#     if logs_1 and logs_2:
#         phone_numbers_1 = {log[1] for log in logs_1}
#         phone_numbers_2 = {log[1] for log in logs_2}
#         common_numbers = list(phone_numbers_1.intersection(phone_numbers_2))
#         return {"common_call_logs": common_numbers}
#     return {"error": "No call logs found in one or both databases."}

# def compare_wifi(files1, files2):
#     def parse_txt_file(file_path):
#         wifi_info = set()  # Using a set to store unique SSIDs
#         with open(file_path, "r") as file:
#             for line in file:
#                 line = line.strip()
#                 if line.startswith("ssid="):
#                     wifi_info.add(line.split("=", 1)[1].strip())
#         return wifi_info

#     # Aggregate SSIDs from all files for mobile 1 and mobile 2
#     mobile1_networks = set()
#     for file in files1:
#         mobile1_networks.update(parse_txt_file(file))
    
#     mobile2_networks = set()
#     for file in files2:
#         mobile2_networks.update(parse_txt_file(file))

#     # Find common networks
#     common_networks = mobile1_networks.intersection(mobile2_networks)
    
#     # Count total .txt files for both devices
#     total_files_mobile1 = len([file for file in files1 if file.endswith('.txt')])
#     total_files_mobile2 = len([file for file in files2 if file.endswith('.txt')])

#     # Calculate percentage similarity for Wi-Fi
#     similarity_percentage = 0
#     if total_files_mobile1 > 0 and total_files_mobile2 > 0:
#         total_files = total_files_mobile1 + total_files_mobile2
#         similarity_percentage = (len(common_networks) / total_files) * 10

#     return {"common_wifi": list(common_networks), "similarity_percentage_wifi": similarity_percentage}

# def compare_images(files1, files2):
#     def calculate_hashes(files):
#         """Calculate hashes for individual image files."""
#         hashes = {}
#         for file_path in files:
#             if file_path.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
#                 try:
#                     with Image.open(file_path) as img:
#                         relative_path = os.path.basename(file_path)
#                         hashes[relative_path] = imagehash.phash(img)
#                 except Exception as e:
#                     print(f"Error processing {file_path}: {e}")
#         return hashes

#     # Get hashes for all images in both mobile1 and mobile2 lists
#     hashes1 = calculate_hashes(files1)
#     hashes2 = calculate_hashes(files2)

#     # Compare hashes to find similar images
#     similar_images = []
#     for file1, hash1 in hashes1.items():
#         for file2, hash2 in hashes2.items():
#             if hash1 - hash2 <= 5:  # Threshold for similarity
#                 similar_images.append((file1, file2))

#     # Count total .png files for both devices
#     total_files_mobile1 = len([file for file in files1 if file.endswith('.png')])
#     total_files_mobile2 = len([file for file in files2 if file.endswith('.png')])

#     # Calculate percentage similarity for Images
#     similarity_percentage = 0
#     if total_files_mobile1 > 0 and total_files_mobile2 > 0:
#         total_files = max(total_files_mobile1, total_files_mobile2)
#         similarity_percentage = (len(similar_images) / total_files) * 100

#     return {"similar_images": similar_images, "similarity_percentage_images": similarity_percentage}


# def process_files(file_paths):
#     # Group files by category and device
#     grouped_files = {"contacts": {}, "calllogs": {}, "wifi": {}, "images": []}

#     for file in file_paths:
#         # Use the folder structure to identify the device (e.g., "mobile1" or "mobile2")
#         if "mobile1" in file.lower():
#             device = "mobile1"
#         elif "mobile2" in file.lower():
#             device = "mobile2"
#         else:
#             continue  # Skip files that don't match either device

#         name = os.path.basename(file).lower()

#         # Group contacts by device
#         if "contacts" in name:
#             if device not in grouped_files["contacts"]:
#                 grouped_files["contacts"][device] = []
#             grouped_files["contacts"][device].append(file)

#         # Group call logs by device
#         elif "calllog" in name or "dialer" in name:
#             if device not in grouped_files["calllogs"]:
#                 grouped_files["calllogs"][device] = []
#             grouped_files["calllogs"][device].append(file)

#         # Group Wi-Fi configurations by device
#         elif "wpa" in name and file.endswith(".txt"):
#             if device not in grouped_files["wifi"]:
#                 grouped_files["wifi"][device] = []
#             grouped_files["wifi"][device].append(file)

#         # Group images by device
#         elif name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
#             grouped_files["images"].append(file)

#     results = {
#         "contacts": {"common_numbers": [], "interest_matches": []},
#         "calllogs": {"common_call_logs": []},
#         "wifi": {"common_wifi": [], "similarity_percentage_wifi": 0},
#         "images": {"similar_images": [], "similarity_percentage_images": 0},
#     }

#     # Process contacts
#     if "mobile1" in grouped_files["contacts"] and "mobile2" in grouped_files["contacts"]:
#         results["contacts"] = compare_contacts(
#             grouped_files["contacts"]["mobile1"],
#             grouped_files["contacts"]["mobile2"],
#         )

#     # Process call logs
#     if "mobile1" in grouped_files["calllogs"] and "mobile2" in grouped_files["calllogs"]:
#         results["calllogs"] = compare_call_logs(
#             grouped_files["calllogs"]["mobile1"],
#             grouped_files["calllogs"]["mobile2"],
#         )

#     # Process Wi-Fi configurations
#     if "mobile1" in grouped_files["wifi"] and "mobile2" in grouped_files["wifi"]:
#         results["wifi"] = compare_wifi(
#             grouped_files["wifi"]["mobile1"],  # List of files for mobile 1
#             grouped_files["wifi"]["mobile2"],  # List of files for mobile 2
#         )

#     # Process images
#     mobile1_images = [file for file in grouped_files["images"] if "mobile1" in file.lower()]
#     mobile2_images = [file for file in grouped_files["images"] if "mobile2" in file.lower()]
#     if mobile1_images and mobile2_images:
#         results["images"] = compare_images(mobile1_images, mobile2_images)

#     return results



# # def process_files(file_paths):
# #     # Group files by category and device
# #     grouped_files = {"contacts": {}, "calllogs": {}, "wifi": {}, "images": []}

# #     for file in file_paths:
# #         name = os.path.basename(file).lower()

# #         # Group contacts by device
# #         if "contacts" in name:
# #             if "mobile1" in name:
# #                 if "mobile1" not in grouped_files["contacts"]:
# #                     grouped_files["contacts"]["mobile1"] = []
# #                 grouped_files["contacts"]["mobile1"].append(file)
# #             elif "mobile2" in name:
# #                 if "mobile2" not in grouped_files["contacts"]:
# #                     grouped_files["contacts"]["mobile2"] = []
# #                 grouped_files["contacts"]["mobile2"].append(file)

# #         # Group call logs by device
# #         elif "calllog" in name or "dialer" in name:
# #             if "mobile1" in name:
# #                 if "mobile1" not in grouped_files["calllogs"]:
# #                     grouped_files["calllogs"]["mobile1"] = []
# #                 grouped_files["calllogs"]["mobile1"].append(file)
# #             elif "mobile2" in name:
# #                 if "mobile2" not in grouped_files["calllogs"]:
# #                     grouped_files["calllogs"]["mobile2"] = []
# #                 grouped_files["calllogs"]["mobile2"].append(file)

# #         # Group Wi-Fi configurations by device
# #         elif "wpa" in name and file.endswith(".txt"):
# #             if "mobile1" in name:
# #                 if "mobile1" not in grouped_files["wifi"]:
# #                     grouped_files["wifi"]["mobile1"] = []
# #                 grouped_files["wifi"]["mobile1"].append(file)
# #             elif "mobile2" in name:
# #                 if "mobile2" not in grouped_files["wifi"]:
# #                     grouped_files["wifi"]["mobile2"] = []
# #                 grouped_files["wifi"]["mobile2"].append(file)

# #         # Group images directly (no folder grouping, just the files)
# #         elif "picture" in name and file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
# #             if "mobile1" in name:
# #                 grouped_files["images"].append(file)  # Add image file for mobile 1
# #             elif "mobile2" in name:
# #                 grouped_files["images"].append(file)  # Add image file for mobile 2

# #     results = {
# #         "contacts": {"common_numbers": [], "interest_matches": []},
# #         "calllogs": {"common_call_logs": []},
# #         "wifi": {"common_wifi": [], "similarity_percentage_wifi": 0},
# #         "images": {"similar_images": [], "similarity_percentage_images": 0},
# #     }

# #     # Process contacts
# #     if "mobile1" in grouped_files["contacts"] and "mobile2" in grouped_files["contacts"]:
# #         results["contacts"] = compare_contacts(
# #             grouped_files["contacts"]["mobile1"],
# #             grouped_files["contacts"]["mobile2"],
# #         )

# #     # Process call logs
# #     if "mobile1" in grouped_files["calllogs"] and "mobile2" in grouped_files["calllogs"]:
# #         results["calllogs"] = compare_call_logs(
# #             grouped_files["calllogs"]["mobile1"],
# #             grouped_files["calllogs"]["mobile2"],
# #         )

# #     # Process Wi-Fi configurations
# #     if "mobile1" in grouped_files["wifi"] and "mobile2" in grouped_files["wifi"]:
# #         results["wifi"] = compare_wifi(
# #             grouped_files["wifi"]["mobile1"],  # List of files for mobile 1
# #             grouped_files["wifi"]["mobile2"],  # List of files for mobile 2
# #         )

# #     # Process images
# #     if len(grouped_files["images"]) > 0:
# #         mobile1_images = [file for file in grouped_files["images"] if "mobile1" in file]
# #         mobile2_images = [file for file in grouped_files["images"] if "mobile2" in file]
        
# #         results["images"] = compare_images(
# #             mobile1_images,  # List of image files for mobile 1
# #             mobile2_images,  # List of image files for mobile 2
# #         )

# #     return results

import sqlite3
import os
from PIL import Image
import imagehash

# Constants
list_of_interest = ['+19193912507', '0791425285', '07996949610', '9198887386', 'hala mohammad']

def read_database(db_path, query):
    """Reads a database and executes the provided query."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows

def compare_contacts(db1, db2):
    """Compares contacts from two databases."""
    query = "SELECT * FROM phone_lookup;"
    try:
        users_1 = read_database(db1, query)
        users_2 = read_database(db2, query)

        phone_numbers_1 = {user[2] for user in users_1 if len(user) > 2}
        phone_numbers_2 = {user[2] for user in users_2 if len(user) > 2}

        common_numbers = list(phone_numbers_1.intersection(phone_numbers_2))
        interest_matches = list(phone_numbers_1.intersection(list_of_interest))

        return {"common_numbers": common_numbers, "interest_matches": interest_matches}
    except Exception as e:
        return {"error": str(e)}

def compare_call_logs(db1, db2):
    """Compares call logs from two databases."""
    query = "SELECT * FROM calls;"
    try:
        logs_1 = read_database(db1, query)
        logs_2 = read_database(db2, query)

        phone_numbers_1 = {log[1] for log in logs_1 if len(log) > 1}
        phone_numbers_2 = {log[1] for log in logs_2 if len(log) > 1}

        common_numbers = list(phone_numbers_1.intersection(phone_numbers_2))
        return {"common_call_logs": common_numbers}
    except Exception as e:
        return {"error": str(e)}

def compare_wifi(files1, files2):
    """Compares Wi-Fi SSIDs from two lists of files."""
    def parse_txt_file(file_path):
        wifi_info = set()
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("ssid="):
                    wifi_info.add(line.split("=", 1)[1].strip())
        return wifi_info

    try:
        mobile1_networks = set.union(*(parse_txt_file(file) for file in files1 if os.path.exists(file)))
        mobile2_networks = set.union(*(parse_txt_file(file) for file in files2 if os.path.exists(file)))

        common_networks = mobile1_networks.intersection(mobile2_networks)
        total_files = len(files1) + len(files2)
        similarity_percentage = (len(common_networks) / total_files) * 100 if total_files > 0 else 0

        return {"common_wifi": list(common_networks), "similarity_percentage_wifi": similarity_percentage}
    except Exception as e:
        return {"error": str(e)}

def compare_images(files1, files2):
    """Compares images between two lists using perceptual hashing."""
    def calculate_hashes(files):
        hashes = {}
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                with Image.open(file) as img:
                    hashes[file] = imagehash.phash(img)
        return hashes

    try:
        hashes1 = calculate_hashes(files1)
        hashes2 = calculate_hashes(files2)

        similar_images = []
        for file1, hash1 in hashes1.items():
            for file2, hash2 in hashes2.items():
                if hash1 - hash2 <= 5:  # Threshold for similarity
                    similar_images.append((os.path.basename(file1), os.path.basename(file2)))

        total_files = len(files1) + len(files2)
        similarity_percentage = (len(similar_images) / total_files) * 100 if total_files > 0 else 0

        return {"similar_images": similar_images, "similarity_percentage_images": similarity_percentage}
    except Exception as e:
        return {"error": str(e)}

def process_files(file_paths):
    """Processes the files extracted from ZIPs and compares them."""
    grouped_files = {"contacts": {"mobile1": [], "mobile2": []},
                     "calllogs": {"mobile1": [], "mobile2": []},
                     "wifi": {"mobile1": [], "mobile2": []},
                     "images": {"mobile1": [], "mobile2": []}}

    for file in file_paths:
        if "mobile1" in file.lower():
            device = "mobile1"
        elif "mobile2" in file.lower():
            device = "mobile2"
        else:
            continue

        if "contacts" in file.lower():
            grouped_files["contacts"][device].append(file)
        elif "calllog" in file.lower():
            grouped_files["calllogs"][device].append(file)
        elif file.lower().endswith(".txt"):
            grouped_files["wifi"][device].append(file)
        elif file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            grouped_files["images"][device].append(file)

    results = {
        "contacts": compare_contacts(grouped_files["contacts"]["mobile1"], grouped_files["contacts"]["mobile2"]),
        "calllogs": compare_call_logs(grouped_files["calllogs"]["mobile1"], grouped_files["calllogs"]["mobile2"]),
        "wifi": compare_wifi(grouped_files["wifi"]["mobile1"], grouped_files["wifi"]["mobile2"]),
        "images": compare_images(grouped_files["images"]["mobile1"], grouped_files["images"]["mobile2"])
    }
    return results

