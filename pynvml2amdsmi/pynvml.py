# SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# pynvml-to-amdsmi delegation module

from collections import namedtuple

from amdsmi import (
    AmdSmiAffinityScope,
    AmdSmiException,
    AmdSmiLibraryException,
    amdsmi_get_cpu_affinity_with_scope,
    amdsmi_get_gpu_activity,
    amdsmi_get_gpu_asic_info,
    amdsmi_get_gpu_device_uuid,
    amdsmi_get_gpu_enumeration_info,
    amdsmi_get_gpu_process_list,
    amdsmi_get_gpu_vram_usage,
    amdsmi_get_processor_handles,
    amdsmi_init,
    amdsmi_shut_down,
    amdsmi_wrapper,
)

__all__ = [
    "NVMLError",
    "NVMLError_NotSupported",
    "NVMLError_FunctionNotFound",
    "NVMLError_LibraryNotFound",
    "NVMLError_DriverNotLoaded",
    "NVMLError_NotFound",
    "NVMLError_Uninitialized",
    "NVMLError_Unknown",
    "NVML_DEVICE_MIG_DISABLE",
    "NVML_DEVICE_MIG_ENABLE",
    "nvmlInit",
    "nvmlShutdown",
    "nvmlDeviceGetCount",
    "nvmlDeviceGetIndex",
    "nvmlDeviceGetName",
    "nvmlDeviceGetUUID",
    "nvmlDeviceGetHandleByIndex",
    "nvmlDeviceGetHandleByUUID",
    "nvmlDeviceGetMemoryInfo",
    "nvmlDeviceGetCpuAffinity",
    "nvmlDeviceGetMigMode",
    "nvmlDeviceIsMigDeviceHandle",
    "nvmlDeviceGetComputeRunningProcesses",
    "nvmlDeviceGetUtilizationRates",
]


# ------------------------------------------------------------------------------
class NVMLError(Exception):
    def __init__(self, value):
        super().__init__(str(value))
        self.value = value


class NVMLError_NotSupported(NVMLError):
    pass


class NVMLError_FunctionNotFound(NVMLError):
    pass


class NVMLError_LibraryNotFound(NVMLError):
    pass


class NVMLError_DriverNotLoaded(NVMLError):
    pass


class NVMLError_NotFound(NVMLError):
    pass


class NVMLError_Uninitialized(NVMLError):
    pass


class NVMLError_Unknown(NVMLError):
    pass


def _handle_amdsmi_exception(e: AmdSmiException):
    if isinstance(e, AmdSmiLibraryException):
        match e.err_code:
            case amdsmi_wrapper.AMDSMI_STATUS_NOT_SUPPORTED:
                raise NVMLError_NotSupported(e.err_info)
            case amdsmi_wrapper.AMDSMI_STATUS_FAIL_LOAD_SYMBOL:
                raise NVMLError_FunctionNotFound(e.err_info)
            case amdsmi_wrapper.AMDSMI_STATUS_FAIL_LOAD_MODULE:
                raise NVMLError_LibraryNotFound(e.err_info)
            case amdsmi_wrapper.AMDSMI_STATUS_DRIVER_NOT_LOADED:
                raise NVMLError_DriverNotLoaded(e.err_info)
            case amdsmi_wrapper.AMDSMI_STATUS_NOT_FOUND:
                raise NVMLError_NotFound(e.err_info)
            case amdsmi_wrapper.AMDSMI_STATUS_INIT_ERROR:
                raise NVMLError_Uninitialized(e.err_info)
            case _:
                raise NVMLError_Unknown(e.err_info)
    else:
        raise NVMLError_Unknown(e.err_info)


# ------------------------------------------------------------------------------
NVML_DEVICE_MIG_DISABLE = 0
NVML_DEVICE_MIG_ENABLE = 1


# ------------------------------------------------------------------------------
def nvmlInit():
    try:
        amdsmi_init()
    except AmdSmiException as e:
        _handle_amdsmi_exception(e)


def nvmlShutdown():
    try:
        amdsmi_shut_down()
    except AmdSmiException as e:
        _handle_amdsmi_exception(e)


# ------------------------------------------------------------------------------
def nvmlDeviceGetCount():
    try:
        return len(amdsmi_get_processor_handles())
    except AmdSmiException as e:
        _handle_amdsmi_exception(e)


# ------------------------------------------------------------------------------
def nvmlDeviceGetIndex(handle):
    try:
        return amdsmi_get_gpu_enumeration_info(handle)["hip_id"]
    except KeyError as e1:
        raise NVMLError_Unknown(f"Internal Error: {e1}")
    except AmdSmiException as e2:
        _handle_amdsmi_exception(e2)


# ------------------------------------------------------------------------------
def nvmlDeviceGetName(handle):
    try:
        return amdsmi_get_gpu_asic_info(handle)["market_name"]
    except KeyError as e1:
        raise NVMLError_Unknown(f"Internal Error: {e1}")
    except AmdSmiException as e2:
        _handle_amdsmi_exception(e2)


# ------------------------------------------------------------------------------
def nvmlDeviceGetUUID(handle):
    try:
        return ("GPU-" + amdsmi_get_gpu_device_uuid(handle)).encode("utf-8")
    except AmdSmiException as e:
        _handle_amdsmi_exception(e)


# ------------------------------------------------------------------------------
def nvmlDeviceGetHandleByIndex(dev_id):
    try:
        return next(
            x for x in amdsmi_get_processor_handles() if nvmlDeviceGetIndex(x) == dev_id
        )
    except StopIteration:
        raise NVMLError_NotFound(f"Device Index {dev_id} not found")
    except AmdSmiException as e2:
        _handle_amdsmi_exception(e2)


# ------------------------------------------------------------------------------
def nvmlDeviceGetHandleByUUID(uuid: bytes):
    try:
        return next(
            x for x in amdsmi_get_processor_handles() if nvmlDeviceGetUUID(x) == uuid
        )
    except StopIteration:
        raise NVMLError_NotFound(f"Device uuid {uuid.decode()} not found")
    except AmdSmiException as e2:
        _handle_amdsmi_exception(e2)


# ------------------------------------------------------------------------------
NvmlMemInfo = namedtuple("NvmlMemInfo", "total free used")


def nvmlDeviceGetMemoryInfo(handle):
    try:
        usage = amdsmi_get_gpu_vram_usage(handle)
        used = usage["vram_used"] * 1024 * 1024
        total = usage["vram_total"] * 1024 * 1024
        free = total - used
        return NvmlMemInfo(total=total, free=free, used=used)
    except KeyError as e1:
        raise NVMLError_Unknown(f"Internal Error: {e1}")
    except AmdSmiException as e2:
        _handle_amdsmi_exception(e2)


# ------------------------------------------------------------------------------
def nvmlDeviceGetCpuAffinity(handle, cpu_set_size):
    try:
        return amdsmi_get_cpu_affinity_with_scope(
            handle, AmdSmiAffinityScope.NUMA_SCOPE
        )
    except AmdSmiException as e:
        _handle_amdsmi_exception(e)


# ------------------------------------------------------------------------------
def nvmlDeviceGetMigMode(handle):
    return (NVML_DEVICE_MIG_DISABLE, NVML_DEVICE_MIG_DISABLE)


def nvmlDeviceIsMigDeviceHandle(handle):
    return False


# ------------------------------------------------------------------------------
NvmlProcessInfo = namedtuple(
    "NvmlProcessInfo", "computeInstanceId gpuInstanceId pid usedGpuMemory"
)


def nvmlDeviceGetComputeRunningProcesses(handle):
    try:
        processes = amdsmi_get_gpu_process_list(handle)
        return [
            NvmlProcessInfo(
                computeInstanceId=0,
                gpuInstanceId=0,
                pid=p["pid"],
                usedGpuMemory=p["mem"],
            )
            for p in processes
        ]
    except KeyError as e1:
        raise NVMLError_Unknown(f"Internal Error: {e1}")
    except AmdSmiException as e2:
        _handle_amdsmi_exception(e2)


# ------------------------------------------------------------------------------
NvmlUtilization = namedtuple("NvmlUtilization", "gpu memory")


def nvmlDeviceGetUtilizationRates(handle):
    try:
        activity = amdsmi_get_gpu_activity(handle)
        return NvmlUtilization(
            gpu=activity["gfx_activity"], memory=activity["umc_activity"]
        )
    except KeyError as e1:
        raise NVMLError_Unknown(f"Internal Error: {e1}")
    except AmdSmiException as e2:
        _handle_amdsmi_exception(e2)
