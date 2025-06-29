from qiskit_ibm_runtime import QiskitRuntimeService
from qfaas.utils.logger import logger
from qfaas.models.backend import IBMQBackendSchema
from qfaas.database.dbProvider import retrieve_provider
from datetime import datetime
from qfaas.models.backend import BackendRequestSchema
from qfaas.database.dbBackend import get_backends_from_db
import time


def initialize_IBMQProvider(ibmqToken: str, hub: str = "ibm_quantum_platform"):
    """Initialize IBMQ Provider using QiskitRuntimeService

    Args:
        ibmqToken (str): IBMQ API token
        hub (str, optional): channel name. Defaults to "ibm_quantum_platform".

    Returns:
        QiskitRuntimeService instance or None
    """
    try:
        IBMQProvider = QiskitRuntimeService(channel=hub, token=ibmqToken)
        logger.info(f"Initialized QiskitRuntimeService, Used current IBMQ Provider, hub {hub}")
        return IBMQProvider
    except Exception as ex:
        logger.warning(f"Failed to initialize IBMQ service: {ex}")
        return None


def get_IBMQ_hubs(ibmqToken: str):
    """Return list of available channels (hubs) for the IBMQ account

    Args:
        ibmqToken (str): IBMQ Token

    Returns:
        List of available channels or [] if IBMQ Account is not correct
    """
    hubs = []
    try:
        service = QiskitRuntimeService(token=ibmqToken)
        # QiskitRuntimeService does not expose 'hubs', but you can list available backends
        for backend in service.backends():
            if hasattr(backend, 'channel'):
                hubs.append(backend.channel)
        hubs = list(set(hubs))
    except Exception as ex:
        logger.warning(f"Failed to get hubs: {ex}")
    return hubs


# Get default hub
async def get_ibmq_default_hub(user: str):
    provider = await retrieve_provider(user, "ibmq")
    hub = (
        provider["additionalInfo"].get("defaultHub")
        if provider["additionalInfo"].get("defaultHub")
        else "ibm_quantum_platform"
    )
    return hub


# Pre-filter the appropriate IBMQ Backend from the database
async def pre_select_ibmq_backend(
    currentUser: str, beReq: BackendRequestSchema, hub: str
):
    # Check if that backend exists or not
    backends = await get_backends_from_db(user=currentUser, provider="ibmq")
    backend = []
    for bk in backends:
        if beReq.type:
            if (
                int(bk["qubit"]) >= beReq.rQubit
                and bk["type"] == beReq.type
                and bk["backendInfo"].get("hub", "") == hub
            ):
                backend.append(bk["name"])
        else:
            if int(bk["qubit"]) >= beReq.rQubit and bk["backendInfo"].get("hub", "") == hub:
                backend.append(bk["name"])
    return backend


async def get_ibmq_backends(user, hub: str) -> list:
    backendList = []
    username = user["username"]
    providerInfo = await retrieve_provider(username, "ibmq")
    providerToken = providerInfo["providerToken"]
    provider = initialize_IBMQProvider(ibmqToken=providerToken, hub=hub)
    if not provider:
        return backendList
    for backend in provider.backends():
        try:
            backendList.append(
                IBMQBackendSchema(
                    name=backend.name,
                    type="simulator" if getattr(backend, 'simulator', False) else "qpu",
                    qubit=getattr(backend, 'num_qubits', None),
                    user=username,
                    active=getattr(backend, 'operational', True),
                    sdk="qiskit",
                    backendInfo={
                        "hub": hub,
                        "name": backend.name,
                        "backend_version": backend.backend_version,
                        "num_qubits": backend.num_qubits,
                        "basis_gates": str(getattr(backend.configuration(), 'basis_gates', [])),
                        "last_updated": str(datetime.now()),
                    },
                )
            )
        except Exception as ex:
            logger.warning(ex)
            continue
    return backendList


async def check_job_result(user, backend_name, hub, jobId):
    username = user["username"]
    providerInfo = await retrieve_provider(username, "ibmq")
    providerToken = providerInfo["providerToken"]
    provider = initialize_IBMQProvider(ibmqToken=providerToken, hub=hub)
    if not provider:
        return None
    backend = provider.backend(backend_name)
    job = provider.job(jobId)
    jobStatus = ibmq_job_monitor(job, 2, 5)
    jobResult = None
    if jobStatus.get("status") == "DONE":
        counts = job.result()
        jobResult = dict(counts.get_counts())
    return {
        "providerJobId": job.job_id,
        "jobStatus": jobStatus,
        "backend": {"name": backend.name, "hub": hub},
        "jobResult": jobResult,
    }


def ibmq_job_monitor(job, interval: int, max_iterations: int):
    """Monitor job status at IBM Quantum

    Args:
    - job: Job instance
    - interval (int): Interval time to check job status (in seconds)

    Returns:
    - Job status
    """
    status = job.status()
    iteration = 0
    while status.name not in ["DONE", "CANCELLED", "ERROR"]:
        time.sleep(interval)
        status = job.status()
        msg = status.value
        iteration += 1
        if iteration >= max_iterations:
            break
    msg = status.value
    details = msg
    jobStatus = {"status": status.name, "details": details}
    return jobStatus


def get_least_busy_backend(preSelectedBackend: list, providerToken: str, hub: str):
    provider = initialize_IBMQProvider(ibmqToken=providerToken, hub=hub)
    if not provider:
        return None
    backends = []
    logger.info(
        "Select least busy backend in the following candidates: "
        + str(preSelectedBackend)
    )
    for bk in preSelectedBackend:
        backends.append(provider.backend(bk))
    try:
        selectedBackend =  provider.least_busy(Operational=True).name()
    except Exception as e:
        logger.error(e)
    return selectedBackend
