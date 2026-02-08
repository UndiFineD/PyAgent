# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentkit.py\backend.py\app.py\tests.py\fake.py\pdf_pipeline_0d7d9cd0059e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\tests\fake\pdf_pipeline.py

# -*- coding: utf-8 -*-

from app.db.vector_db_pdf_ingestion import PDFExtractionPipeline

from langchain.vectorstores import VectorStore


class FakePDFExtractionPipeline(PDFExtractionPipeline):
    def __init__(self, vector_db: VectorStore):
        self.vector_db = vector_db

    def run(self, **kwargs):
        return self.vector_db
