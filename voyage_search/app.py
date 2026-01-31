import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import voyageai
import base64

app = Flask(__name__)

# Initialize Voyage AI client
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

if not os.path.exists(cert_path):
    raise FileNotFoundError(f"Certificate file not found at: {cert_path}")

def fix_connection_string_for_x509(uri):
    """Ensures the connection string has authSource=$external and authMechanism=MONGODB-X509"""
    parsed = urlparse(uri)
    
    if parsed.query:
        params = parse_qs(parsed.query, keep_blank_values=True)
    else:
        params = {}
    
    params['authSource'] = ['$external']
    params['authMechanism'] = ['MONGODB-X509']
    
    params_single = {k: v[0] if isinstance(v, list) else v for k, v in params.items()}
    new_query = urlencode(params_single)
    
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)

# Initialize MongoDB connection
fixed_uri = fix_connection_string_for_x509(DEMO_CLUSTER)
client = MongoClient(
    fixed_uri,
    tls=True,
    tlsCertificateKeyFile=cert_path,
    tlsAllowInvalidCertificates=False,
    connectTimeoutMS=60000,
    serverSelectionTimeoutMS=60000
)

db = client[DEMO_DB]
collection = db['image_embeddings']

print("✓ Connected to MongoDB")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query_text = data.get('query', '').strip()
        
        if not query_text:
            return jsonify({'error': 'Query text is required'}), 400
        
        # Generate embedding for the query with input_type='query'
        print(f"Generating embedding for query: '{query_text}'")
        result = vo.multimodal_embed(
            [[query_text]], 
            model="voyage-multimodal-3.5",
            input_type="query"
        )
        
        query_embedding = result.embeddings[0]
        print(f"✓ Generated query embedding (dimension: {len(query_embedding)})")
        
        # Perform vector search
        # Using MongoDB Atlas Vector Search aggregation pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "default",  # You'll need to create this index in Atlas
                    "path": "vector",
                    "queryVector": query_embedding,
                    "numCandidates": 100,
                    "limit": 1
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": 1,
                    "filename": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        results = list(collection.aggregate(pipeline))
        print(f"✓ Found {len(results)} results")
        
        # Read image files and convert to base64 for display
        results_with_images = []
        for result in results:
            filename = result.get('filename', result.get('name'))
            image_path = filename
            
            try:
                # Try to read the image file
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode('utf-8')
                        result['image_data'] = f"data:image/jpeg;base64,{img_data}"
                else:
                    result['image_data'] = None
                    print(f"⚠ Image file not found: {image_path}")
            except Exception as e:
                print(f"⚠ Error reading image {filename}: {e}")
                result['image_data'] = None
            
            results_with_images.append(result)
        
        return jsonify({
            'success': True,
            'query': query_text,
            'results': results_with_images,
            'count': len(results_with_images)
        })
        
    except Exception as e:
        print(f"✗ Error during search: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        return jsonify({'status': 'healthy', 'mongodb': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
