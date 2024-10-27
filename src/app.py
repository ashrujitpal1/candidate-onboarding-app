import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import PGVector
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database configuration
CONNECTION_STRING = os.getenv('PG_CONNECTION_STRING')
COLLECTION_NAME = "documents"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the PDF
        loader = PyPDFLoader(filepath)
        documents = loader.load()

        # Split the document into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        # Create embeddings using all-MiniLM-L6-v2
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Store in pgvector
        db = PGVector.from_documents(
            documents=texts,
            embedding=embeddings,
            connection_string=CONNECTION_STRING,
            collection_name=COLLECTION_NAME
        )

        # Clean up the uploaded file
        os.remove(filepath)

        return jsonify({"message": "Document processed and stored successfully"}), 200

    return jsonify({"error": "Invalid file type"}), 400


@app.route('/')
def hello_world():
    return 'Hello, Docker!'


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=8080)
