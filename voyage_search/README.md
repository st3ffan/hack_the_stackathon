# Visual Search - Multimodal Image Search with Voyage AI

A Flask web application for semantic image search using Voyage AI's multimodal embeddings and MongoDB Atlas Vector Search.

## Features

- 🔍 Semantic text-to-image search using natural language queries
- 🚀 Powered by Voyage AI multimodal-3.5 embeddings
- 💾 MongoDB Atlas Vector Search for fast similarity matching
- 🎨 Modern, responsive UI with smooth animations
- 🔐 X.509 certificate authentication for MongoDB

## Architecture

1. **Query Processing**: User enters text query → generates embedding with `input_type="query"`
2. **Vector Search**: Query embedding searches against pre-computed image embeddings in MongoDB
3. **Results Display**: Top matching images displayed with similarity scores

## Prerequisites

- Python 3.8+
- MongoDB Atlas cluster with Vector Search enabled
- Voyage AI API key
- X.509 certificate for MongoDB authentication
- Image files (*.jpg) in the application directory

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file or export these environment variables:

```bash
export VOYAGE_API_KEY="your_voyage_api_key"
export DEMO_DB="your_database_name"
export DEMO_CERT="path/to/your/certificate.pem"
export DEMO_CLUSTER="mongodb+srv://your-cluster.mongodb.net/"
```

### 3. Create MongoDB Vector Search Index

In MongoDB Atlas, create a vector search index on the `image_embeddings` collection:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "vector",
      "numDimensions": 1024,
      "similarity": "cosine"
    }
  ]
}
```

**Important**: Name the index `vector_index` (or update the index name in `app.py`)

**Note**: The number of dimensions for voyage-multimodal-3.5 is 1024. Verify this matches your model.

### 4. Generate Image Embeddings

First, place your image files (1.jpg, 2.jpg, etc.) in the application directory, then run:

```bash
python gen_image_embeddings_v2.py
```

This will:
- Read image files from the current directory
- Generate embeddings using Voyage AI
- Store embeddings in MongoDB `image_embeddings` collection

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Enter a Query**: Type a natural language description of what you're looking for
   - Examples: "sunset over water", "people smiling", "modern architecture"

2. **View Results**: The app displays matching images sorted by similarity score

3. **Try Examples**: Click the example chips to quickly try sample queries

## Project Structure

```
.
├── app.py                      # Main Flask application
├── gen_image_embeddings_v2.py  # Script to generate and store image embeddings
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # Styles with bold, modern aesthetic
│   └── js/
│       └── script.js          # Client-side search logic
└── *.jpg                      # Your image files
```

## API Endpoints

### `GET /`
Main search interface

### `POST /search`
Perform vector search

**Request:**
```json
{
  "query": "sunset over water"
}
```

**Response:**
```json
{
  "success": true,
  "query": "sunset over water",
  "count": 5,
  "results": [
    {
      "filename": "1.jpg",
      "name": "1.jpg",
      "score": 0.8542,
      "image_data": "data:image/jpeg;base64,..."
    }
  ]
}
```

### `GET /health`
Health check endpoint

## Troubleshooting

### MongoDB Authentication Errors

If you see "Command insert requires authentication":

1. Verify your connection string includes `authSource=$external&authMechanism=MONGODB-X509`
2. Check that your certificate file exists and is readable
3. Ensure the certificate CN matches a user in MongoDB
4. Verify the MongoDB user has proper roles (e.g., `readWrite` on your database)

### Vector Search Returns No Results

1. Verify the vector search index is created and active in MongoDB Atlas
2. Check that embeddings were successfully uploaded to the collection
3. Ensure the index name matches what's used in the aggregation pipeline
4. Verify the embedding dimensions (1024 for voyage-multimodal-3.5)

### Images Not Displaying

1. Ensure image files exist in the application directory
2. Check that filenames in the database match actual files
3. Verify file permissions allow the Flask app to read images

## Performance Optimization

- **Caching**: Consider caching query embeddings for repeated searches
- **Batch Processing**: Generate embeddings in batches for large image collections
- **Index Tuning**: Adjust `numCandidates` in vector search for speed/accuracy tradeoff
- **Image Optimization**: Compress images to reduce bandwidth

## Security Notes

- Never commit certificates or API keys to version control
- Use environment variables for all sensitive configuration
- Set `tlsAllowInvalidCertificates=False` in production
- Implement rate limiting for the search endpoint in production
- Add authentication if deploying publicly

## License

MIT

## Credits

- **Voyage AI** for multimodal embeddings
- **MongoDB Atlas** for vector search capabilities
- Built with Flask, Python, and modern web technologies
