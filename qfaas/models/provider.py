from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class ProviderSchema(BaseModel):
    username: str = Field(...)
    providerName: str = Field(...)
    providerToken: str = Field(...)
    additionalInfo: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "qfaas",
                "providerName": "ibmq",
                "providerToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "additionalInfo": {
                    "hub": ["ibm_quantum_platform", "ibm_quantum-qfaas"],
                    "defaultHub": "ibm_quantum_platform",
                },
            }
        }


class CreateProviderModel(BaseModel):
    providerName: str = Field(...)
    providerToken: str = Field(...)
    additionalInfo: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "providerName": "ibmq",
                "providerToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "additionalInfo": {
                    "defaultHub": "ibm_quantum_platform"
                },
            }
        }


class UpdateProviderModel(BaseModel):
    providerToken: str = Field(...)
    additionalInfo: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "providerToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "additionalInfo": {
                    "defaultHub": "ibm_quantum_platform"
                },
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
