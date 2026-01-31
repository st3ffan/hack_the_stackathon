import voyageai
from voyageai.video_utils import Video
import PIL 
import os
from pymongo import MongoClient

vo = voyageai.Client()
# This will automatically use the environment variable VOYAGE_API_KEY.

# MongoDB connection setup
DEMO_DB = os.environ.get("DEMO_DB")
DEMO_CERT = os.environ.get("DEMO_CERT")
DEMO_CLUSTER = os.environ.get("DEMO_CLUSTER")

if not all([DEMO_DB, DEMO_CERT, DEMO_CLUSTER]):
    raise ValueError("Missing one or more MongoDB environment variables: DEMO_DB, DEMO_CERT, DEMO_CLUSTER")

# Build certificate path - adjust this based on where your cert actually is
# Option 1: If DEMO_CERT is an absolute path
if os.path.isabs(DEMO_CERT):
    cert_path = DEMO_CERT
# Option 2: If DEMO_CERT is relative to the current script
elif os.path.exists(DEMO_CERT):
    cert_path = os.path.abspath(DEMO_CERT)
# Option 3: If DEMO_CERT is in parent directory
else:
    cert_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        DEMO_CERT,
    )

# Verify certificate exists
if not os.path.exists(cert_path):
    raise FileNotFoundError(f"Certificate file not found at: {cert_path}")

print(f"Using certificate at: {cert_path}")

# Connect to MongoDB with X.509 authentication
try:
    client = MongoClient(
        DEMO_CLUSTER,
        authMechanism='MONGODB-X509',  # Explicitly set auth mechanism
        authSource='$external',
        tls=True,  # Enable TLS
        tlsCertificateKeyFile=cert_path,
        tlsAllowInvalidCertificates=False,  # Set to False in production
        connectTimeoutMS=60000,
        serverSelectionTimeoutMS=60000
    )
    
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
    
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

db = client[DEMO_DB]  # Use the database from environment variable
collection = db['image_embeddings']

# Generate inputs array
inputs = []
for i in range(1, 6):  # Iterates from 1 to 1 (just file 1.jpg)
    filename = f"{i}.jpg"
    try:
        image = PIL.Image.open(filename)
        inputs.append([image])
        print(f"Loaded {filename}")
    except FileNotFoundError:
        print(f"Warning: File {filename} not found. Skipping.")

# Vectorize inputs
embeddings_list = []
if inputs:
    images_to_embed = [item for item in inputs]
    print("Creating embeddings...")
    result = vo.multimodal_embed(images_to_embed, model="voyage-multimodal-3.5")
    
    # Associate embeddings with their original names and filenames
    for i, embedding in enumerate(result.embeddings):
        embeddings_list.append({
            "name": f"{i+1}.jpg",  # Fixed: should be i+1 to match filename
            "filename": f"{i+1}.jpg",  # Fixed: use actual filename
            "vector": embedding
        })
    print(f"Generated {len(embeddings_list)} embeddings")

# Upload embeddings to MongoDB
if embeddings_list:
    try:
        result = collection.insert_many(embeddings_list)
        print(f"Successfully uploaded {len(result.inserted_ids)} embeddings to MongoDB collection '{collection.name}'.")
    except Exception as e:
        print(f"Error uploading embeddings to MongoDB: {e}")
        raise
else:
    print("No embeddings to upload.")

client.close()
print("Connection closed")
