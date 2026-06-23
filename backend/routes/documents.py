import uuid
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import require_auth
from services.s3_service import upload_file, generate_download_url, delete_file
from services.dynamodb_service import save_document_metadata, list_documents, get_document, delete_document

documents_bp = Blueprint('documents', __name__)


@documents_bp.route('/documents', methods=['GET'])
@require_auth
def get_documents():
    docs = list_documents()
    return jsonify(docs)


@documents_bp.route('/documents/upload', methods=['POST'])
@require_auth
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'Không có file được gửi lên'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Tên file không hợp lệ'}), 400

    doc_id = str(uuid.uuid4())
    filename = f"{doc_id}_{file.filename}"

    upload_file(file, filename)
    save_document_metadata(
        doc_id=doc_id,
        filename=filename,
        uploader=request.current_user,
        size=request.content_length or 0
    )

    return jsonify({'message': 'Upload thành công', 'document_id': doc_id}), 201


@documents_bp.route('/documents/download/<doc_id>', methods=['GET'])
@require_auth
def download_document(doc_id):
    doc = get_document(doc_id)
    if not doc:
        return jsonify({'error': 'Tài liệu không tồn tại'}), 404

    url = generate_download_url(doc['filename'])
    return jsonify({'download_url': url})


@documents_bp.route('/documents/<doc_id>', methods=['DELETE'])
@require_auth
def remove_document(doc_id):
    doc = get_document(doc_id)
    if not doc:
        return jsonify({'error': 'Tài liệu không tồn tại'}), 404

    delete_file(doc['filename'])
    delete_document(doc_id)
    return jsonify({'message': 'Xóa thành công'})
