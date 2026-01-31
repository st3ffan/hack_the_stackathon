import os
import ssl
from pymongo import MongoClient

# Load configuration from environment variables
CLUSTER = os.getenv("DEMO_CLUSTER", "mongodb+srv://cluster0.wjfjfe.mongodb.net")
DB = os.getenv("DEMO_DB", "hts")
CERT = os.getenv("DEMO_CERT", "X509-cert.pem")


class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            cert_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                f"{CERT}",
            )

            connection_string = f"{CLUSTER}/{DB}?authSource=%24external&authMechanism=MONGODB-X509"
            print(connection_string)
            self.client = MongoClient(
                connection_string,
                tls=True,
                tlsCertificateKeyFile=cert_path,
                tlsAllowInvalidCertificates=False,
                tlsAllowInvalidHostnames=False,
            )

            self.client.admin.command("ping")

            self.db = self.client["hts"]
            self.collection = self.db["corporations"]

            print("Successfully connected to MongoDB Atlas")
            return True

        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return False

    def get_corporations(self):
        if self.collection is None:
            return []
        try:
            corporations = list(self.collection.find({}).sort({"rank":1}))
            return corporations
        except Exception as e:
            print(f"Error fetching corporations: {e}")
            return []

    def close(self):
        if self.client:
            self.client.close()


db = Database()
