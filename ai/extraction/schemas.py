from typing import Optional, Any

from pydantic import BaseModel, Field


class ExtractedField(BaseModel):
    value: Optional[Any] = None
    source: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ApplicationData(BaseModel):
    name: ExtractedField = Field(default_factory=ExtractedField)
    application_id: ExtractedField = Field(default_factory=ExtractedField)
    date: ExtractedField = Field(default_factory=ExtractedField)
    income: ExtractedField = Field(default_factory=ExtractedField)
    category: ExtractedField = Field(default_factory=ExtractedField)


class CertificateData(BaseModel):
    name: ExtractedField = Field(default_factory=ExtractedField)
    certificate_number: ExtractedField = Field(default_factory=ExtractedField)
    issue_date: ExtractedField = Field(default_factory=ExtractedField)
    category: ExtractedField = Field(default_factory=ExtractedField)
    income: ExtractedField = Field(default_factory=ExtractedField)


class IdentityDocumentData(BaseModel):
    name: ExtractedField = Field(default_factory=ExtractedField)
    id_number: ExtractedField = Field(default_factory=ExtractedField)
    date_of_birth: ExtractedField = Field(default_factory=ExtractedField)
    address: ExtractedField = Field(default_factory=ExtractedField)


class InvoiceData(BaseModel):
    invoice_number: ExtractedField = Field(default_factory=ExtractedField)
    vendor: ExtractedField = Field(default_factory=ExtractedField)
    invoice_date: ExtractedField = Field(default_factory=ExtractedField)
    total_amount: ExtractedField = Field(default_factory=ExtractedField)


SCHEMA_MAP = {
    "application": ApplicationData,
    "certificate": CertificateData,
    "identity_document": IdentityDocumentData,
    "invoice": InvoiceData,
}
