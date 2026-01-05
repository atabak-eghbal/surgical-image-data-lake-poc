import os
from tqdm import tqdm
from src.generator import SurgicalPhantomGenerator
from src.metadata_store import MetadataStore
from src.s3_io import S3Client

BUCKET = os.getenv("S3_BUCKET")  # set this in your env
if not BUCKET:
    raise RuntimeError("Set env var S3_BUCKET to your bucket name.")

def main(n=50, noise_sigma=15.0):
    gen = SurgicalPhantomGenerator(output_dir="data/raw")
    db = MetadataStore("surgical_metadata.db")
    s3 = S3Client(bucket=BUCKET, prefix="raw")

    for _ in tqdm(range(n)):
        meta = gen.create_one(noise_sigma=noise_sigma)
        s3_uri = s3.upload_file(meta["local_path"], meta["filename"])
        db.insert({
            "image_id": meta["image_id"],
            "s3_uri": s3_uri,
            "anatomy": meta["anatomy"],
            "view_type": meta["view_type"],
            "pelvic_tilt": meta["pelvic_tilt"],
            "noise_sigma": meta["noise_sigma"],
        })

    print("✅ Ingest complete.")
    print("Example query (tilt>15):", db.query("Hip", min_tilt=15.0)[:5])

if __name__ == "__main__":
    main()

