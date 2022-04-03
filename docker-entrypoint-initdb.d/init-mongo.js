db = db.getSiblingDB('mydb');
db.createUser(
    {
        user  : "admin",
        pwd   : "admin",
        roles : [
            {
                role : "readWrite",
                db   : "mydb"
            }
        ]
    }
)
db.createCollection('my_collection');
