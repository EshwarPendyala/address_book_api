# address_book_api

Address Book APP

The following python libraries are required in order to run the app:
fastapi==0.95.0
geopy==2.3.0
SQLAlchemy==2.0.7
uvicorn==0.21.1

The above libraries are a part of requirements.txt

Run the following command after installing the required libraries:
python3 -m uvicorn address_book_app.main:app --reload

Note: Navigate to the one level above the source directory, i.e. address_book_api.

Swagger docs: http://127.0.0.1:8000/docs

The user can perform the following operations:
1. Create a contact (With name and mobile number).
2. Create an address(with logitude and latitude) for a given contact (With the contact_id).
3. Update/Delete contacts (using contact_id).
4. Get the list of contacts for a given contact name and distance.
