from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class IBMQAdditionalInfo(BaseModel):
    """Schema for IBMQ provider additional information"""
    defaultChannel: Optional[str] = Field(default="ibm_cloud", description="Default IBM Quantum channel")
    defaultInstance: Optional[str] = Field(default=None, description="Default IBM Quantum instance (CRN or service name)")
    instances: Optional[List[str]] = Field(default=None, description="List of available instances (auto-populated)")


class BraketAdditionalInfo(BaseModel):
    """Schema for AWS Braket provider additional information"""
    swUser: Optional[str] = Field(default=None, description="Strangeworks user")
    # Add other Braket-specific fields as needed


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
                    "defaultChannel": "ibm_cloud",
                    "defaultInstance": "ibmcloudinstance1",
                    "instances": ["crn:v1:bluemix:public:quantum-computing:us-east:a/...", "hub/group/project"]
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
                    "defaultChannel": "ibm_cloud",
                    "defaultInstance": "ibmcloudinstance1"
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
                    "defaultChannel": "ibm_cloud",
                    "defaultInstance": "ibmcloudinstance1"
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
