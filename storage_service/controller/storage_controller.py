from __future__ import annotations

from storage_service.depends.depend_queue import dependency_queue
from storage_service.depends.depend_s3_service import (
    dependency_storage_service,
)
from storage_service.model.storage.new_file_request import NewFileURLRequest
from storage_service.model.storage.process_file_request import (
    ProcessFileRequest,
)
from storage_service.model.storage.signed_url_response import SignedUrlResponse
from storage_service.service.storage.storage_service import StorageService
from storage_service.utils.exceptions.file_not_found_exception import (
    FileNotFoundException,
)
from storage_service.utils.file.file_hash_generator import generate_file_hash
from storage_service.worker.storage_file_worker import storage_file_worker

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from rq import Queue

router = APIRouter(tags=["storage"])


@cbv(router)
class StorageController:
    queue: Queue = Depends(dependency_queue, use_cache=True)
    storage_service: StorageService = Depends(
        dependency_storage_service, use_cache=True
    )

    @router.post("/file", status_code=200)
    def new_file_url(self, new_file_request: NewFileURLRequest) -> SignedUrlResponse:
        hashed_file_name = generate_file_hash(
            new_file_request.file_key, new_file_request.file_postfix
        )

        return self.storage_service.get_temp_upload_link(
            hashed_file_name, new_file_request.file_type
        )

    @router.get("/file", status_code=200)
    def file_url(self, file_key: str, file_postfix: str) -> SignedUrlResponse:
        try:
            return self.storage_service.get_temp_read_link(
                generate_file_hash(file_key, file_postfix)
            )
        except Exception as _:
            raise FileNotFoundException("File not found")

    @router.delete("/file", status_code=204)
    def delete_file(self, file_key: str, file_postfix: str):
        return self.storage_service.delete_file(
            generate_file_hash(file_key, file_postfix)
        )

    @router.post("/file/process", status_code=200)
    def process_file(self, process_file_request: ProcessFileRequest):
        self.queue.enqueue(
            storage_file_worker,
            process_file_request.file_key,
            process_file_request.file_postfix,
        )
