import voyageai
from voyageai.video_utils import Video
import PIL 
import os
from pymongo import MongoClient
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

vo = voyageai.Client()

# MongoDB connection setup
DEMO_DB = os.environ.get("DEMO_DB")
DEMO_CERT = os.environ.get("DEMO_CERT")
DEMO_CLUSTER = os.environ.get("DEMO_CLUSTER")

if not all([DEMO_DB, DEMO_CERT, DEMO_CLUSTER]):
    raise ValueError("Missing one or more MongoDB environment variables: DEMO_DB, DEMO_CERT, DEMO_CLUSTER")

# Build certificate path
if os.path.isabs(DEMO_CERT):
    cert_path = DEMO_CERT
elif os.path.exists(DEMO_CERT):
    cert_path = os.path.abspath(DEMO_CERT)
else:
    cert_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        DEMO_CERT,
    )

# Verify certificate exists
if not os.path.exists(cert_path):
    raise FileNotFoundError(f"Certificate file not found at: {cert_path}")

print(f"Using certificate at: {cert_path}")

# Fix the connection string to ensure proper authSource for X.509
def fix_connection_string_for_x509(uri):
    """
    Ensures the connection string has authSource=$external and authMechanism=MONGODB-X509
    """
    parsed = urlparse(uri)
    
    # Parse existing query parameters
    if parsed.query:
        params = parse_qs(parsed.query, keep_blank_values=True)
    else:
        params = {}
    
    # Force authSource to $external for X.509
    params['authSource'] = ['$external']
    params['authMechanism'] = ['MONGODB-X509']
    
    # Rebuild query string
    # Convert back to single values (parse_qs returns lists)
    params_single = {k: v[0] if isinstance(v, list) else v for k, v in params.items()}
    new_query = urlencode(params_single)
    
    # Rebuild the URL
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)

# Fix the connection string
fixed_uri = fix_connection_string_for_x509(DEMO_CLUSTER)
print(f"Fixed connection string: {fixed_uri.replace(fixed_uri.split('@')[0].split('//')[1], '***') if '@' in fixed_uri else fixed_uri}")

# Connect to MongoDB with X.509 authentication
try:
    client = MongoClient(
        fixed_uri,
        tls=True,
        tlsCertificateKeyFile=cert_path,
        tlsAllowInvalidCertificates=False,
        connectTimeoutMS=60000,
        serverSelectionTimeoutMS=60000
    )
    
    # Test the connection
    client.admin.command('ping')
    print("✓ Successfully connected to MongoDB")
    
    # Check authentication status
    try:
        auth_info = client.admin.command('connectionStatus')
        print(f"✓ Authenticated as: {auth_info.get('authInfo', {}).get('authenticatedUsers', [])}")
    except:
        pass
    
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

db = client[DEMO_DB]
collection = db['image_embeddings']

# Generate inputs array
inputs = []
for i in range(1, 2):  # Iterates from 1 to 1 (just file 1.jpg)
    filename = f"{i}.jpg"
    try:
        image = PIL.Image.open(filename)
        inputs.append([image])
        print(f"✓ Loaded {filename}")
    except FileNotFoundError:
        print(f"⚠ Warning: File {filename} not found. Skipping.")

# Vectorize inputs
embeddings_list = []
if inputs:
    images_to_embed = [item for item in inputs]
    print("Creating embeddings...")
    result = vo.multimodal_embed(images_to_embed, model="voyage-multimodal-3.5")
    
    # Associate embeddings with their original names and filenames
    for i, embedding in enumerate(result.embeddings):
        embeddings_list.append({
            "name": f"{i+1}.jpg",
            "filename": f"{i+1}.jpg",
            "vector": embedding
        })
    print(f"✓ Generated {len(embeddings_list)} embeddings")

# Upload embeddings to MongoDB
if embeddings_list:
    try:
        result = collection.insert_many(embeddings_list)
        print(f"✓ Successfully uploaded {len(result.inserted_ids)} embeddings to collection '{collection.name}'")
    except Exception as e:
        print(f"✗ Error uploading embeddings to MongoDB: {e}")
        raise
else:
    print("⚠ No embeddings to upload.")

client.close()
print("✓ Connection closed")
