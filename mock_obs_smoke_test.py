"""One-command smoke test for Huawei Cloud OBS upload and download."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


# ======================== HARDCODE CONFIG START ========================
# Replace these values directly before running the script.
OBS_ACCESS_KEY = "HPUAYLRPR6DJKAA9EUBT"
OBS_SECRET_KEY = "rQJcALjyJqot784hUYfQb20MQOIPJNaMsf9PTfZY"
OBS_SERVER = "https://obs.cn-north-4.myhuaweicloud.com"
OBS_BUCKET = "vllm-ascend"
OBS_OBJECT_PREFIX = "ci/precision-test/mock-upload-download"
OBS_DOWNLOAD_PREFIX = "ci/precision-test/"
LOCAL_DOWNLOAD_ROOT = "obs-downloads"

# Validity period of the browser-downloadable signed URL, in seconds.
SIGNED_DOWNLOAD_URL_EXPIRES = 3600

# Number of Markdown files uploaded in one test run.
MOCK_FILE_COUNT = 5

# True: install esdk-obs-python automatically when it is not available.
AUTO_INSTALL_OBS_SDK = True
# ========================= HARDCODE CONFIG END =========================


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_obs_client_class():
    try:
        from obs import ObsClient

        return ObsClient
    except ImportError:
        if not AUTO_INSTALL_OBS_SDK:
            raise RuntimeError(
                "Missing dependency. Run: python -m pip install esdk-obs-python"
            ) from None

    print("[SETUP] Installing esdk-obs-python ...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "esdk-obs-python"],
        check=True,
    )
    from obs import ObsClient

    return ObsClient


def validate_config() -> None:
    placeholders = {
        "OBS_ACCESS_KEY": OBS_ACCESS_KEY,
        "OBS_SECRET_KEY": OBS_SECRET_KEY,
        "OBS_SERVER": OBS_SERVER,
        "OBS_BUCKET": OBS_BUCKET,
        "OBS_OBJECT_PREFIX": OBS_OBJECT_PREFIX,
        "OBS_DOWNLOAD_PREFIX": OBS_DOWNLOAD_PREFIX,
        "LOCAL_DOWNLOAD_ROOT": LOCAL_DOWNLOAD_ROOT,
    }
    missing = [
        name
        for name, value in placeholders.items()
        if not value.strip() or "REPLACE_WITH" in value
    ]
    if missing:
        raise RuntimeError(
            "Fill in the HARDCODE CONFIG section first: " + ", ".join(missing)
        )
    if SIGNED_DOWNLOAD_URL_EXPIRES <= 0:
        raise RuntimeError("SIGNED_DOWNLOAD_URL_EXPIRES must be greater than zero")
    if MOCK_FILE_COUNT <= 0:
        raise RuntimeError("MOCK_FILE_COUNT must be greater than zero")


def require_success(operation: str, response) -> None:
    status = getattr(response, "status", None)
    if status is not None and status < 300:
        print(f"[{operation}] OK, HTTP {status}")
        return

    error_code = getattr(response, "errorCode", "unknown")
    error_message = getattr(response, "errorMessage", "unknown")
    request_id = getattr(response, "requestId", "unknown")
    raise RuntimeError(
        f"{operation} failed: HTTP {status}, code={error_code}, "
        f"message={error_message}, request_id={request_id}"
    )


def list_objects(client, prefix: str) -> list:
    """List every object below an OBS prefix, including paginated results."""
    objects = []
    marker = None

    while True:
        response = client.listObjects(
            OBS_BUCKET,
            prefix=prefix,
            marker=marker,
            max_keys=1000,
        )
        require_success("LIST", response)
        body = response.body
        objects.extend(body.contents or [])

        if not body.is_truncated:
            break
        marker = body.next_marker
        if not marker:
            raise RuntimeError("OBS returned a truncated list without next_marker")

    return objects


def main() -> int:
    validate_config()
    ObsClient = load_obs_client_class()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_prefix = f"{OBS_OBJECT_PREFIX.rstrip('/')}/batch-{timestamp}/"
    download_prefix = OBS_DOWNLOAD_PREFIX.rstrip("/") + "/"

    client = ObsClient(
        access_key_id=OBS_ACCESS_KEY,
        secret_access_key=OBS_SECRET_KEY,
        server=OBS_SERVER,
        timeout=30,
        max_retry_count=1,
    )

    with tempfile.TemporaryDirectory(prefix="obs-smoke-test-") as temp_dir:
        temp_path = Path(temp_dir)
        upload_dir = temp_path / "upload"
        download_dir = Path(LOCAL_DOWNLOAD_ROOT) / timestamp
        upload_dir.mkdir()
        download_dir.mkdir(parents=True, exist_ok=True)

        try:
            print(f"[BATCH] Uploading {MOCK_FILE_COUNT} files to:")
            print(f"obs://{OBS_BUCKET}/{run_prefix}")

            for index in range(1, MOCK_FILE_COUNT + 1):
                filename = f"smoke-test-{index:02d}.md"
                object_key = f"{run_prefix}{filename}"
                upload_path = upload_dir / filename
                markdown = (
                    "# OBS batch upload/download smoke test\n\n"
                    f"Generated at UTC: {timestamp}\n\n"
                    f"Batch file: {index}/{MOCK_FILE_COUNT}\n"
                )
                upload_path.write_text(markdown, encoding="utf-8")

                upload_response = client.putFile(
                    OBS_BUCKET,
                    object_key,
                    str(upload_path),
                )
                require_success(f"UPLOAD {index}/{MOCK_FILE_COUNT}", upload_response)

            print(f"[BATCH] Traversing complete OBS prefix: {download_prefix}")
            objects = list_objects(client, download_prefix)
            if not objects:
                raise RuntimeError(f"No objects found below prefix: {download_prefix}")
            print(f"[LIST] Found {len(objects)} objects")
            print(f"[SNAPSHOT] Local directory: {download_dir.resolve()}")

            current_directory = None
            for index, object_info in enumerate(objects, start=1):
                object_key = object_info.key
                relative_name = object_key.removeprefix(download_prefix)
                if not relative_name or relative_name.endswith("/"):
                    print(f"[SKIP] Folder marker: {object_key}")
                    continue

                relative_path = PurePosixPath(relative_name)
                if relative_path.is_absolute() or ".." in relative_path.parts:
                    raise RuntimeError(f"Unsafe OBS object key: {object_key}")

                directory = str(relative_path.parent)
                if directory != current_directory:
                    current_directory = directory
                    print()
                    print(f"[DIRECTORY] {directory}")

                download_path = download_dir.joinpath(*relative_path.parts)
                download_path.parent.mkdir(parents=True, exist_ok=True)
                print()
                print(f"[FILE {index}/{len(objects)}]")
                print(f"  Object key    : {object_key}")
                print(f"  Remote size   : {getattr(object_info, 'size', 'unknown')} bytes")
                print(
                    f"  Last modified : "
                    f"{getattr(object_info, 'lastModified', 'unknown')}"
                )
                print(f"  ETag          : {getattr(object_info, 'etag', 'unknown')}")
                print(f"  Local path    : {download_path}")
                download_response = client.getObject(
                    OBS_BUCKET,
                    object_key,
                    downloadPath=str(download_path),
                )
                require_success(
                    f"DOWNLOAD {index}/{len(objects)}", download_response
                )

                uploaded_relative_name = object_key.removeprefix(run_prefix)
                upload_path = upload_dir / uploaded_relative_name
                if upload_path.is_file():
                    upload_hash = sha256(upload_path)
                    download_hash = sha256(download_path)
                    if upload_hash != download_hash:
                        raise RuntimeError(
                            f"Downloaded content does not match uploaded content: "
                            f"{object_key}"
                        )
                    print(f"[VERIFY] {relative_name}: SHA-256 {download_hash}")
                else:
                    print(f"[DOWNLOADED] {relative_name}")

                signed_url = client.createSignedUrl(
                    "GET",
                    OBS_BUCKET,
                    object_key,
                    expires=SIGNED_DOWNLOAD_URL_EXPIRES,
                )
                print(f"[DOWNLOAD URL] {signed_url.signedUrl}")

            print(
                f"[PASS] Traversed and downloaded all objects below {download_prefix}"
            )
            print("[KEEP] All remote test objects were retained in OBS.")
            return 0
        finally:
            client.close()

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1)
